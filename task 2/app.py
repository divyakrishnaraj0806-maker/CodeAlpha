from flask import Flask, render_template, request, jsonify
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

app = Flask(__name__)

# Load FAQs
with open("faqs.json", "r") as f:
    faqs = json.load(f)

faq_questions = [faq["question"] for faq in faqs]
faq_answers = [faq["answer"] for faq in faqs]

# Preprocess + Vectorize
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(faq_questions)


def chatbot_answer(user_input):
    user_tfidf = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_tfidf, tfidf_matrix)
    index = similarity.argmax()
    
    if similarity[0][index] < 0.3:  
        return "Sorry, I couldn't understand your question."

    return faq_answers[index]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def get_bot_response():
    data = request.get_json()
    user_msg = data["message"]
    bot_reply = chatbot_answer(user_msg)
    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
