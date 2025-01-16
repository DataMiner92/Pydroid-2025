from flask import Flask, render_template_string, request, jsonify
from googletrans import Translator

# Flask app
app = Flask(__name__)

# Translator for multi-language support
translator = Translator()

# Chatbot logic
menstrual_info = {
    "ovulation": "Ovulation is when a mature egg is released from the ovary...",
    "safe days": "Safe days refer to the period in your menstrual cycle when...",
    "PMS": "Premenstrual Syndrome (PMS) includes symptoms like mood swings, cravings, etc.",
    "cramps": "Menstrual cramps are throbbing or cramping pains in the lower abdomen...",
}

def translate_response(response, target_language):
    try:
        translated = translator.translate(response, dest=target_language)
        return translated.text
    except Exception:
        return "Translation failed."

def chatbot_response(user_input, language="en"):
    prompts = {
        "greeting": "Hello! What do you want to learn today?",
        "specific_info": "What specific information do you want to know? E.g., ovulation, safe days, etc.",
    }

    if user_input.lower() in ["hi", "hello", "hey"]:
        response = prompts["greeting"]
    elif user_input.lower() in menstrual_info:
        response = menstrual_info[user_input.lower()]
    else:
        response = prompts["specific_info"]

    if language != "en":
        response = translate_response(response, language)

    return response

# Routes
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Menstrual Health Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .chat-container {
                width: 400px;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
                display: flex;
                flex-direction: column;
            }
            #chat-window {
                flex-grow: 1;
                height: 300px;
                overflow-y: auto;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                padding: 10px;
                background-color: #f9f9f9;
            }
            .input-container {
                display: flex;
            }
            #user-input {
                flex-grow: 1;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-right: 10px;
            }
            #send-btn {
                padding: 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            #language-select {
                margin-top: 10px;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>Menstrual Health Chatbot</h1>
            <div id="chat-window"></div>
            <div class="input-container">
                <input id="user-input" type="text" placeholder="Type your question...">
                <button id="send-btn">Send</button>
            </div>
            <select id="language-select">
                <option value="en">English</option>
                <option value="fr">French</option>
                <option value="es">Spanish</option>
            </select>
        </div>
        <script>
            document.getElementById("send-btn").addEventListener("click", function() {
                const userInput = document.getElementById("user-input").value;
                const language = document.getElementById("language-select").value;

                if (userInput.trim() === "") return;

                const chatWindow = document.getElementById("chat-window");
                const userMessage = `<div><strong>You:</strong> ${userInput}</div>`;
                chatWindow.innerHTML += userMessage;

                fetch("/get_response", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: userInput, language: language }),
                })
                .then(response => response.json())
                .then(data => {
                    const botMessage = `<div><strong>Bot:</strong> ${data.response}</div>`;
                    chatWindow.innerHTML += botMessage;
                    document.getElementById("user-input").value = "";
                })
                .catch(console.error);
            });
        </script>
    </body>
    </html>
    """)

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    user_input = data.get("message", "")
    language = data.get("language", "en")
    response = chatbot_response(user_input, language)
    return jsonify({"response": response})

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)