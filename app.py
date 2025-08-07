from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        return redirect(url_for('results'))
    return render_template('quiz.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = f"You asked: {question} — AI suggests: Learn step by step with Dream Drift!"
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
