# 🤖 AI-Powered Intelligent Assistant using Flask and Google Gemini API

## Project Overview
This project is an AI-powered web application developed using Python Flask and the Google
Gemini API. It allows users to perform various AI tasks such as answering questions,
summarizing text, and generating creative content. The application also collects user
feedback and provides an analytics dashboard, all wrapped in a modern, responsive interface
with light and dark themes.

## Features
- Answer Questions
- Summarize Text
- Generate Creative Content
- User Feedback System (Yes/No rating)
- Feedback History
- Search Feedback
- Download Feedback
- Clear Feedback History
- Dashboard Analytics
- Pie Chart Visualization (Chart.js)
- Dark Mode
- Responsive Design
- About Page

## Technologies Used
- Python
- Flask
- Google Gemini API (`google-genai`)
- python-dotenv
- HTML5
- CSS3
- JavaScript
- Chart.js

## Project Structure
AI Assistant/
│
├── app.py
├── prompts.py
├── requirements.txt
├── .env
├── .gitignore
├── feedback.txt
├── README.md
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    ├── index.html
    ├── history.html
    ├── dashboard.html
    └── about.html

## Installation
1. Clone the repository.
git clone <repository-url>
cd "AI Assistant"

2. Create and activate a virtual environment.
python -m venv venv
venv\Scripts\activate      (Windows)
source venv/bin/activate   (macOS/Linux)

3. Install dependencies.
pip install -r requirements.txt

4. Create a `.env` file in the project root.
GEMINI_API_KEY=your_key_here

5. Run the application.
python app.py

6. Open your browser.
http://127.0.0.1:5000

## Notes
- Feedback data is stored locally in `feedback.txt` and powers both the History and
  Dashboard pages.
- Dark mode preference is saved in the browser using `localStorage`.
- Never commit a real `.env` file containing your API key — use the placeholder format
  shown above and keep `.env` listed in `.gitignore`.

## Author
Annaladasu Meghana
