import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

print(" API key loaded")


DATA_PATHS = [
    "knowledge_base/personal_docs",
    "knowledge_base/projects"
]

# 1. Load documents
all_docs = []

for path in DATA_PATHS:
    if os.path.exists(path):
        # Load PDFs
        pdf_loader = DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader)
        all_docs.extend(pdf_loader.load())

        txt_loader = DirectoryLoader(path, glob="*.md", loader_cls=TextLoader)
        all_docs.extend(txt_loader.load())
    else:
        print(f" Path does not exist: {path}")

print(f"\nLoaded {len(all_docs)} documents")

# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(all_docs)

print(f"\nSplit documents into {len(chunks)} chunks")

# 3.  embeddings
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

# 4. Build FAISS vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# 5. Save the vector store locally
VECTOR_STORE_PATH = "vectorstore_faiss"
vectorstore.save_local(VECTOR_STORE_PATH)

print(f"\n FAISS vector store saved at '{VECTOR_STORE_PATH}'")
print("You can now run query.py to test your RAG system!")
