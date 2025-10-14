This github repository is basically a collection of learnings and codes that I have gather and made while following the Introduction to Langgraph course by Langchain. 
**All codes in the subsequent modules and lessons are modified codes done by me.**



# Module 1: Introduction
In this module, we will dive into *agents*.
We dwelve about what agents are, be introduced to several agent architectures and common challenges faced by developers when building agents.

## Lesson 1: Motivation
A "solitary" LLM is fairly limited as it doesnt have access to tools, external context i.e. documentation and cannot alone perform multi-step workflows. Hence many LLM use a control flow *(termed as **Chain**)* with step before/after LLM call, like tool calls, retrieval, etc.

Advantage of Chain: Very reliable. So same flow steps occur everytime the chain is invoked.

However, we do want LLMs to pick their own control flow/chain for certain kinds of problems.

Enters the **"Agent"**.
Agent: A control flow defined by an LLM.

Different kinds of Agents:
1) Less Control (Router): LLM controls a single step in a flow, and may choose b/w a narrow set of options.
2) More Control (Fully Autonomous): Can pick any sequence of steps through set of given options, or can even generate its on steps that it can take.

However, as we go from less control to more control, the reliability drops.
This is where the motivation of using LangGraph comes as it allows us to use agents that maintain reliability.

## Lesson 2: Simple Graph
In this lesson, we built a simple graph, to introduce the core components of LangGraph. 

1) **Nodes**: Basically python functions. 
2) **Edges**: Simply used to connect the nodes.
3) **Normal Edge**: The connection/edge with between two nodes.
4) **Conditional Edges**: Used when we want to decide whether to go to one node or the other one.
5) **States**: The object that we pass between the nodes and edges of our graph.


In the notebook ```simplegraph.ipynb```, we built a graph with 4 simple nodes and one conditional edge which tells Mr. Gupta whether he won or lost the lottery.

## Lesson 3: LangSmith Studio
In this lesson, we visualised the same graph, that we built in ```simplegraph.ipynb```, in LangSmith Studio UI. We played with the graph, ran the graph from the UI and studied the behaviour using the UI as well. 
The UI provides a much cleaner look and helps in better understanding of the graph.

## Lesson 4: Chain
**Chains** combine 4 core concepts:

1) *Using Chat Messages*: Uses messages to capture different roles within a conversation.
2) *Using Chat Models*: Chat models can use a sequence of message as input and support message types.
3) *Binding Tools*: Use tools to give the model awareness of the required input schema.
4) *Executing Tool Calls*: The model will choose to call a tool based upon the natural language input from the user.

In the notebook ```chain.ipynb``` we demonstrated the given 4 core concepts, where at the very end we made a graph which invokes the tool method (addition and multiplication), whenever the user asks for such task, and will switch to general answers when not needed (in the notebook, I asked about Fifa World Cup 2026).

## Lesson 5: Router
In the previous lesson, we built a graph that uses ```messages``` as state and a chat model with bound tools.
The graph can:

1) Return a tool call
2) Return a natural language response 

This can be thought of as a simple **Router**, where the chat model routes between a direct response or a tool call based upon the user input.

In the notebook ```router.ipynb``` we extended the graph to work with either output:

1) Add a node that will call our tool (add, multiply).
2) Add a conditional edge that will look at the chat model output, and route to our tool calling node or simply end if no tool call is performed.

We even ran it in the LangSmith Studio UI, where we did the same experiment but we can see clearly how the traces were working.


