from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
import bcrypt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'cancer_detection_secret_key_2024'
CORS(app, supports_credentials=True)

# ─── MySQL Configuration ─────────────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change to your MySQL password
    'database': 'cancer_detection'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Initialize the database and create tables."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                age INT,
                gender VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                fatigue TINYINT(1),
                cough TINYINT(1),
                chest_pain TINYINT(1),
                weight_loss TINYINT(1),
                bleeding TINYINT(1),
                fever TINYINT(1),
                loss_of_appetite TINYINT(1),
                nausea TINYINT(1),
                difficulty_breathing TINYINT(1),
                skin_changes TINYINT(1),
                swelling TINYINT(1),
                night_sweats TINYINT(1),
                pain TINYINT(1),
                lumps TINYINT(1),
                hoarseness TINYINT(1),
                prediction TINYINT(1),
                probability FLOAT,
                risk_level VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  DB init error (running without DB): {e}")

# ─── ML Model ────────────────────────────────────────────────────────────────
FEATURE_COLS = [
    'fatigue', 'cough', 'chest_pain', 'weight_loss', 'bleeding',
    'fever', 'loss_of_appetite', 'nausea', 'difficulty_breathing',
    'skin_changes', 'swelling', 'night_sweats', 'pain', 'lumps', 'hoarseness'
]

def build_training_data():
    """Enhanced dataset with 100+ samples."""
    np.random.seed(42)
    n = 200

    # Positive cases (cancer)
    pos = {f: np.random.choice([0, 1], size=100, p=[0.2, 0.8]) for f in FEATURE_COLS}
    pos['cancer'] = [1] * 100

    # Negative cases (no cancer)
    neg = {f: np.random.choice([0, 1], size=100, p=[0.85, 0.15]) for f in FEATURE_COLS}
    neg['cancer'] = [0] * 100

    data = {f: list(pos[f]) + list(neg[f]) for f in FEATURE_COLS}
    data['cancer'] = pos['cancer'] + neg['cancer']

    # Add some real-world patterns
    extra_rows = [
        # High-risk patterns
        [1,1,1,1,0,1,1,1,1,1,1,1,1,1,0, 1],
        [1,0,1,1,1,1,1,0,1,0,1,1,1,1,1, 1],
        [0,1,0,1,0,0,1,1,0,1,0,1,1,1,0, 1],
        [1,1,1,1,1,0,1,1,1,0,1,1,1,0,1, 1],
        # Low-risk patterns
        [0,1,0,0,0,1,0,1,0,0,0,0,0,0,0, 0],
        [1,0,0,0,0,1,0,0,0,0,0,1,0,0,0, 0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0,0,1, 0],
        [0,1,0,0,0,1,0,1,0,0,0,0,0,0,0, 0],
    ]
    for row in extra_rows:
        for i, f in enumerate(FEATURE_COLS):
            data[f].append(row[i])
        data['cancer'].append(row[-1])

    return pd.DataFrame(data)

def train_model():
    df = build_training_data()
    X = df[FEATURE_COLS]
    y = df['cancer']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    model = GradientBoostingClassifier(n_estimators=200, max_depth=4, random_state=42)
    model.fit(X_train_s, y_train)
    acc = accuracy_score(y_test, model.predict(X_test_s))
    print(f"✅ Model trained | Accuracy: {acc:.2%}")
    return model, scaler

model, scaler = train_model()

# ─── Auth Routes ──────────────────────────────────────────────────────────────
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    age = data.get('age')
    gender = data.get('gender', '')

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, age, gender) VALUES (%s,%s,%s,%s,%s)",
            (name, email, pw_hash, age, gender)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        session['user_id'] = user_id
        session['user_name'] = name
        return jsonify({'message': 'Account created', 'name': name, 'user_id': user_id})
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Email already registered'}), 409
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user or not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return jsonify({'error': 'Invalid email or password'}), 401

        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return jsonify({'message': 'Login successful', 'name': user['name'], 'user_id': user['id']})
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'})

@app.route('/api/me')
def me():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    return jsonify({'user_id': session['user_id'], 'name': session['user_name']})

# ─── Prediction Route ─────────────────────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    user_id = data.get('user_id') or session.get('user_id')

    symptoms = {f: int(data.get(f, 0)) for f in FEATURE_COLS}
    df = pd.DataFrame([symptoms])
    scaled = scaler.transform(df)
    pred = int(model.predict(scaled)[0])
    prob = float(model.predict_proba(scaled)[0, 1])

    if prob < 0.3:
        risk = 'Low'
    elif prob < 0.6:
        risk = 'Moderate'
    else:
        risk = 'High'

    # Save to DB if user is logged in
    if user_id:
        try:
            conn = get_db()
            cursor = conn.cursor()
            cols = ', '.join(FEATURE_COLS + ['prediction', 'probability', 'risk_level', 'user_id'])
            vals = [symptoms[f] for f in FEATURE_COLS] + [pred, prob, risk, user_id]
            placeholders = ', '.join(['%s'] * len(vals))
            cursor.execute(f"INSERT INTO predictions ({cols}) VALUES ({placeholders})", vals)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Could not save prediction: {e}")

    return jsonify({'prediction': pred, 'probability': round(prob, 4), 'risk_level': risk})

# ─── History Route ────────────────────────────────────────────────────────────
@app.route('/api/history')
def history():
    user_id = request.args.get('user_id') or session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM predictions WHERE user_id=%s ORDER BY created_at DESC LIMIT 20",
            (user_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for r in rows:
            if isinstance(r.get('created_at'), datetime):
                r['created_at'] = r['created_at'].strftime('%Y-%m-%d %H:%M')
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
