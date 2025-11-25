from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db = SQLAlchemy(app)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_msg = db.Column(db.String(500))
    bot_reply = db.Column(db.String(500))

with app.app_context():
    db.create_all()

model = pickle.load(open("model.pkl", "rb"))
vectorizer = model["vectorizer"]
X = model["X"]
answers = model["answers"]
questions = model["questions"]

def chatbot_response(user_text):
    user_vec = vectorizer.transform([user_text])
    similarity = cosine_similarity(user_vec, X)
    NAVEEN = similarity.argmax()
    return answers[NAVEEN]


# Routes
@app.route("/")
def NAVEEN():
    return render_template("NAVEEN.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data["message"]
    bot_reply = chatbot_response(user_msg)

    # Save chat to DB
    chat_entry = ChatHistory(user_msg=user_msg, bot_reply=bot_reply)
    db.session.add(chat_entry)
    db.session.commit()

    return jsonify({"response": bot_reply})


# URL Building + Variable Rule Example
@app.route("/history/<int:limit>")
def history(limit):
    chats = ChatHistory.query.limit(limit).all()
    output = [{"user": c.user_msg, "bot": c.bot_reply} for c in chats]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
