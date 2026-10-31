
from pathlib import Path
from sentence_transformers import SentenceTransformer, util


# Load embedding model locally
model = SentenceTransformer("all-MiniLM-L6-v2")


# Read knowledge base
KNOWLEDGE_FILE = (
    Path(__file__).parent
    / "knowledge_base"
    / "troubleshooting.md"
)


def load_knowledge_base():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return file.read()


# Split document into chunks
def create_chunks(text):

    sections = text.split("\n## ")

    chunks = []

    for section in sections:

        section = section.strip()

        if len(section) > 50:
            chunks.append(section)

    return chunks


# Generate embeddings
knowledge_text = load_knowledge_base()
knowledge_chunks = create_chunks(knowledge_text)

knowledge_embeddings = model.encode(
    knowledge_chunks,
    convert_to_tensor=True
)


# Retrieve relevant knowledge
def retrieve_knowledge(query: str, top_k: int = 3):

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    scores = util.cos_sim(
        query_embedding,
        knowledge_embeddings
    )[0]

    top_results = scores.topk(
        min(top_k, len(knowledge_chunks))
    )

    retrieved_chunks = []

    for score, index in zip(
        top_results.values,
        top_results.indices
    ):

        retrieved_chunks.append({
            "content": knowledge_chunks[index.item()],
            "similarity": round(score.item(), 3)
        })

    return retrieved_chunks
