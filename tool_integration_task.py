from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Literal
from duckduckgo_search import DDGS
import random
import os

print(" All libraries sucessfully imported")

# Load API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found! Please set it in your .env file.")

print(" API key loaded")

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,  # Temperature set to zero for more precise tool usage
    api_key=openai_api_key
)

print(f" LLM initialized: {llm.model_name}")

# Tool 1: Weather tool

@tool
def weather_checker(city: str) -> str:
    """
    Get the current weather for a given city.
    Use this tool when asked about weather conditions, temperature, or forecasts.
    
    Args:
        city: The name of the city to check weather for
        
    Returns:
        A simulated weather report including temperature, conditions, and humidity
        
    Examples:
"Lagos" returns weather for Lagos, Nigeria
"New York" returns weather for New York, USA
    """
    # weather data for different cities
    weather_data = {
        "lagos": {"temp": 28, "condition": "Partly Cloudy", "humidity": "78%"},
        "new york": {"temp": 15, "condition": "Sunny", "humidity": "45%"},
        "london": {"temp": 12, "condition": "Rainy", "humidity": "85%"},
        "tokyo": {"temp": 18, "condition": "Clear", "humidity": "60%"},
        "sydney": {"temp": 22, "condition": "Windy", "humidity": "65%"},
        "paris": {"temp": 14, "condition": "Cloudy", "humidity": "70%"},
        "dubai": {"temp": 32, "condition": "Sunny", "humidity": "40%"},
        "mumbai": {"temp": 30, "condition": "Humid", "humidity": "80%"},
    }
    
    city_lower = city.lower()
    
    # Get weather data or generate random for unknown cities
    if city_lower in weather_data:
        data = weather_data[city_lower]
    else:
        # Generate random weather for unknown cities
        data = {
            "temp": random.randint(10, 35),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Windy", "Clear"]),
            "humidity": f"{random.randint(30, 90)}%"
        }
    
    return f""":mostly_sunny: Weather Report for {city.title()}:
• Temperature: {data['temp']}°C
• Conditions: {data['condition']}
• Humidity: {data['humidity']}
• Forecast: Similar conditions expected tomorrow
"""

print(" Weather tool created")

# Tool 2: Dictionary tool 

@tool
def dictionary_lookup(word: str) -> str:
    """
    Look up the definition and usage of a word.
    Use this tool when asked about word meanings, definitions, or vocabulary.
    
    Args:
        word: The word to look up
        
    Returns:
        Definition, part of speech, and example sentences
        
    Examples:
"ephemeral" returns definition and usage
"serendipity" returns definition and examples
    """
    # Simulated dictionary database
    dictionary = {
        "ephemeral": {
            "definition": "Lasting for a very short time",
            "part_of_speech": "adjective",
            "examples": ["The ephemeral beauty of cherry blossoms", "His fame was ephemeral"]
        },
        "serendipity": {
            "definition": "The occurrence of events by chance in a happy or beneficial way",
            "part_of_speech": "noun",
            "examples": ["Finding that book was pure serendipity", "Serendipity led to their meeting"]
        },
        "ubiquitous": {
            "definition": "Present, appearing, or found everywhere",
            "part_of_speech": "adjective",
            "examples": ["Mobile phones are now ubiquitous", "The ubiquitous presence of advertising"]
        },
        "eloquent": {
            "definition": "Fluent or persuasive in speaking or writing",
            "part_of_speech": "adjective",
            "examples": ["An eloquent speaker", "Her eloquent description moved everyone"]
        },
        "resilient": {
            "definition": "Able to withstand or recover quickly from difficult conditions",
            "part_of_speech": "adjective",
            "examples": ["Children are remarkably resilient", "A resilient economy"]
        },
        "paradigm": {
            "definition": "A typical example or pattern of something; a model",
            "part_of_speech": "noun",
            "examples": ["A new paradigm in physics", "Shifting paradigms in education"]
        }
    }
    
    word_lower = word.lower()
    
    if word_lower in dictionary:
        data = dictionary[word_lower]
        return f""":books: Dictionary Entry for '{word}':
        
Definition: {data['definition']}
Part of Speech: {data['part_of_speech'].upper()}

Example Sentences:
{data['examples'][0]}
{data['examples'][1]}

Synonyms: Use a thesaurus for related words.
"""
    else:
        # For words not in the dictionary
        return f""":books: Dictionary Entry for '{word}':
        
Word not found in the dictionary. 
For comprehensive definitions, try:
• Oxford English Dictionary
• Merriam-Webster
• Cambridge Dictionary

Tip: The word '{word}' might be:
Very new or slang
Misspelled
A technical term
"""

print("Dictionary tool created")

# Tool 3: Web search tool 
@tool
def web_search(query: str, max_results: int = 3) -> str:
    """
    Search the web for current information using DuckDuckGo.
    Use this tool when asked about recent news, current events, or up-to-date information.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        Concise search results with summaries
        
    Examples:
"latest AI news" returns recent AI developments
"Python 3.12 features" returns information about Python updates
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            
            if not results:
                return f"No results found for '{query}'. Try different keywords."
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                snippet = result.get('body', 'No description available')
                snippet = snippet[:200] + "..." if len(snippet) > 200 else snippet
                
                formatted_results.append(
                    f"{i}. {title}\n   :memo: {snippet}\n"
                )
            
            return f""" Web Search Results for: "{query}"
    
{''.join(formatted_results)}
Found {len(results)} relevant results.
"""
    except Exception as e:
        return f":warning: Search error: {str(e)}\nPlease try again or rephrase your query."

print(" Web search tool created")

# Testing tools directly 
print("\n Testing tools directly:")

# weather tool
weather_result = weather_checker.invoke({"city": "Lagos"})
print(f"Weather Tool Test:\n{weather_result[:100]}...")

# dictionary tool
dict_result = dictionary_lookup.invoke({"word": "ephemeral"})
print(f"\nDictionary Tool Test:\n{dict_result[:100]}...")

# web search tool 
try:
    search_result = web_search.invoke({"query": "latest AI developments 2024", "max_results": 2})
    print(f"\nWeb Search Tool Test:\n{search_result[:150]}...")
except Exception as e:
    print(f"\nWeb Search Tool Test (simulated): Showing tool works - {str(e)[:50]}...")

# Building agent..

tools = [weather_checker, dictionary_lookup, web_search]
llm_with_tools = llm.bind_tools(tools)
print(f"\n LLM bound to {len(tools)} tools: {[t.name for t in tools]}")

# System prompt
sys_msg = SystemMessage(content="""You are a versatile assistant with access to multiple tools.

Use tools when appropriate:
Weather Checker: For weather queries, temperature, forecasts
Dictionary Lookup: For word definitions, meanings, vocabulary
Web Search: For current events, news, recent information, or when you need up-to-date facts

Guidelines:
Only use tools when necessary
For simple questions or general knowledge, answer directly
If user asks about a word meaning AND wants recent examples, you might need to use both dictionary and web search
Be concise but helpful
Always acknowledge when you're using a tool
""")

# Assistant node
def assistant(state: MessagesState) -> dict:
    """
    Assistant node - decides whether to use tools or answer directly.
    """
    messages = [sys_msg] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Conditional routing function
def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    """
    Decide next step based on last message.
    """
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "tools"
    
    return "__end__"

# Building with  graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    should_continue,
    {"tools": "tools", "__end__": END}
)
builder.add_edge("tools", "assistant") 

# memory saver
memory = MemorySaver()
agent = builder.compile(checkpointer=memory)

print(" Multi-tool agent compiled successfully!")

# Visualize the graph
# try:
#     display(Image(agent.get_graph().draw_mermaid_png()))
# except Exception as e:
#     print(f"Graph structure: START → assistant → [conditional] → tools → assistant → END")
#     print(f"(Visualization error: {e})")

# Helper function
def run_multi_tool_agent(user_input: str, thread_id: str = "multi_tool_test", verbose: bool = True):
    """
    Run the agent and display the conversation.
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f" User: {user_input}")
        print(f"{'='*70}")
    
    result = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": thread_id}}
    )
    
    if verbose:
        for message in result["messages"]:
            if isinstance(message, HumanMessage):
                continue 
            elif isinstance(message, AIMessage):
                if message.tool_calls:
                    tool_names = [tc['name'] for tc in message.tool_calls]
                    print(f" Agent: [Calling tools: {', '.join(tool_names)}]")
                else:
                    print(f" Agent: {message.content}")
            elif isinstance(message, ToolMessage):
                content_preview = message.content[:120] + "..." if len(message.content) > 120 else message.content
                print(f" {content_preview}")
    
    if verbose:
        print(f"{'='*70}\n")
    
    return result

print("Agent ready for testing!")


# Interactive chat
def interactive_multi_tool_chat():
    """
    Live chat with your multi-tool agent.
    """
    print("\n" + "="*60)
    print("  MULTI-TOOL ASSISTANT - INTERACTIVE MODE")
    print("="*60)
    print("Try these types of queries:")
    print("• 'Weather in [city]'")
    print("• 'Define [word]'")
    print("• 'Search for [topic]'")
    print("• General questions (no tools)")
    print("Commands: /new (new session), /thread (show ID), /exit")
    print("="*70 + "\n")
    
    thread_id = "interactive_session"
    session_num = 1
    
    while True:
        try:
            user_input = input(f"[Session {session_num}]  You: ").strip()
        except KeyboardInterrupt:
            print("\n\n Session ended!")
            break
        
        if user_input.lower() == "/exit":
            print("\n: Goodbye!")
            break
        elif user_input.lower() == "/new":
            session_num += 1
            thread_id = f"session_{session_num}"
            print(f" New session: {thread_id}")
            continue
        elif user_input.lower() == "/thread":
            print(f" Thread ID: {thread_id}")
            continue
        elif user_input == "":
            continue
        
        # Running agent 
        print(": Thinking...")
        result = agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": thread_id}}
        )
        
        #results 
        print("\n" + "-"*50)
        
        tool_used = False
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                if msg.tool_calls:
                    tool_used = True
                    for tc in msg.tool_calls:
                        print(f" Called tool: {tc['name']}")
                elif msg.content:
                    print(f": {msg.content}")
            elif isinstance(msg, ToolMessage):
                print(f" Tool result: {msg.content[:100]}...")
        
        if tool_used:
            print(f"\n Decision: Used tools")
        else:
            print(f"\n Decision: Answered directly")
        
        print("-"*50 + "\n")

if __name__ == "__main__":
    interactive_multi_tool_chat()