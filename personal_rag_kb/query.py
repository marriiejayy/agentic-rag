
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

print("API key loaded")

# Load FAISS Vector Store 
VECTOR_STORE_PATH = "vectorstore_faiss"
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectorstore = FAISS.load_local(VECTOR_STORE_PATH, embeddings)

print(f"\n✅ FAISS vector store loaded from '{VECTOR_STORE_PATH}'")

# Simple Query 
def simple_query(query_text, k=3):
    results = vectorstore.similarity_search(query_text, k=k)
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:\n{doc.page_content}\n")
    return results

# Conversational RAG 

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

#conversational memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Conversational retrieval chain
conv_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    memory=memory,
    return_source_documents=True
)

def chat_query(query_text):
    response = conv_chain({"question": query_text})
    answer = response["answer"]
    sources = response.get("source_documents", [])
    
    print(f"\nAnswer:\n{answer}\n")
    if sources:
        print("Sources:")
        for i, src in enumerate(sources):
            print(f"{i+1}: {src.metadata.get('source', 'Unknown')}")
    return response

if __name__ == "__main__":
    print("\nWelcome to your Personal RAG Assistant!")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! ")
            break
        
        print("\n--- Simple Retrieval Results ---")
        simple_query(user_input)
        
        print("\n--- Conversational RAG Answer ---")
        chat_query(user_input)
        print("\n" + "-"*50 + "\n")
