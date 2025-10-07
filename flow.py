#!/usr/bin/env python
# coding: utf-8

# In[55]:


import os
from dotenv import load_dotenv
import requests
from typing import TypedDict
from typing_extensions import Annotated
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # Tracks all messages
    sentiment: str  # Stores sentiment of last user input
    paragraph: str  # Stores generated paragraph


# In[56]:


qlm = ChatGroq(model_name="openai/gpt-oss-120b")


# In[58]:


def sentiment_node(state: ChatState):

    messages = state["messages"]

    # Find last user input
    last_user_msg = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_user_msg = msg.content
            break
    if last_user_msg is None:
        raise ValueError("No user message found in state")

    # Prepare prompt for sentiment detection
    sentiment_prompt = f"""
    Classify the sentiment of the following text as Positive, Negative, or Neutral:
    "{last_user_msg}"
    Output only the sentiment label.
    """

    # Use ChatGroq LLaMA 3 model to detect sentiment
    detected_sentiment = qlm.invoke([HumanMessage(content=sentiment_prompt)]).content.strip()

    # Update state
    state["sentiment"] = detected_sentiment

    # Return in LangGraph node format
    return {"sentiment": detected_sentiment}


# In[60]:


gen_llm = ChatGroq(model_name="openai/gpt-oss-120b")


# In[61]:


def paragraph_node(state: ChatState):
    messages = state["messages"]
    sentiment = state["sentiment"]  # ✅ use the sentiment from previous node

    # Get the last user message (topic)
    last_user_msg = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_user_msg = msg.content
            break
    if last_user_msg is None:
        raise ValueError("No user message found in state")

    # Prompt for paragraph generation
    generation_prompt = f"""
    Write a detailed and coherent paragraph about the topic:
    "{last_user_msg}"
    The paragraph should reflect a {sentiment.lower()} tone.
    """

    # Use Mixtral (different LLM) to generate
    paragraph = gen_llm.invoke([HumanMessage(content=generation_prompt)]).content.strip()

    # Return updated state
    return {"paragraph": paragraph}


# In[62]:


from langgraph.graph import StateGraph, END,START

graph = StateGraph(ChatState)

# 2️⃣ Add nodes (these are your defined functions)
graph.add_node("sentiment_node", sentiment_node)
graph.add_node("paragraph_node", paragraph_node)


# In[63]:


graph.add_edge(START, "sentiment_node")
graph.add_edge("sentiment_node", "paragraph_node")
graph.add_edge("paragraph_node", END)

# 4️⃣ Compile graph
app = graph.compile()


# In[64]:




# In[41]:




