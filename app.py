from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


def analyze_email(email):
    text = email.lower()

    # -----------------------------
    # Priority Detection
    # -----------------------------
    high_words = [
        "urgent", "immediately", "asap", "deadline",
        "important", "emergency", "today", "tomorrow"
    ]

    medium_words = [
        "please", "meeting", "reminder", "submit",
        "response", "confirm"
    ]

    if any(word in text for word in high_words):
        priority = "High"
    elif any(word in text for word in medium_words):
        priority = "Medium"
    else:
        priority = "Low"

    # -----------------------------
    # Category Detection
    # -----------------------------
    if any(word in text for word in
           ["exam", "college", "student", "assignment", "project", "class"]):
        category = "Education"

    elif any(word in text for word in
             ["meeting", "office", "work", "project", "employee", "client"]):
        category = "Work"

    elif any(word in text for word in
             ["payment", "invoice", "bank", "transaction", "salary"]):
        category = "Finance"

    elif any(word in text for word in
             ["offer", "discount", "sale", "promotion"]):
        category = "Promotion"

    else:
        category = "Personal"

    # -----------------------------
    # Spam / Phishing Detection
    # -----------------------------
    spam_words = [
        "click here", "verify your account",
        "password", "winner", "lottery",
        "claim prize", "urgent payment"
    ]

    spam_count = sum(word in text for word in spam_words)

    if spam_count >= 2:
        spam_risk = "High"
    elif spam_count == 1:
        spam_risk = "Medium"
    else:
        spam_risk = "Low"

    # -----------------------------
    # Sentiment Detection
    # -----------------------------
    positive_words = [
        "thank", "thanks", "great", "excellent",
        "happy", "congratulations"
    ]

    negative_words = [
        "problem", "issue", "angry", "delay",
        "failed", "complaint"
    ]

    positive = sum(word in text for word in positive_words)
    negative = sum(word in text for word in negative_words)

    if positive > negative:
        sentiment = "Positive"
    elif negative > positive:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # -----------------------------
    # Task Extraction
    # -----------------------------
    tasks = []

    task_patterns = [
        r"please (.*?)(?:\.|$)",
        r"submit (.*?)(?:\.|$)",
        r"complete (.*?)(?:\.|$)",
        r"send (.*?)(?:\.|$)",
        r"confirm (.*?)(?:\.|$)"
    ]

    for pattern in task_patterns:
        matches = re.findall(pattern, email, re.IGNORECASE)

        for match in matches:
            task = match.strip()

            if task and task not in tasks:
                tasks.append(task)

    if not tasks:
        tasks.append("No specific task detected")

    # -----------------------------
    # Deadline Extraction
    # -----------------------------
    deadline_patterns = [
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\b",
        r"\b(?:today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    ]

    deadlines = []

    for pattern in deadline_patterns:
        matches = re.findall(pattern, email, re.IGNORECASE)

        for match in matches:
            if match not in deadlines:
                deadlines.append(match)

    if not deadlines:
        deadlines.append("No deadline detected")

    # -----------------------------
    # Summary
    # -----------------------------
    sentences = re.split(r'(?<=[.!?])\s+', email.strip())

    if len(sentences) <= 2:
        summary = email.strip()
    else:
        summary = " ".join(sentences[:2])

    # -----------------------------
    # Priority Explanation
    # -----------------------------
    if priority == "High":
        priority_reason = "The email contains urgent or deadline-related information."

    elif priority == "Medium":
        priority_reason = "The email requires attention or a response."

    else:
        priority_reason = "The email does not appear to require immediate action."

    # -----------------------------
    # Smart Reply
    # -----------------------------
    reply = (
        "Dear Sir/Madam,\n\n"
        "Thank you for your email. I have reviewed the information "
        "and will take the necessary action accordingly.\n\n"
        "Best regards"
    )

    return {
        "summary": summary,
        "priority": priority,
        "priority_reason": priority_reason,
        "category": category,
        "tasks": tasks,
        "deadlines": deadlines,
        "spam_risk": spam_risk,
        "sentiment": sentiment,
        "reply": reply
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    email = data.get("email", "").strip()

    if not email:
        return jsonify({
            "error": "Please enter an email."
        }), 400

    result = analyze_email(email)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
