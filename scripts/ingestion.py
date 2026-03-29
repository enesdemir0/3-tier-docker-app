import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore  # Swapped from Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# 1. Initialize Embeddings (MPNet Base V2 = 768 dimensions)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 2. Initialize the Pinecone Retriever 
# This part "connects" to the cloud index
index_name = os.getenv("PINECONE_INDEX_NAME")

vectorstore = PineconeVectorStore(
    index_name=index_name,
    embedding=embeddings
)

retriever = vectorstore.as_retriever()

# ==========================================================
# THE INGESTION LOGIC
# ==========================================================
if __name__ == "__main__":
    print(f"--- STARTING PINE CONE INGESTION TO INDEX: {index_name} ---")
    
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]

    print("Loading documents from web...")
    # Using WebBaseLoader to scrape the blog posts
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    print("Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, 
        chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)

    print(f"Uploading {len(doc_splits)} chunks to Pinecone...")
    
    # This sends your data to the Pinecone Cloud!
    PineconeVectorStore.from_documents(
        documents=doc_splits,
        embedding=embeddings,
        index_name=index_name
    )
    
    print("✅ Ingestion Complete! Your data is now in the Pinecone Cloud.")