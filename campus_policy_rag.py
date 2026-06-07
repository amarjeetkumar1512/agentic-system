import os
from pypdf import PdfReader
import chromadb
from google import genai
from sentence_transformers import SentenceTransformer

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)


chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="campus_policies"
)


def read_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def chunk_text(text, chunk_size=200, overlap=40):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def generate_embedding(text):

    embedding = embedding_model.encode(text)

    return embedding.tolist()

def load_documents():

    folder = "policy_documents"

    chunk_id = collection.count()

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(folder, file)

            print(f"\nLoading PDF: {file}")

            text = read_pdf_text(pdf_path)

            chunks = chunk_text(text)

            print(f"Created {len(chunks)} chunks")

            for chunk in chunks:

                embedding = generate_embedding(chunk)

                collection.add(
                    ids=[str(chunk_id)],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[
                        {
                            "source": file
                        }
                    ]
                )

                chunk_id += 1

    print("\nDocuments indexed successfully!")

def retrieve_chunks(query, top_k=3):

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results

def ask_llm(question, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a campus policy assistant.

Answer ONLY from the provided context.

If answer is not available in context, say:
"I don't have that information."

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text

def answer_question(question):

    results = retrieve_chunks(question)

    retrieved_docs = results["documents"][0]

    print("\nRetrieved Chunks:\n")

    for doc in retrieved_docs:

        print(doc)
        print("-" * 50)

    answer = ask_llm(question, retrieved_docs)

    return answer

if __name__ == "__main__":

    # API KEY CHECK

    if not os.getenv("GOOGLE_API_KEY"):

        print("\nERROR: GOOGLE_API_KEY not found!")
        exit()

    # LOAD VECTOR DB ONLY ONCE

    if collection.count() == 0:

        print("\nBuilding vector database...")

        load_documents()

        print("\nVector DB Ready!")

    else:

        print("\nVector DB already exists!")

    # CHAT LOOP

    while True:

        question = input("\nAsk Question (type exit to quit): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer)
