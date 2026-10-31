
from rag import retrieve_knowledge

query = """
The production database is down.
Users are getting connection timeout errors.
The connection pool is exhausted.
"""

results = retrieve_knowledge(query, top_k=3)

print("\n===== AEGISAI KNOWLEDGE RETRIEVAL =====")

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print("Similarity:", result["similarity"])
    print("Knowledge:")
    print(result["content"][:500])
