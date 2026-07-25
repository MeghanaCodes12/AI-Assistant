import os
import random

from flask import (
    Flask,
    render_template,
    request,
    session,
    send_file,
    redirect,
    url_for
)

from dotenv import load_dotenv
from google import genai
from datetime import datetime

from prompts import (
    question_prompts,
    summary_prompts,
    creative_prompts
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = Flask(__name__)
app.secret_key = "my_secret_key"

print("API Key Loaded:", os.getenv("GEMINI_API_KEY") is not None)


@app.route("/", methods=["GET", "POST"])
def home():
    response = None
    user_input = ""
    function = "question"
    feedback_message = session.pop("feedback_message", None)
    feedback_time = session.pop("feedback_time", None)

    if request.method == "POST":
        function = request.form["function"]
        user_input = request.form["user_input"]

        session["last_function"] = function
        session["last_input"] = user_input

        if function == "question":
            prompt = random.choice(question_prompts)
        elif function == "summary":
            prompt = random.choice(summary_prompts)
        else:
            prompt = random.choice(creative_prompts)

        full_prompt = f"{prompt}\n\n{user_input}"

        try:
            result = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=full_prompt
            )

            response = result.text
            session["last_response"] = response

        except Exception as e:

            print("\n========== GEMINI ERROR ==========")
            print(type(e))
            print(e)
            print("==================================\n")

            error = str(e)

            if "RESOURCE_EXHAUSTED" in error:
                response = (
                    "⚠️ Daily API quota reached.\n\n"
                    "Please try again tomorrow or wait until your quota resets."
                )

            elif "503" in error or "UNAVAILABLE" in error:
                response = (
                    "⚠️ Gemini is currently experiencing high demand.\n\n"
                    "Please try again after a few moments."
                )

            elif "404" in error:
                response = (
                    "⚠️ The selected AI model is unavailable.\n\n"
                    "Please choose another Gemini model."
                )

            else:
                response = (
                    "⚠️ An unexpected error occurred.\n\n"
                    f"{error}"
                )
                session["last_response"] = response

    return render_template(
        "index.html",
        response=response,
        user_input=user_input,
        selected_function=function,
        feedback_message=feedback_message,
        feedback_time=feedback_time
    )


@app.route("/feedback", methods=["POST"])
def feedback():

    user_feedback = request.form.get("feedback")

    if not user_feedback:
        return "No feedback received!"

    last_function = session.get("last_function")
    last_input = session.get("last_input")
    last_response = session.get("last_response")
    
    current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    
    with open("feedback.txt", "a", encoding="utf-8") as file:
        file.write("-----------------------------------\n")
        file.write(f"Date: {current_time}\n")
        file.write(f"Function: {last_function}\n\n")
        file.write(f"User Input:\n{last_input}\n\n")
        file.write(f"AI Response:\n{last_response}\n\n")
        file.write(f"Feedback: {user_feedback}\n")
        file.write("-----------------------------------\n\n")
        
    session["feedback_message"] = "✅ Thank you for your feedback!"
    session["feedback_time"] = current_time
    return redirect(url_for("home"))

@app.route("/history",methods=["GET"])
def history():
    
    search = request.args.get("search", "").lower()
    records = []
    
    try:
        with open("feedback.txt", "r", encoding="utf-8") as file:
            content = file.read()
            blocks = content.split("-----------------------------------")
            for block in blocks:
                if block.strip():
                    if search in block.lower():
                        records.append(block)
    except FileNotFoundError:
        pass
        
    return render_template(
        "history.html",
        records=records,
        search=search
    )
    
@app.route("/clear_history",methods=["POST"])
def clear_history():
    open("feedback.txt", "w").close()
    
    return render_template(
        "history.html",
        records = [],
        message="✅ Feedback history cleared successfully!"
    )

@app.route("/download_feedback")
def download_feedback():
    return send_file(
        "feedback.txt",
        as_attachment=True
    )
    
@app.route("/dashboard")
def dashboard():
    
    yes_count = 0
    no_count = 0
    total = 0
    
    try:
        with open("feedback.txt","r", encoding="utf-8") as file:
            for line in file:
                if "Feedback: Yes" in line:
                    yes_count += 1
                elif "Feedback: No" in line:
                    no_count += 1
        total = yes_count + no_count
        
        if total > 0:
            positive_rate = round((yes_count / total) * 100, 2)
        else:
            positive_rate = 0
    except FileNotFoundError:
        positive_rate = 0
        
    return render_template(
        "dashboard.html",
        yes=yes_count,
        no=no_count,
        total=total,
        rate=positive_rate
    )

@app.route("/about")
def about():
    return render_template("about.html")   

if __name__ == "__main__":
    app.run(debug=True)
