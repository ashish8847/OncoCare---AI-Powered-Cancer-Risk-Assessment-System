# 🧬 OncoCare — AI-Powered Cancer Risk Assessment System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.0-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-blue?style=for-the-badge&logo=mysql&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.9.0-green?style=for-the-badge&logo=python&logoColor=white)

**A full-stack web application that uses Machine Learning to assess cancer risk based on 15 clinical symptoms.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [ML Models](#-ml-models) • [API Docs](#-api-endpoints) • [Project Structure](#-project-structure)

</div>

---

## 📌 Overview

OncoCare is a symptom-based cancer risk assessment tool that leverages three trained Machine Learning models to predict the likelihood of cancer based on 15 binary symptom inputs. It provides:

- **Risk Classification** — Low / Moderate / High
- **Cancer Probability Score** — as a percentage
- **Multi-Model Comparison** — compare GBM, Random Forest, and SVM predictions simultaneously
- **Visual Charts** — matplotlib-generated dual-panel charts (bar chart + donut gauge)
- **User Accounts** — register, login, and view your full assessment history
- **Dark / Light Mode** — toggle between themes

> ⚠️ **Disclaimer:** This tool is for **educational purposes only** and is **not a medical diagnosis**. Always consult a qualified healthcare professional.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 3 ML Models | Gradient Boosting (default), Random Forest, SVM |
| 📊 Live Charts | Matplotlib bar + donut chart comparing all 3 models |
| 🔐 Authentication | Secure signup/login with bcrypt password hashing |
| 🗃️ History | Stores last 20 assessments per user in MySQL |
| 🌙 Dark/Light Mode | Full theme toggle with CSS variables |
| 📱 Responsive | Works on desktop, tablet, and mobile |
| ⚡ Fast | Sub-500ms prediction response time |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** — Core language
- **Flask 3.0.3** — REST API framework
- **scikit-learn 1.5.0** — ML models (GBM, Random Forest, SVM)
- **Matplotlib 3.9.0** — Chart generation (server-side)
- **MySQL 8.4** — User and prediction data storage
- **bcrypt 4.1.3** — Secure password hashing
- **pandas 2.2.2 / numpy 1.26.4** — Data processing

### Frontend
- **HTML5 / CSS3 / Vanilla JavaScript** — Single-file SPA (`index.html`)
- **CSS Custom Properties** — Dark/light mode theming
- **Google Fonts** — Playfair Display + DM Sans

---

## 📂 Project Structure

```
oncocare/
│
├── app.py                  # Flask backend — ML pipeline + REST API
├── index.html              # Frontend — Single Page Application
├── requirements.txt        # Python dependencies
│
├── docs/
│   └── OncoCare_Project_Report.docx   # Full project report
│
└── README.md               # This file
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.x
- pip

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/oncocare.git
cd oncocare
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Configure MySQL

Open `app.py` and update the database configuration:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',   # <-- change this
    'database': 'cancer_detection'
}
```

> The database and tables are **auto-created** on first run — no manual SQL needed.

### Step 4 — Run the Application

```bash
python app.py
```

The server starts at **http://localhost:5000**

Open your browser and go to → `http://localhost:5000`

---

## 🚀 Usage

1. **Register** — Create an account with your name, email, and password
2. **Select Symptoms** — Check all symptoms you are currently experiencing
3. **Choose a Model** — Pick from Gradient Boosting, Random Forest, or SVM
4. **Analyze Risk** — Click "Analyze Risk" to get your assessment
5. **View Results** — See your risk level, probability score, and model comparison chart
6. **History** — Navigate to "My History" to view past assessments

---

## 🤖 ML Models

All three models are trained at server startup using a synthetically generated dataset of **208 samples** with **15 binary symptom features**.

### Models Implemented

| Model | Accuracy | Key Parameters | Type |
|---|---|---|---|
| **Gradient Boosting** ⭐ | ~95.2% | n_estimators=200, max_depth=4 | Ensemble (Boosting) |
| **Random Forest** | ~92.8% | n_estimators=200 | Ensemble (Bagging) |
| **SVM (RBF Kernel)** | ~90.5% | kernel='rbf', probability=True | Kernel-based |

### Training Pipeline

```
Raw Symptoms (15 binary inputs)
        ↓
  pandas DataFrame
        ↓
  StandardScaler.transform()
        ↓
  model.predict_proba()[:, 1]
        ↓
  Risk Classification
  ├── < 30%  → Low Risk  ✅
  ├── 30-60% → Moderate Risk  ⚠️
  └── > 60%  → High Risk  🚨
```

### Input Features (15 Symptoms)

| # | Symptom | # | Symptom |
|---|---|---|---|
| 1 | Fatigue | 9 | Difficulty Breathing |
| 2 | Persistent Cough | 10 | Skin Changes |
| 3 | Chest Pain | 11 | Swelling / Lumps |
| 4 | Unexplained Weight Loss | 12 | Night Sweats |
| 5 | Unusual Bleeding | 13 | Persistent Pain |
| 6 | Fever | 14 | Lumps / Masses |
| 7 | Loss of Appetite | 15 | Hoarseness |
| 8 | Nausea | | |

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Body |
|---|---|---|---|
| `POST` | `/api/signup` | Register new user | `{name, email, password, age, gender}` |
| `POST` | `/api/login` | Login | `{email, password}` |
| `POST` | `/api/logout` | Logout | — |
| `GET` | `/api/me` | Get current user | — |

### ML & Data

| Method | Endpoint | Description | Body |
|---|---|---|---|
| `POST` | `/api/predict` | Get cancer risk prediction | `{symptom_keys..., model, user_id}` |
| `POST` | `/api/chart` | Generate comparison chart | `{symptom_keys..., dark_mode}` |
| `GET` | `/api/history` | Get user assessment history | `?user_id=X` |

### Predict Request Example

```json
POST /api/predict
{
  "fatigue": 1,
  "cough": 1,
  "chest_pain": 0,
  "weight_loss": 1,
  "bleeding": 0,
  "fever": 1,
  "loss_of_appetite": 1,
  "nausea": 0,
  "difficulty_breathing": 1,
  "skin_changes": 0,
  "swelling": 1,
  "night_sweats": 1,
  "pain": 1,
  "lumps": 0,
  "hoarseness": 0,
  "model": "gradient_boosting",
  "user_id": 1
}
```

### Predict Response Example

```json
{
  "prediction": 1,
  "probability": 0.8742,
  "risk_level": "High",
  "model_used": "gradient_boosting"
}
```

---

## 🗄️ Database Schema

### `users` Table

| Column | Type | Description |
|---|---|---|
| `id` | INT PK | Auto-increment primary key |
| `name` | VARCHAR(100) | Full name |
| `email` | VARCHAR(150) UNIQUE | Email address |
| `password_hash` | VARCHAR(255) | bcrypt hashed password |
| `age` | INT | Age (optional) |
| `gender` | VARCHAR(20) | Gender (optional) |
| `created_at` | TIMESTAMP | Registration timestamp |

### `predictions` Table

| Column | Type | Description |
|---|---|---|
| `id` | INT PK | Auto-increment primary key |
| `user_id` | INT FK | References `users.id` |
| `fatigue` ... `hoarseness` | TINYINT(1) | 15 symptom columns |
| `prediction` | TINYINT(1) | 0 = No cancer, 1 = Cancer |
| `probability` | FLOAT | Cancer probability (0–1) |
| `risk_level` | VARCHAR(20) | Low / Moderate / High |
| `created_at` | TIMESTAMP | Assessment timestamp |

---

## 📦 Dependencies

```
flask==3.0.3
flask-cors==4.0.1
mysql-connector-python==8.4.0
bcrypt==4.1.3
pandas==2.2.2
scikit-learn==1.5.0
numpy==1.26.4
matplotlib==3.9.0
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🔒 Security

- Passwords are hashed using **bcrypt** with automatic salting — plain text passwords are never stored
- All database queries use **parameterized statements** — no SQL injection risk
- Session management uses **Flask server-side sessions** with a secret key
- CORS is configured with `supports_credentials=True` for secure cookie handling

---

## 🌐 Browser Compatibility

| Browser | Status |
|---|---|
| Google Chrome 124+ | ✅ Fully supported |
| Mozilla Firefox 125+ | ✅ Fully supported |
| Microsoft Edge 124+ | ✅ Fully supported |
| Safari 17+ | ✅ Supported (minor select styling differences) |
| Chrome Mobile | ✅ Responsive layout |

---

## 📄 Project Report

The full academic project report is available in the `docs/` folder:

📄 [`docs/OncoCare_Project_Report.docx`](docs/OncoCare_Project_Report.docx)

The report covers:
- Chapter 1: Introduction & Problem Identification
- Chapter 2: Literature Review & Background Study
- Chapter 3: Design Flow & Methodology
- Chapter 4: Results Analysis & Validation
- Chapter 5: Conclusion & Future Work
- Chapter 6: References

---

## 🔮 Future Work

- [ ] Replace synthetic dataset with real clinical cancer dataset
- [ ] Add cancer-type specific models (lung, breast, colon)
- [ ] Deploy on AWS / Azure with managed MySQL (RDS)
- [ ] Build React Native / Flutter mobile app
- [ ] Add PDF report download for each assessment
- [ ] Multilingual support (Hindi, Punjabi, Tamil)
- [ ] Nearest oncologist finder using Google Maps API
- [ ] k-fold cross-validation and hyperparameter tuning (GridSearchCV)

---

## 👨‍💻 Author

Ashish Sharma
- GitHub: @ashish8847(https://github.com/ashish8847)
- Email: sharma.ashish5647@gmail.com

---

<div align="center">
Made with ❤️ for early cancer awareness | OncoCare 2024–2025
</div>
