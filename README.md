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

## Lesson 6: Agent
In this previous lesson we built a router where:

1) Our chat model will decide to make a tool call or not based upon the user input.
2) We use a conditional edge to route to a node that will call our tool or simply end

In this lesson, we extended this router to a *generic agent architecture*.
We did this by simply passing the ```ToolMessage``` back to the model itself.
Hence we can either:

1) call another tool or
2) respond directly.

This is the intuition/idea behind ReAct, which is a general agent architecture.
Below are some terms we learnt.

1) ```act```: let the model call specific tools
2) ```observe```: pass the tool output back to the model
3) ```reason```: let the model reason about the tool output to decide what to do next

In the notebook ```agent.ipynb```, we made an agent having all the basic arithmetic tools (addition, subtraction, multiplication and division). We went to our project in LangSmith UI and analysed the traces of this agent.

## Lesson 7: Agent with Memory
In this lesson, we simply extend our agent (made in the previous lesson) by introducing *memory*.

**Problem**: When a new invokation is being done by the graph, it doesn't remember the result of the previous invokation. Hence if we want to use the result from the previous invokation, we have to write it ourselves

**Solution**: Use memory checkpointers like ```MemorySaver``` to save the graph state after each step and this gives the agent memory.

In the notebook ```agentmemory.ipynb```, I used the agent as in the previous lesson except I used new invokations so to show that each time the memory saves the result and then uses it in the new invokation.
We analyse the same result in LangSmith UI. Note that in LangSmith UI we used the code without ```MemorySaver``` because LangSmith UI is backed up by LangGraph which by default uses memory, hence checkpoints like ```MemorySaver``` is not needed.

# Module 2: State and Memory
In this module we learnt about the concept of memory and to add persistence to our graph.

Memory is important as memory is a central component in building agentic application with a high quality user experience, because users expect the agent to recal previous interactions.

## Lesson 1: State Schema
In this lesson we learnt about state and memory more in depth.

**State Schema**: Represents the structure and types of data that our graph will use. All nodes in the graph are expected to communicate with that schema.

We used ```TypedDict``` which is a dictionary subclass from Python's library. It allows us to specify the keys and their corresponding value types. They can be used by IDEs to catch potential type-related errors before the code is run. However they are not enforced at run time.

**Dataclasses**: Dataclasses offer a concise syntax for creating classes that are primarily used to store data. Python's dataclasses provide another way to define structured data.

Since they dont enforce types at runtime, we could potentially assign invalid values without raising an error which is a problem.

*Solution*: **Pydantic**

**Pydantic**: It is a data validation and settings management library using Python type annotations. Pydantic can perform validation to check whether data conforms to the specified types and constraints at runtime.

In the notebook ```stateschema.ipynb```, we have demonstrated each concept using a simple situation where a user has either won, lost, or drawn a game.

## Lesson 2: State Reducers
In this lesson, we learnt about reducers.

By default, LangGraph does not know the preferred way to update the state, hence it will just overwrite the value of a variable in node. 

In *Cell 4* we have an invalid update error as Node 2 and Node 3 are running parallely and in both cases the variable ```foo``` is getting incremented by 2. This leads to ambiguity as both attempt to overwrite the state within the same step. So which state should it keep?

*Solution*: **Reducers**
**Reducers**: Specify how the state updates are performed on specific keys/channels in the state schema.
Eg: ```operator.add```

We can even have certain cases where the input value is invalid given the current reducer. This motivates the need to use *Custom Reducers* sometimes

In the notebook ```statereducers.ipynb```, we demonstrated the workings of Reducers and Custom Reducers as well ```MessagesStates``` from LangGraph.

## Lesson 3: Multiple Schemas
In this lesson, we learn a few ways to customize graphs with multiple schemas.

Normally, all graph nodes communicate with a single schema which contains the graph's input and output keys/channels.
However there are cases where we need a bit more control:

1) Internal nodes may pass information that is not required in the graph's input / output.

2) We may also want to use different input / output schemas for the graph. The output might, for example, only contain a single relevant output key.

By default, ```StateGraph``` takes in a single schema and all nodes are expected to communicate with that schema.
However, it is also possible to define explicit input and output schemas for a graph.

In most of the cases we define an *internal* schema that contains all keys relevant to graph operations.
In addition, we can use a type hint state: ```InputState``` to specify the input schema of each of our nodes.

In the notebook ```multipleschemas.ipynb```, we demonstrated the concept of multiple schemas by using ```InputState```, ```OutputState``` and ```OverallState```. 

## Lesson 4: Trim and Filters Messages
In this lesson, we learn about more ways to work with messages in graph state.

A practical issue in working with messages is managing long running conversations and being very token intensive.
We have a few ways to address this:

1) ```RemoveMessage``` & ```add_messages``` reducer: Delete message based on their id from message queue. Very nice and simpley way. *(Cell 7 & 8)*

2) **Filtering Messages**: Instead of modifying the graph state, we can just filter the messages we pass to the chat model. *(Cell 9, 10, 11 & 12)*

3) **Trim Messages**: We can also trim the messages based on a set number of tokens. This restricts the message history to a specified number of tokens. While filtering only returns a post-hoc subset of the messages between agents, trimming restricts the number of tokens that a chat model can use to respond. *(Cell 13, 14, 15 & 16)*

In the notebook ```trimfiltermessages.ipynb``` we demonstrated the above methods used to have long running conversations with thet chatbot.

## Lesson 5: Chatbot with message summarization
In this lesson, we lear how to use LLM's to produce a running summary of the conversation.
This helps us in getting a brief yet precise representation of the full conversation, rather than just removing it with ```trimming``` or ```filtering```.

In the notebook ```chatbotsummarization.ipynb```, we demonstrated this incorporation of summarisation into a simple Chatbot. We also equipped the Chatbot with memory, supporting long-running conversations without incurring high token cost / latency. 
We did by working with ```MemorySaver```,  an in-memory key-value store for Graph state, which is used as a checkpoint to automatically save the graph state after each step. The checkpointer saves the state at each step as a checkpoint. These saved checkpoints can be grouped into a ```thread``` of conversation.

## Lesson 6: Chatbot with Message Summarization & External DB Memory
In this lesson, we learnt some more advanced checkpoints that supports external databases, like **Sqlite**.

**Sqlite**: It is a small, fast, highly popular SQL database. If we supply ```:memory:``` it creates an in-memory Sqlite database. But, if we supply a db path, then it will create a database for us.

One main advantage of **sqlite** is that the state is persisted. 
So suppose if we re-start the notebook kernel, we can still load from Sqlite DB on disk.

In the notebook ```chatbotexternalmemmory.ipynb```, we demonstrated a chatbot using **sqlite**.

# Module 3: UX and Human-in-the-Loops
Some workflows need to "off-load" a certain task to a human and then later allow the agent to pick up from where the human left off.
In this module we got introduced to the concept of ```breakpoints```, which stop our graph at specific steps in the workflow- and once stopped, we learnt how it can accomplish a variety of tasks. We also demonstrated how to update the graph state with user input.

## Lesson 1: Streaming
In this lesson we learnt about **streaming**.
In Langgraph, there are two general ways to stream our graph state:

1) ```.stream```: Sync methods for streaming back results.
2) ```.astream```: Async methods for streaming back results.

But there are also different streaming modes for graph state:

1) ```values```: This streams the full state of the graph after each node is called.
2) ```updates```: This streams updates to the state of the graph after each node is called.

Sometimes, we want to stream more than graph state, like commonly tokens are also streamed during chat model calls as they are generated. 
This can be achieved by using the ```.astream_events``` methods, which streams back events as they happen inside the nodes.

Each event is a dict with a few keys:
1) ```event```: This is the type of event that is being emitted.
2) ```name```: This is the name of event.
3) ```data```: This is the data associated with the event.
4) ```metadata```: Containslanggraph_node, the node emitting the event.

We can even use ```event['metadata']['langgraph_node']``` to select the node to stream from, as well as use ```event['data']``` to get the actual data for each event. 
To just get the ```AIMessageChunk```, we use the ```chunk``` key.

In the notebook ```streaminginterruption.ipynb``` we demonstrated the different ways and modes to stream as well as streaming tokens and other meta-data.

## Lesson 2: Breakpoints
In this lesson, we learnt about **breakpoints**, which is a simple way to stop the graph at specific steps. This helps us in enabling user ```approval``.

In the notebook ```breakpoints.ipynb```, we used to breakpoints to approve the agent to use any of its tools.
We compiled the graph with ```interrupt_before=["tools"]``` where ```tools``` is our tools node. This means that the execution will be interrupted before the node ```tools```, which executes the tool call.

## Lesson 3: Editing State and Human Feedback
In this lesson, we learnt to how to actually the edit the graph state once it stopped.
```breakpoints``` are used to wait for user approval, but they also provide the opportunity to **modify the graph state*.

In the notebook ```editstatehumanfeedback.ipynb``` we demonstrated how to modify the graph state once ```breakpoints``` are used by applying a state update using ```update_state``` with a new message. The ```add_messages``` reducer appends it to our state key, ```messages```. We then further edit our agent state so to allow for human feedback to perform this state update, by using a node that **serves as a placeholder for human feedback** within our agent. The ```human_feedback``` node allow the user to add feedback directly to state. We then specify the breakpoint using ```interrupt_before``` our ```human_feedback``` node.

## Lesson 4: Dynamic Breakpoints
In the previous lessons, we discussed the following things which act as motivations for human-in-the-loop:

1) **Approval** - We can interrupt our agent, surface state to a user, and allow the user to accept an action.

(2) **Debugging** - We can rewind the graph to reproduce or avoid issues.

(3) **Editing** - We can modify the state.

We also covered ```breakpoints``` as a general way to stop the graph at specific steps, which enables use-cases like ```Approval```.

But sometimes, it is helpful to allow the graph **dynamically** interrupt** itself.  This is an *internal* breakpoint and can be achieved using ```NodeInterrupt```.
Few specific benifits of it are:

(1) you can do it conditionally, i.e, from inside a node based on developer-defined logic.

(2) you can communicate to the user why its interrupted by passing whatever you want to the ```NodeInterrupt```.

In the notebook ```dynamicbreakpoints.ipynb```, we demonstrated the dynamic breakpoint by creating a graph where a ```NodeInterrupt``` is thrown when a input of length more than 3 characters are is received.

