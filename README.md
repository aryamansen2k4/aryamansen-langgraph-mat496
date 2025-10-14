This github repository is basically a collection of learnings and codes that I have gather and made while following the Introduction to Langgraph course by Langchain.

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



