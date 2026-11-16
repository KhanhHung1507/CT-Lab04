"""RAG (Retrieval-Augmented Generation) module for Lumen Travel Assistant."""
import json
import os
from pathlib import Path
from typing import Any
import numpy as np
import requests

REQUEST_TIMEOUT = 180


class RagError(Exception):
    """Safe user-facing error message for RAG operations."""
    pass


def load_knowledge_base(file_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load guide entries from knowledge_base.json."""
    if file_path is None:
        file_path = Path(__file__).resolve().parent / "knowledge_base.json"
    else:
        file_path = Path(file_path)

    if not file_path.exists():
        raise RagError(f"Knowledge base file not found at: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Knowledge base must contain a JSON array of entries.")
        return data
    except Exception as e:
        raise RagError(f"Failed to read knowledge base: {e}") from e


def get_embedding(text: str, base_url: str, model: str) -> np.ndarray:
    """Request vector embedding for a single text from Ollama server."""
    base_url = base_url.rstrip("/")
    if not text.strip():
        raise RagError("Cannot generate embedding for empty text.")

    # Try /api/embeddings first (standard Ollama endpoint)
    url = f"{base_url}/api/embeddings"
    payload = {"model": model, "prompt": text}
    
    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise RagError(f"Cannot connect to Ollama server at {base_url}. Please ensure Ollama or Pinggy is running.")
    except requests.exceptions.Timeout:
        raise RagError("Ollama embedding request timed out. Please try again.")
    except requests.RequestException as e:
        raise RagError(f"Network error while connecting to Ollama: {e}")

    if not response.ok:
        # Fallback check for newer Ollama /api/embed endpoint
        if response.status_code == 404:
            alt_url = f"{base_url}/api/embed"
            try:
                alt_resp = requests.post(alt_url, json={"model": model, "input": text}, timeout=REQUEST_TIMEOUT)
                if alt_resp.ok:
                    data = alt_resp.json()
                    vec = data.get("embeddings", [[]])[0]
                    if vec:
                        return np.array(vec, dtype=np.float32)
            except Exception:
                pass
        
        try:
            err_msg = response.json().get("error", response.text)
        except Exception:
            err_msg = response.text
        raise RagError(f"Ollama embedding failed ({response.status_code}): {err_msg}")

    try:
        data = response.json()
        vec = data.get("embedding")
        if not vec and "embeddings" in data:
            vec = data["embeddings"][0]
        if not vec:
            raise ValueError("No embedding vector returned in response.")
        return np.array(vec, dtype=np.float32)
    except Exception as e:
        raise RagError(f"Failed to parse embedding response: {e}") from e


def embed_knowledge_base(entries: list[dict[str, Any]], base_url: str, model: str) -> list[dict[str, Any]]:
    """Embed all entries once. Returns entries enriched with 'embedding' vector."""
    embedded = []
    for entry in entries:
        # Combine title, category, tags, and text for rich semantic representation
        title = entry.get("title", "")
        category = entry.get("category", "")
        tags = ", ".join(entry.get("tags", []))
        text = entry.get("text", "")
        content_to_embed = f"Title: {title}. Category: {category}. Tags: {tags}. Description: {text}"
        
        vec = get_embedding(content_to_embed, base_url, model)
        entry_copy = dict(entry)
        entry_copy["embedding"] = vec
        embedded.append(entry_copy)
    return embedded


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two 1D vectors."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def retrieve_top_k(
    query: str,
    embedded_entries: list[dict[str, Any]],
    k: int = 3,
    base_url: str = "http://localhost:11434",
    model: str = "embeddinggemma"
) -> list[tuple[dict[str, Any], float]]:
    """Embed query and retrieve top-k entries ordered by descending cosine similarity."""
    if not query.strip():
        return []

    query_vec = get_embedding(query, base_url, model)
    scored = []
    for entry in embedded_entries:
        score = cosine_similarity(query_vec, entry["embedding"])
        scored.append((entry, score))

    # Sort descending by similarity score
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


def generate_answer(
    query: str,
    retrieved_entries: list[tuple[dict[str, Any], float]],
    base_url: str = "http://localhost:11434",
    chat_model: str = "qwen3:4b",
    similarity_threshold: float = 0.35,
) -> str:
    """Generate answer using Ollama /api/chat based STRICTLY on retrieved entries."""
    # Check if retrieval found any relevant information
    if not retrieved_entries or retrieved_entries[0][1] < similarity_threshold:
        return "I don't know based on the provided travel guide."

    # Build context from retrieved entries
    context_blocks = []
    for entry, score in retrieved_entries:
        context_blocks.append(
            f"Entry ID: [{entry['id']}]\n"
            f"Title: {entry['title']}\n"
            f"Content: {entry['text']}"
        )
    context_str = "\n\n".join(context_blocks)

    full_prompt = (
        f"You are Lumen Travel Assistant for Hanoi.\n"
        f"Here is the travel guide information:\n\n"
        f"{context_str}\n\n"
        f"Task: Answer the user's question using ONLY the guide information above. "
        f"Always include the entry ID like [G02]. "
        f"If the guide does not contain the answer, reply: 'I don't know based on the provided travel guide.'\n\n"
        f"User question: {query.strip()}"
    )

    url = f"{base_url.rstrip('/')}/api/chat"
    payload = {
        "model": chat_model,
        "messages": [
            {"role": "user", "content": full_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 512,
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT * 2)
    except requests.exceptions.ConnectionError:
        raise RagError(f"Cannot reach Ollama chat service at {base_url}.")
    except requests.exceptions.Timeout:
        raise RagError("Ollama chat generation timed out.")
    except requests.RequestException as e:
        raise RagError(f"Network error communicating with Ollama chat: {e}")

    if not response.ok:
        try:
            err_msg = response.json().get("error", response.text)
        except Exception:
            err_msg = response.text
        raise RagError(f"Chat generation failed ({response.status_code}): {err_msg}")

    try:
        data = response.json()
        content = data.get("message", {}).get("content", "").strip()
        if not content:
            return "I don't know based on the provided travel guide."
        return content
    except Exception as e:
        raise RagError(f"Failed to parse chat response: {e}") from e
