import sqlite3
import sqlite_vec
import json
from sentence_transformers import SentenceTransformer

DB_PATH = "db/rag.db"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect DB
conn = sqlite3.connect(DB_PATH)
conn.enable_load_extension(True)
sqlite_vec.load(conn)


def retrieve(query, top_k=3):
    """
    Search similar chunks from vector DB
    """

    # Convert query → embedding
    query_embedding = model.encode(query).tolist()

    # Search vector DB
    results = conn.execute(
        """
        SELECT documents.content, distance
        FROM embeddings
        JOIN documents ON embeddings.rowid = documents.id
        WHERE embedding MATCH ?
        AND k = ?
        ORDER BY distance
        """,
        (json.dumps(query_embedding), top_k)
    ).fetchall()

    return results


if __name__ == "__main__":
    query = input("Ask something: ")

    results = retrieve(query)

    print("\nTop matches:\n")

    for i, (text, score) in enumerate(results, 1):
        print(f"{i}. Score: {score:.4f}")
        print(text)
        print("-" * 50)