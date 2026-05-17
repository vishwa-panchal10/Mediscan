# 🚀 MEDISCAN

### AI-Powered Medicine Information Extraction from Images

MEDISCAN is a lightweight, AI-driven web application that enables users to **analyze medicine strip images** and instantly receive **structured, human-readable medical information**.

By combining **OCR (Optical Character Recognition)** with **AI-based language processing**, the system transforms raw packaging text into meaningful insights such as composition, usage, and safety information — all in real time.


# 🌟 Features

## 📸 Image-Based Medicine Detection

* Upload a medicine strip image
* Automatically extracts visible text using OCR

## 🧠 Intelligent Information Extraction

Generates structured details including:

* Medicine Name
* Strength & Dosage
* Composition / Active Ingredients
* Usage / Treated Conditions
* Advantages / Benefits
* Common Side Effects
* Serious Side Effects
* Safety Warnings (Who should avoid)
* Alternative Medicines

## 🌐 Multi-language Translation

* Converts extracted information into multiple languages

## 🔊 Text-to-Speech (TTS)

* Converts medical information into audio output
* Improves accessibility for all users


# ⚙️ How It Works

```text
Image Upload → OCR Extraction → AI Processing → Structured Medical Output
```



# 🧰 Tech Stack

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* JavaScript

### AI & Processing

* OCR for text extraction
* AI API for contextual medicine analysis


# 📂 Project Structure

```
mediscan/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── services/
│   ├── openai_service.py
│   ├── translator_service.py
│   └── tts_service.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── uploads/
│   └── audio/
```


# ⚙️ Installation & Setup

## 1️⃣ Clone the repository

```bash
git clone https://github.com/vishwa-panchal10/Mediscan.git
cd Mediscan
```

## 2️⃣ Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Configure environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
```

## 5️⃣ Run the application

```bash
python app.py
```

Application will run at:

```
http://127.0.0.1:5000
```


# 🎯 Use Cases

* 👨‍⚕️ Quick medicine understanding for patients
* 💊 Pharmacy-level verification
* 🎓 Educational AI healthcare projects
* ♿ Accessibility-focused applications (via TTS)


# 🔮 Future Enhancements

* 📱 Mobile application version
* 🌍 Advanced multilingual support
* 🧾 Integration with official medicine databases


# 👨‍💻 Author

**Vishwa Panchal**
Computer Science Engineering Student


# 📜 License

This project is intended for **educational and research purposes only**.

