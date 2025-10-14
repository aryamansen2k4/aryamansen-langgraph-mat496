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

from langchain_groq import ChatGroq 
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Tool
def add(a: int, b: int) -> int:
    """Add a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm = ChatGroq(model="openai/gpt-oss-20b")
llm_with_tools = llm.bind_tools([add, multiply])

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([add, multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()