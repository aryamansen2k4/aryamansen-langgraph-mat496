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
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# LLM with bound tool
llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")  
llm_with_tools = llm.bind_tools([multiply])

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)

# Compile graph
graph = builder.compile()