from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# loading environment variables from .env file 
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found! Please set it in your .env file.")

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=openai_api_key
)

# system prompt for customer support
customer_support_prompt = SystemMessage(
    content="""You are a helpful customer support representative for Marriejays Gadgets.
    You specialize in troubleshooting electronics, particularly laptops, phones, and tablets.
    Always be polite, patient, and solution-oriented.
    Ask clarifying questions when needed.
    Remember the entire conversation history to provide consistent support."""
)

# Assistant node function
def customer_support_assistant(state: MessagesState) -> dict:
    """
    Customer support node - processes messages and generates helpful responses.
    """
    # system prompt with conversation history
    messages = [customer_support_prompt] + state["messages"]
    
    # response from LLM
    response = llm.invoke(messages)
    
    # Return as state update
    return {"messages": [AIMessage(content=response.content)]}

# Create StateGraph
builder = StateGraph(MessagesState)

# Add the customer support assistant node
builder.add_node("customer_support", customer_support_assistant)

# Flow Declaration
builder.add_edge(START, "customer_support")
builder.add_edge("customer_support", END)

# memory checkpointer
memory = MemorySaver()

# building graph with memory
customer_support_agent = builder.compile(checkpointer=memory)

print(": Customer support agent built successfully!")

# Helper function to run conversations
def run_customer_conversation(user_input: str, thread_id: str = "default_session"):
    """
    Send a message to the customer support agent and get response.
    """
    result = customer_support_agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": thread_id}}
    )
    
    # Human and AI message conversation flow
    for message in result["messages"]:
        if isinstance(message, HumanMessage):
            print(f"\n Customer: {message.content}")
        elif isinstance(message, AIMessage):
            print(f" Support: {message.content}")
    
    print("\n" + "="*70)
    return result


