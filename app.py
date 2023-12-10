from Chatbot import Chatbot
from VectorStore import VectorStore
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

vectorstore = VectorStore()
chatbot = Chatbot()

chatbot.create_conversation_chain(vectorstore.get_vectorstore())


@app.route('/forgot-password', methods=["POST"])
def forgot_password():
    pass


@app.route('/register', methods=["POST"])
def register():
    pass


@app.route('/login', methods=["POST"])
def login():
    pass


@app.route('/chat', methods=["POST"])
def chat():
    try:
        # Extract the message from the request body
        data = request.get_json()
        user_question = data.get('content')

        # Handle the user input with the vector store and chatbot
        if user_question:
            response = chatbot.handle_user_input(user_question)

            # Return the AI response to the user
            return jsonify({"status": "Success", "message": response})
        else:
            return jsonify({"status": "failure", "error": "Missing 'message' parameter in the request body"})

    except Exception as e:
        print(e, 'error')
        return jsonify({"status": "failure", "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
