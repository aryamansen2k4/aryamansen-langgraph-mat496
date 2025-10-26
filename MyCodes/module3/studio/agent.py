import os, ssl, certifi
os.environ["USER_AGENT"] = f"rag-app/{1.0}"
#os.environ["OPENAI_API_KEY"]="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"
os.environ["GROQ_API_KEY"]="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"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "langsmith-academy"
os.environ["LANGCHAIN_HUB_NO_VERIFY_SSL"] = "true"
os.environ["SSL_CERT_FILE"] = certifi.where()
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq 

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

# --- Define arithmetic tools ---
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

def divide(a: int, b: int) -> float:
    """Divides a and b."""
    return a / b

tools = [add, multiply, divide]

llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")  
llm_with_tools = llm.bind_tools(tools)

# --- System message ---
sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)

# --- Assistant node ---
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# --- Build LangGraph ---
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

print("✅ LangGraph with Groq LLM compiled successfully.")