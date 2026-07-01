from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
import re

app = Flask(__name__)
# In a real app, use a strong, randomly generated secret key stored in environment variables
app.secret_key = 'super_secret_session_key_for_development'

# --- Database Setup ---
def get_db_connection():
    conn = sqlite3.connect('secure_app.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Creates table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# --- HTML Templates (Inline for simplicity) ---
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Login System</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 300px; text-align: center; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #28a745; color: white; border: none; padding: 10px 15px; width: 100%; border-radius: 4px; cursor: pointer; }
        button:hover { background: #218838; }
        .error { color: red; font-size: 0.9em; margin-bottom: 10px; }
        .success { color: green; font-size: 0.9em; margin-bottom: 10px; }
        a { color: #007bff; text-decoration: none; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

REGISTER_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h2>Register</h2>
    <form method="POST" action="{{ url_for('register') }}">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Sign Up</button>
    </form>
    <br>
    <a href="{{ url_for('login') }}">Already have an account? Login here</a>
""")

LOGIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h2>Login</h2>
    <form method="POST" action="{{ url_for('login') }}">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    <br>
    <a href="{{ url_for('register') }}">Need an account? Register here</a>
""")

DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h2>Welcome, {{ username }}!</h2>
    <p>You have successfully accessed the secure dashboard.</p>
    <form method="POST" action="{{ url_for('logout') }}">
        <button type="submit" style="background: #dc3545;">Logout</button>
    </form>
""")

# --- Routes & Logic ---

@app.route('/')
def index():
    # Session Management: Check if user is logged in
    if 'user_id' in session:
        return render_template_string(DASHBOARD_TEMPLATE, username=session['username'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # 1. Basic Input Validation
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
            flash('Username must be 3-20 characters (alphanumeric or underscore).', 'error')
            return render_template_string(REGISTER_TEMPLATE)
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template_string(REGISTER_TEMPLATE)

        # 2. Hashing the Password (using bcrypt)
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        conn = get_db_connection()
        try:
            # 3. SQL Injection Protection (Using parameterized queries '?')
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                         (username, password_hash))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'error')
        finally:
            conn.close()

    return render_template_string(REGISTER_TEMPLATE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        conn = get_db_connection()
        # SQL Injection Protection: Parameterized query
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        # 4. Verify Hash and Manage Session
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            # Prevent Session Fixation by clearing old session data
            session.clear() 
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout', methods=['POST'])
def logout():
    # 5. Logout Feature: Clear the session securely
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)