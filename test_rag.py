import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from rag import load_knowledge_base, embed_knowledge_base, retrieve_top_k, generate_answer

def run_tests():
    entries = load_knowledge_base()
    print(f"Loaded {len(entries)} entries from knowledge_base.json.")
    
    # Embed all entries
    print("Embedding entries with embeddinggemma...")
    embedded = embed_knowledge_base(entries, "http://localhost:11434", "embeddinggemma")
    print("Embeddings complete!")
    
    test_questions = [
        # Answerable
        ("When is the Ho Chi Minh Mausoleum open for visitors?", "G03"),
        ("What is the entrance ticket price for the Temple of Literature?", "G04"),
        ("Where can I eat authentic Cha Ca La Vong in Hanoi?", "G16"),
        # Paraphrase
        ("How much does admission cost for adults at Hoa Lo Prison?", "G09"),
        # Not in guide
        ("What time does the Eiffel Tower open in Paris?", None),
        ("Where can I rent a helicopter to tour Hanoi?", None),
    ]
    
    print("\n" + "="*80)
    for q, expected_id in test_questions:
        print(f"\n[Question]: {q}", flush=True)
        print(f"[Expected ID]: {expected_id}", flush=True)
        retrieved = retrieve_top_k(q, embedded, k=3, base_url="http://localhost:11434", model="embeddinggemma")
        retrieved_ids = [r[0]["id"] for r in retrieved]
        top_score = retrieved[0][1] if retrieved else 0.0
        print(f"[Retrieved IDs]: {retrieved_ids} (Top Score: {top_score:.4f})", flush=True)
        
        answer = generate_answer(q, retrieved, base_url="http://localhost:11434", chat_model="qwen3:4b")
        print(f"[Answer]:\n{answer}", flush=True)
        print("-" * 60, flush=True)

if __name__ == "__main__":
    run_tests()
