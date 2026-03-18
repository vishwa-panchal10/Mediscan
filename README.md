# 🧠 MEDISCAN – AI-Powered Medicine Information Extraction System

MEDISCAN is an intelligent web application that analyzes **medicine strip images** and automatically extracts structured medical information using OCR and AI-based processing.

It helps users quickly understand medicine details such as composition, usage, side effects, and alternatives — making healthcare information more accessible and user-friendly.

---

## 🚀 Features

### 🔍 Image Analysis

* Upload medicine strip images
* OCR-based text extraction from packaging
* AI-powered interpretation of extracted text

### 💊 Medicine Information Extraction

* Medicine Name
* Strength
* Composition / Active Ingredients
* Usage / Treated Conditions
* Advantages / Benefits
* Common Side Effects
* Serious Side Effects
* Who Should Avoid the Medicine
* Alternative Medicines

### 🌐 Accessibility Features

* Multi-language translation
* Text-to-Speech (TTS) support

### 🔐 Admin Dashboard

* Secure admin login
* View uploaded medicines with images & timestamps
* Restricted access (single admin only)

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite (local development)

### Libraries & Tools

* Flask-SQLAlchemy
* Flask-CORS
* Python-dotenv

---

## 📁 Project Structure

```
mediscan/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── services/
│   ├── openai_service.py
│   ├── translator_service.py
│   └── tts_service.py
│
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── login.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── audio/
│
└── instance/
    └── mediscan.db
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vishwa-panchal10/Mediscan.git
cd Mediscan
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate (Windows):

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```bash
python app.py
```

📍 App will run at:

```
http://127.0.0.1:5000
```

---

## 🔐 Admin Panel

Access admin dashboard:

```
/admin
```

### Security Features

* Single predefined admin account
* No public registration
* No admin creation allowed
* Restricted dashboard access

---

## 🎯 Use Cases

MEDISCAN can be used by:

* 👨‍⚕️ Patients – to understand medicines easily
* 💊 Pharmacists – to verify medicine details
* 🏥 Healthcare assistants – to analyze packaging
* ♿ Users needing accessible medical info

---

## ⚠️ Limitations

* Depends on image quality for OCR accuracy
* Not a substitute for professional medical advice
* Uses local SQLite DB (not persistent in deployment)

---

## 🔮 Future Improvements

* Integration with official medical databases
* Cloud database (PostgreSQL / MySQL)
* Mobile application (Android/iOS)
* Barcode / QR-based detection
* Enhanced multilingual support

---

## 👨‍💻 Author

**Vishwa Panchal**
Computer Engineering Student

---

## 📜 License

This project is developed for **educational and research purposes only**.

