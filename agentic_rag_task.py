from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv
from typing import Literal
import os

print(" All libraries successfully imported")

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found!")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, api_key=openai_api_key)
print(f" LLM initialized: {llm.model_name}")

# 1. document collection
python_docs = [
    "Python functions use 'def' keyword. Functions can take parameters and return values. Example: def greet(name): return f'Hello, {name}!'",
    "Python classes use 'class' keyword. Classes have __init__ constructor. Example: class Dog: def __init__(self, name): self.name = name",
    "Python data structures: lists [], tuples (), dictionaries {}, sets {}. Lists are mutable, tuples immutable.",
    "Exception handling: try-except blocks. Example: try: x = 1/0 except ZeroDivisionError: print('Cannot divide by zero')",
    "File handling: with open('file.txt', 'r') as f: content = f.read(). Context managers auto-close files.",
    "Decorators modify function behavior. Example: @decorator def func(): pass. Used for logging, timing, auth.",
    "Virtual environments: python -m venv env. Activate: source env/bin/activate (Mac) or env\\Scripts\\activate (Windows)",
    "Flask web framework: from flask import Flask, app = Flask(__name__). @app.route('/') defines routes.",
    "Pandas for data analysis: import pandas as pd, df = pd.read_csv('data.csv'). Use df.head() to preview.",
    "pytest testing: def test_addition(): assert 1+1==2. Run with pytest test_file.py"
]

doc_objects = [Document(page_content=doc, metadata={"source": f"python_doc_{i+1}"}) 
               for i, doc in enumerate(python_docs)]
print(f" Created {len(doc_objects)} Python documents")

#  2. vector setup
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
doc_splits = text_splitter.split_documents(doc_objects)
print(f" Split into {len(doc_splits)} chunks")

chroma_path = "./python_tutorials_db"
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    embedding=embeddings,
    persist_directory=chroma_path
)
print(f" Vector store created at {chroma_path}")

# 3. Retrival tool
@tool
def retrieve_python_docs(query: str) -> str:
    """Search Python programming tutorials. Use for Python syntax, functions, classes, code examples."""
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    results = retriever.invoke(query)
    
    if not results:
        return "No relevant Python docs found."
    
    formatted = "\n---\n".join([f"Source: {r.metadata.get('source')}\n{r.page_content[:200]}..." 
                              for r in results])
    return formatted

print(" Retrieval tool created")

# 4. Agentic rag system
system_prompt = SystemMessage(content="""You are PyTutor, a Python programming assistant.

RETRIEVE WHEN:
Python syntax, functions, classes, libraries
"How to" or "what is" about Python
Code examples needed

ANSWER DIRECTLY WHEN:
Greetings, casual chat
Non-Python questions
Simple math or general knowledge

Cite sources when retrieving. Be concise.""")

tools = [retrieve_python_docs]
llm_with_tools = llm.bind_tools(tools)

def assistant(state: MessagesState) -> dict:
    messages = [system_prompt] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    return "tools" if state["messages"][-1].tool_calls else "__end__"

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", should_continue, {"tools": "tools", "__end__": END})
builder.add_edge("tools", "assistant")

agent = builder.compile(checkpointer=MemorySaver())
print(" Agentic RAG system compiled")

# 5. Testing
def test_agent(query: str, thread_id: str = "test"):
    print(f"\n{'='*60}")
    print(f": {query}")
    
    result = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"configurable": {"thread_id": thread_id}}
    )
    
    used_retrieval = any(isinstance(m, AIMessage) and m.tool_calls for m in result["messages"])
    answer = result["messages"][-1].content if result["messages"][-1].content else "No answer"
    
    print(f" {answer[:150]}...")
    print(f" {'RETRIEVED' if used_retrieval else 'DIRECT'}")
    print("="*60)
    
    return used_retrieval

print("\n:test_tube: TEST CASES:")
print("="*60)

# Test cases
tests = [
    ("How do I define a Python function?", True),
    ("What are Python decorators?", True),
    ("Hello! How are you?", False),
    ("What is 10 + 15?", False),
    ("Explain Python exception handling", True),
]

results = []
for query, expected in tests:
    actual = test_agent(query, f"test_{len(results)}")
    correct = actual == expected
    results.append(correct)
    print(f"Expected: {'RETRIEVE' if expected else 'DIRECT'} | {':' if correct else ':x:'}")

accuracy = sum(results) / len(results) * 100
print(f"\n Accuracy: {accuracy:.0f}% ({sum(results)}/{len(results)} correct)")

# Interactive mode
def interactive_mode():
    print("\n" + "="*60)
    print(" Python Tutor - Interactive Mode")
    print("Type 'exit' to quit")
    print("="*60)
    
    thread_id = "interactive"
    while True:
        query = input("\n: You: ").strip()
        if query.lower() in ["exit", "quit"]:
            print(" Goodbye! Happy coding!")
            break
        
        result = agent.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": thread_id}}
        )
        print(f" {result['messages'][-1].content}")

interactive_mode()
