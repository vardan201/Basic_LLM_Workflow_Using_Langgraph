from flask import Flask, request, jsonify, render_template_string
from flow import app as langgraph_app, ChatState
from langchain.schema import HumanMessage

flask_app = Flask(__name__)

# HTML template with a prompt box and results area
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Paragraph Generator</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7fc; font-family: 'Segoe UI', sans-serif; padding-top: 50px; }
        .container { max-width: 800px; }
        textarea { width: 100%; height: 120px; resize: none; padding: 10px; border-radius: 8px; border: 1px solid #ccc; }
        button { margin-top: 10px; }
        .result { margin-top: 20px; padding: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        #loading { display: none; }
    </style>
</head>
<body>
<div class="container">
    <h1 class="text-center mb-4">AI Paragraph Generator</h1>
    
    <div class="mb-3">
        <textarea id="prompt" placeholder="Type your prompt here..."></textarea>
    </div>
    <button class="btn btn-primary" onclick="generate()">Generate</button>
    
    <div id="loading" class="mt-3 text-center">
        <div class="spinner-border text-primary" role="status"></div>
        <p>Generating paragraph...</p>
    </div>

    <div class="result" id="result" style="display:none;">
        <h5>Sentiment: <span id="sentiment"></span></h5>
        <hr>
        <h5>Generated Paragraph:</h5>
        <p id="paragraph"></p>
    </div>
</div>

<script>
async function generate() {
    const prompt = document.getElementById("prompt").value;
    if (!prompt.trim()) {
        alert("Please enter a prompt.");
        return;
    }

    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";

    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });

    const data = await response.json();

    document.getElementById("sentiment").textContent = data.sentiment;
    document.getElementById("paragraph").textContent = data.paragraph;

    document.getElementById("loading").style.display = "none";
    document.getElementById("result").style.display = "block";
}
</script>

<!-- Bootstrap JS Bundle -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@flask_app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@flask_app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_prompt = data.get("prompt", "")

    chat_state: ChatState = {
        "messages": [HumanMessage(content=user_prompt)],
        "sentiment": "",
        "paragraph": ""
    }

    # Invoke your LangGraph workflow
    result = langgraph_app.invoke(chat_state, output_keys=["sentiment", "paragraph"])

    return jsonify(result)


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8000, debug=True)
