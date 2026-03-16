# MEDISCAN – Medicine Information Extraction System

MEDISCAN is a web-based application that analyzes medicine strip images and extracts important medicine information automatically. The system performs OCR-based text extraction from uploaded medicine images and generates structured details such as composition, usage, advantages, and possible side effects.

The application is built using Python and Flask and integrates AI-based analysis to interpret medicine information efficiently.


# Features

• Upload medicine strip images for analysis
• Automatic OCR-based text extraction from medicine packaging
• Extract detailed medicine information including

* Medicine Name
* Strength
* Composition / Active Ingredients
* Usage / Treated Conditions
* Advantages / Benefits
* Disadvantages / Common Side Effects
* Serious Side Effects
* Who Should Avoid the Medicine
* Alternative Medicines

• Multi-language translation support
• Text-to-Speech support for medicine information
• Admin dashboard to monitor uploaded medicines
• Secure admin authentication system
• Stores medicine analysis with image and timestamp


# Technologies Used

Backend
• Python
• Flask

Frontend
• HTML
• CSS
• JavaScript

Database
• SQLite

Additional Libraries
• Flask-SQLAlchemy
• Flask-CORS
• Python dotenv


# Project Structure

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
│   └── admin_login.html
│
├── static/
│   ├── css/
│   ├── uploads/
│   └── audio/
│
└── instance/
    └── mediscan.db


# Installation

### 1 Clone the repository

git clone https://github.com/vishwa-panchal10/mediscan.git


### 2 Navigate to the project directory

cd mediscan


### 3 Create a virtual environment

python -m venv venv

Activate the environment (Windows)

venv\Scripts\activate


### 4 Install dependencies

pip install -r requirements.txt


### 5 Run the application

python app.py

The application will start at:


http://127.0.0.1:5000


# Admin Panel

The admin dashboard is available at:


/admin

Admin authentication is restricted to a **single predefined administrator account**.

Security features:

• Only the project owner can log in as admin
• No user registration system is available
• No option for users to create admin accounts
• Password change functionality is disabled for public users

This ensures that only the authorized administrator can access the dashboard and view uploaded medicine data.



# Use Case

MEDISCAN can assist:

• Patients who want to understand medicine information
• Pharmacists verifying medicine details
• Healthcare assistants analyzing medicine packaging
• Users needing accessible medicine explanations


# Future Improvements

• Integration with official medicine databases
• Mobile application version
• Barcode or QR code-based medicine detection
• Expanded multilingual support

# Author

Vishwa Panchal
Computer Engineering Student


# License

This project is developed for educational and research purposes.

---

✅ If you want, I can also give you a **much more impressive README version (with badges, UI screenshots, architecture diagram, and demo GIF)** that makes your project look **like a professional AI product on GitHub**.
