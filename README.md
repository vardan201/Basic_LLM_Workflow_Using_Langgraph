AI Paragraph Generator with Sentiment Analysis

A powerful AI-powered web application that allows users to generate detailed paragraphs based on their input, while automatically detecting the sentiment (Positive, Negative, Neutral) of the prompt. This project demonstrates the combination of LangGraph, Groq LLM, and Flask to build an end-to-end workflow for text generation tasks.

🚀 Features

Sentiment Detection: Automatically classifies user prompts as Positive, Negative, or Neutral using Groq LLM.

Paragraph Generation: Generates coherent, detailed paragraphs reflecting the detected sentiment.

Stateful Conversation: Tracks user inputs and AI responses to maintain context.

Web Interface: Beautiful and interactive Flask-based UI for easy user input and output visualization.

Flexible Architecture: Separate nodes for sentiment detection and paragraph generation, making it easy to extend or modify the workflow.

Extensible: Easily integrate other LLMs for different tasks (like summarization, Q&A, or content generation).

📦 Tech Stack

Python 3.13 – Core programming language.

Flask – Web framework for creating the user interface and API.

LangGraph – Workflow orchestration to manage stateful AI pipelines.

Groq LLM (ChatGroq / Mixtral) – LLMs for sentiment detection and paragraph generation.

dotenv – Securely load API keys from .env file.

HTML / CSS / JS – Clean and responsive UI.

🛠 Installation

Clone the repository

git clone https://github.com/vardan201/Basic_LLM_Workflow_Using_Langgraph.git
cd Basic_LLM_Workflow_Using_Langgraph


Create a virtual environment

python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows


Install dependencies

pip install -r requirements.txt


Setup environment variables
Create a .env file in the root folder:

GROQ_API_KEY=your_groq_api_key_here

⚙ Usage
1️⃣ Run the Flask app
python interface.py


The app will be available at: http://127.0.0.1:8000/

2️⃣ Using the Web Interface

Type your prompt in the text box (e.g., "Talk about hope after loss").

Click Generate.

The app will display:

Sentiment: Positive, Negative, or Neutral.

Paragraph: AI-generated text reflecting the sentiment.

3️⃣ Using API (POST Request)
POST http://127.0.0.1:8000/generate
Content-Type: application/json

{
  "prompt": "Talk about hope after loss"
}


Response

{
  "sentiment": "Positive",
  "paragraph": "AI-generated paragraph here..."
}

🏗 Project Structure
Basic_LLM_Workflow_Using_Langgraph/
│
├── flow.ipynb          # Main workflow notebook with LangGraph nodes
├── flow.py             # Compiled LangGraph workflow
├── interface.py        # Flask app for web interface
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── .env                # Stores Groq API key

🧠 Workflow Architecture

ChatState Node

Tracks all user messages and AI responses.

Stores the last sentiment and paragraph.

Sentiment Node

Extracts the last user input.

Uses Groq LLM (ChatGroq) to classify sentiment.

Updates chat_state["sentiment"].

Paragraph Node

Uses another LLM (Mixtral) to generate a paragraph.

The paragraph reflects the detected sentiment.

Updates chat_state["paragraph"].

Flask Interface

Takes user input via a web page.

Invokes the compiled LangGraph workflow.

Returns sentiment and paragraph dynamically.
