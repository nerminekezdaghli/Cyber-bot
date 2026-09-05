from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

# Charger les variables du fichier .env
load_dotenv()

# Récupérer la clé API
API_KEY = os.getenv("GEMINI_API_KEY")

# Vérifier que la clé existe
if not API_KEY:
    raise ValueError("GEMINI_API_KEY n'est pas définie dans le fichier .env")

# Initialiser Gemini
client = genai.Client(api_key=API_KEY)

# Créer l'application Flask
app = Flask(__name__)


# Page principale
@app.route("/")
def home():
    return render_template("index.html")


# API du chatbot
@app.route("/chat", methods=["POST"])
def chat():

    try:
        # Récupérer le message envoyé par l'utilisateur
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "")
        if not isinstance(user_message, str):
            return jsonify({
                "response": "Le message doit être du texte."
            }), 400
        user_message = user_message.strip()

        if not user_message:
            return jsonify({
                "response": "Veuillez écrire un message 😊"
            })

        # Instructions de Cyber-Bot
        system_prompt = """
You are Cyber-Bot 🤖, a friendly and intelligent public AI assistant.

Your mission is to help users with:
- Everyday life
- Technology
- Programming
- Artificial Intelligence
- Electronics
- Electrical Engineering
- Science
- Education
- Movies and entertainment
- Gaming
- Productivity
- General knowledge

Rules:
- Be friendly, helpful and respectful.
- Answer clearly and simply.
- Adapt your explanation to the user's level.
- Help beginners step by step.
- For programming questions, provide clean and understandable code.
- Do not invent information.
- If you are unsure, say so.
- Answer in the same language as the user.
- You can communicate in English, French, Arabic and Tunisian Arabic (Derja).
- Use emojis when appropriate.

You are Cyber-Bot 🤖⚡
Your goal is to be a useful everyday AI assistant.
"""

        # Envoyer le message à Gemini
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=system_prompt + "\n\nUser message:\n" + user_message
        )

        # Récupérer la réponse
        bot_response = (response.text or "").strip()
        if not bot_response:
            raise RuntimeError("Gemini returned an empty response")

        return jsonify({
            "response": bot_response
        })

    except Exception as e:

        print("Erreur :", e)

        return jsonify({
            "response": "Désolé 😕 Une erreur s'est produite. Vérifie ta clé API et ta connexion."
        }), 500


# Lancer le serveur
if __name__ == "__main__":
    app.run(debug=False)