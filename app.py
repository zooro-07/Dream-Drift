# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/about')
def about():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change to a strong secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dream_drift.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Sample data for courses, interests, and colleges
courses_info = {
    'Data Science': {
        'interests': ['Math', 'Statistics', 'Programming'],
        'colleges': ['MIT', 'Stanford', 'Carnegie Mellon']
    },
    'AI & ML': {
        'interests': ['Programming', 'Logic', 'Math'],
        'colleges': ['CMU', 'UC Berkeley', 'Oxford']
    },
    'Web Development': {
        'interests': ['Creativity', 'Programming', 'Design'],
        'colleges': ['Harvard', 'Google University', 'MIT']
    },
    'Mechanical Engineering': {
        'interests': ['Physics', 'Math', 'Hands-on'],
        'colleges': ['MIT', 'IIT Bombay', 'Stanford']
    },
    'Business Management': {
        'interests': ['Communication', 'Leadership', 'Economics'],
        'colleges': ['Harvard', 'Wharton', 'INSEAD']
    }
}

# Best Scope Courses Data (for visualization)
best_scope_courses = {
    'Data Science': 90,
    'AI & ML': 85,
    'Web Development': 70,
    'Mechanical Engineering': 65,
    'Business Management': 75
}

# Routes

# Home redirects to login
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# Register page (optional for testing)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="User already exists")
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Dashboard after login
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Interest analyzer page and form submission
@app.route('/interest_analyzer', methods=['GET', 'POST'])
def interest_analyzer():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Collect interest inputs from form
        interests = request.form.getlist('interests')
        # Simple matching algorithm: count matching interests with course interests
        course_scores = {}
        for course, details in courses_info.items():
            score = len(set(interests) & set(details['interests']))
            course_scores[course] = score

        # Get best course match
        best_course = max(course_scores, key=course_scores.get)
        roadmap = generate_roadmap(best_course)

        return render_template('roadmap.html', best_course=best_course, roadmap=roadmap, colleges=courses_info[best_course]['colleges'])
    # Interest options
    all_interests = sorted({i for details in courses_info.values() for i in details['interests']})
    return render_template('interest_analyzer.html', interests=all_interests)

# Helper function to generate roadmap based on course
def generate_roadmap(course):
    # Ideally this will be more detailed and dynamic, here is a static example
    roadmaps = {
        'Data Science': [
            "Build strong foundation in Mathematics and Statistics",
            "Learn Python programming and libraries like NumPy, pandas",
            "Take online courses on Machine Learning and Data Visualization",
            "Work on projects and internships",
            "Apply to top Data Science Masters programs"
        ],
        'AI & ML': [
            "Strengthen Mathematics and Logic skills",
            "Learn Python and AI libraries (TensorFlow, PyTorch)",
            "Participate in AI/ML competitions (Kaggle)",
            "Research papers and internships",
            "Enroll in specialized AI Masters courses"
        ],
        'Web Development': [
            "Learn HTML, CSS and JavaScript",
            "Understand frontend frameworks (React, Vue)",
            "Learn backend with Flask/Django or Node.js",
            "Build and deploy websites and applications",
            "Explore colleges with strong CS programs"
        ],
        'Mechanical Engineering': [
            "Master Physics and Mathematics",
            "Understand core Mechanical Engineering subjects",
            "Work on hands-on projects and CAD software",
            "Internships in manufacturing or design",
            "Apply for top Mechanical Engineering colleges"
        ],
        'Business Management': [
            "Develop communication and leadership skills",
            "Learn basics of Economics and Marketing",
            "Participate in business clubs and competitions",
            "Internships in startups or companies",
            "Apply for reputed B-schools"
        ]
    }
    return roadmaps.get(course, [])

# Courses scope graph page
@app.route('/courses_scope')
def courses_scope():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('courses_scope.html', courses=best_scope_courses)

# API endpoint to get colleges for a selected course (AJAX)
@app.route('/get_colleges/<course>')
def get_colleges(course):
    colleges = courses_info.get(course, {}).get('colleges', [])
    return jsonify(colleges)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
