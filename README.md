# Practice 03: Sign-In Travel Assistant with RAG Chat (Lumen Travel)

## 1. Student Information & Chosen City
* **Student name:** Nguyễn Khánh Hưng
* **Student ID:** 25127344
* **Course:** Computational Thinking
* **Chosen City:** **Hanoi, Vietnam**
* **Video Demonstration Link:** [Video Demo](https://drive.google.com/file/d/1CJx7MRcSsJrw1qyLZcuBca2ypIJw7m02/view?usp=sharing)
* **GitHub Repository:** [https://github.com/KhanhHung1507/CT-Lab04](https://github.com/KhanhHung1507/CT-Lab04)

---

## 2. Project Overview & Architecture
**Lumen Travel** is a verified AI travel assistant for Hanoi city. General chatbots frequently hallucinate opening hours, ticket prices, and locations. Lumen Travel solves this by:
1. Requiring user authentication via Firebase Authentication before accessing the chat assistant.
2. Answering questions strictly based on a curated, factual travel guide (`knowledge_base.json`) with 16 iconic Hanoi attractions and culinary landmarks (Hoan Kiem Lake, Imperial Citadel of Thang Long, Ho Chi Minh Mausoleum, Temple of Literature, Old Quarter, Hoa Lo Prison, Cha Ca La Vong, etc.).
3. Citing specific guide entry IDs (e.g. `[G03]`, `[G04]`) and showing similarity scores in an expandable UI panel.
4. Saying "I don't know based on the provided travel guide." whenever a query cannot be answered by the guide, preventing hallucination.
5. Managing session chat history in `st.session_state` and clearing it completely upon sign-out (no external database persistence).

---

## 3. Installation & Running Instructions

### Prerequisites
* Python 3.10+ (tested with Python 3.12 / 3.14)
* Ollama installed and running with models:
  ```bash
  ollama pull embeddinggemma
  ollama pull qwen3:4b
  ```

### Step 1: Clone the Repository & Navigate
```bash
git clone https://github.com/KhanhHung1507/CT-Lab04.git
cd CT-Lab04
```

### Step 2: Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your Firebase credentials in `.env`:
```env
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_API_KEY=your-firebase-web-api-key
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=embeddinggemma
OLLAMA_CHAT_MODEL=qwen3:4b
```

### Step 4: Run the Streamlit Application
```bash
py -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 4. Test Table (At Least 6 Questions)

The system was evaluated with 6 representative queries: 3 answerable, 1 paraphrase, and 2 out-of-domain / not in guide.

| # | Question Type | User Question | Expected Entry ID | Retrieved IDs (Top Score) | Correct? | Failed Step (if wrong) |
|---|---------------|---------------|-------------------|---------------------------|----------|------------------------|
| 1 | Answerable | "When is the Ho Chi Minh Mausoleum open for visitors?" | `G03` | `['G03', 'G01', 'G13']` (0.6489) | **Yes** | None (Retrieved G03; correctly cited [G03] and detailed Tue-Thu, Sat-Sun summer 7:30-10:30 AM & winter 8:00-11:00 AM) |
| 2 | Answerable | "What is the entrance ticket price for the Temple of Literature?" | `G04` | `['G04', 'G01', 'G12']` (0.5726) | **Yes** | None (Retrieved G04; correctly cited [G04] and stated 30,000 VND per adult and 15,000 VND for students) |
| 3 | Answerable | "Where can I eat authentic Cha Ca La Vong in Hanoi?" | `G16` | `['G16', 'G05', 'G01']` (0.6101) | **Yes** | None (Retrieved G16; correctly cited [G16] at 14 Cha Ca Street in Hanoi Old Quarter) |
| 4 | Paraphrase | "How much does admission cost for adults at Hoa Lo Prison?" | `G09` | `['G09', 'G01', 'G03']` (0.5724) | **Yes** | None (Dense embedding correctly mapped 'admission cost for adults' to Hoa Lo Prison G09 with fee 30,000 VND) |
| 5 | Not in Guide (Out of domain) | "What time does the Eiffel Tower open in Paris?" | `None` | `['G01', 'G06', 'G07']` (0.3338) | **Yes** | None (Top score 0.3338 < threshold 0.35; system immediately returned "I don't know based on the provided travel guide.") |
| 6 | Not in Guide (In domain, unlisted activity) | "Where can I rent a helicopter to tour Hanoi?" | `None` | `['G01', 'G05', 'G03']` (0.4700) | **Yes** | None (Retrieval passed threshold with G01/G05/G03, but LLM inspected context, found no helicopter rentals, and correctly answered "I don't know based on the provided travel guide.") |

---

## 5. Computational Thinking Analysis

### 5.1. Abstraction
* **Input:** Raw user question string in natural language, along with user authentication credentials (email & password).
* **Output:** A concise, factual answer citing source entries (e.g., `[G03]`), plus an expandable UI panel exposing retrieved entry metadata and cosine similarity scores.
* **Knowledge Base Fields kept:**
  * `id`: Short unique identifier (`G01`, `G02`...) for precise citation without flooding the prompt.
  * `title`: Name of the landmark, museum, or eatery for human clarity and fast keyword match.
  * `category`: Broad classification (e.g. `historical`, `culture`, `cuisine`, `nature`, `architecture`) enabling metadata filtering in RAG-Rec.
  * `tags`: Granular attributes (`["lake", "walking-street", "unesco", "street-food"]`) for future faceted search and recommendation.
  * `text`: Factual description restricted strictly to verifiable details (hours, prices, addresses, precautions). Extraneous marketing fluff was eliminated.
  * `source`: Verifiable provenance (e.g. Hanoi Department of Tourism, Management Board) to ensure credibility.

### 5.2. Decomposition
The system is divided into modular, decoupled pipelines:

```
[User Credentials] ──► [1. Sign-In / Auth] ──► [User Session (st.session_state)]
                                                        │
[knowledge_base.json] ──► [2. One-time Embedding] ──────┼──► [Cached Vector Store]
                                                        │              │
[User Question] ──► [3. Query Embedding] ───────────────┤              │
                            │                           │              │
                            ▼                           │              │
                 [4. Cosine Retrieval] ◄────────────────┘              │
                            │                                          │
                    (Top-k Entries + Scores)                            │
                            │                                          │
                            ▼                                          │
                 [5. Context Builder]                                  │
                            │                                          │
                      (Prompt + Context)                                │
                            │                                          │
                            ▼                                          │
                [6. Generation (qwen3:4b)]                              │
                            │                                          │
                            ▼                                          │
              [7. Display Answer & Sources] ◄───────────────────────────┘
```

* **Box 1 (Auth):** Input: Email, Password. Output: User token / UID in `st.session_state`.
* **Box 2 (Embed Guide):** Input: `knowledge_base.json`. Output: 768-dimensional NumPy vectors stored via `@st.cache_resource`.
* **Box 3 (Query Embed):** Input: User question. Output: Query vector.
* **Box 4 (Retrieve):** Input: Query vector, guide vectors, $k=3$. Output: Top-$k$ sorted pairs `(entry, score)`.
* **Box 5 (Build Context):** Input: Top-$k$ entries. Output: Formatted context block with IDs.
* **Box 6 (Generate):** Input: Context block, question, strict prompt. Output: Generated answer citing IDs or "I don't know".
* **Box 7 (Display & Cleanup):** Input: Generated answer, retrieved sources. Output: Streamlit chat UI. Cleared on Sign-out.

### 5.3. Pattern Recognition
* **Reused from Lab 3:** Firebase Authentication REST API patterns (`create_account`, `sign_in`, credential validation, secure error wrapping without leaking API keys).
* **Reused from Lab 4:** REST interaction with Ollama daemon (`/api/embeddings`, `/api/chat`), Prompt templating with system and user roles.
* **Filter $\rightarrow$ Score $\rightarrow$ Top-$k$ Pattern:**
  * In this Lab: Compute cosine similarity across all guide entries $\rightarrow$ Score each entry $\rightarrow$ Select Top-$k$ highest scores.
  * In Assignment 4 (RAG-Rec): The same pattern reappears in recommendation: Filter candidates by user preference (`category`, `tags`) $\rightarrow$ Score candidates based on embedding similarity or preference weights $\rightarrow$ Return Top-$k$ recommended places.

### 5.4. Algorithm Design
* **Pseudo-code for Answering a Query:**
  ```python
  def answer_question(query, embedded_guide, k=3, threshold=0.35):
      query_vec = get_embedding(query)
      scored_entries = []
      for entry in embedded_guide:
          sim = dot(query_vec, entry.vec) / (norm(query_vec) * norm(entry.vec))
          scored_entries.append((entry, sim))
      
      scored_entries.sort(key=lambda x: x.score, reverse=True)
      top_k = scored_entries[:k]
      
      # Fast threshold check (Layer 1 guardrail)
      if top_k[0].score < threshold:
          return "I don't know based on the provided travel guide.", top_k
          
      context = format_entries_with_ids(top_k)
      response = call_llm(system_prompt, context, query)
      return response, top_k
  ```
* **Design Decision Rationale:**
  * **Choice of $k=3$:** Balances sufficient contextual detail with low CPU latency and compact prompt size for the 4B parameter model.
  * **Two-Layer "I don't know" Guardrail:**
    * *Layer 1 (Retrieval Score Threshold $\tau = 0.35$):* Completely out-of-domain queries (e.g. Eiffel Tower in Paris, top score 0.3338) are short-circuited immediately without running the LLM, reducing latency to $< 0.5$s and eliminating hallucination risk.
    * *Layer 2 (Strict Prompting Constraint):* If a query passes the retrieval score but asks for an unlisted detail (e.g. "rent a helicopter in Hanoi", top score 0.4700), the LLM inspects the retrieved context and explicitly declares that no helicopter rentals are documented.

---

## 6. Known Limitations & AI Tools Used
* **Known Limitations:**
  * Running locally on CPU requires 8–15 seconds per LLM response.
  * Knowledge base currently contains 16 curated entries for Hanoi; queries about other cities or unlisted restaurants will yield "I don't know".
  * Embeddings are generated once at application startup; dynamically adding entries during runtime requires an app reload to refresh the cache.
* **Note on AI Tools Used:**
  * Used `embeddinggemma` via Ollama for semantic vector embeddings.
  * Used `qwen3:4b` via Ollama for grounded context-based generation.
  * Used AI coding assistance (Antigravity by Google DeepMind) to structure and refactor the Streamlit and RAG modules.
