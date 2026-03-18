import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

#from services.gemini_service import analyze_medicine 
from services.translator_service import translate_text
from services.tts_service import generate_audio
from services.openai_service import analyze_medicine, summarize_medicine_details

load_dotenv()

app = Flask(__name__)
app.secret_key = "mediscan_super_secret_key"
CORS(app)

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediscan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Relationship to medicine uploads
    medicines = db.relationship('Medicine', backref='user', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Linked to user
    image_path = db.Column(db.String(200))
    medicine_name = db.Column(db.String(200))
    strength = db.Column(db.String(100))
    composition = db.Column(db.Text)
    usage = db.Column(db.Text)
    advantages = db.Column(db.Text)
    disadvantages = db.Column(db.Text)
    serious_side_effects = db.Column(db.Text)
    who_should_avoid = db.Column(db.Text)
    alternatives = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, **kwargs):
        super(Medicine, self).__init__(**kwargs)

# Removed Admin model as per request for unified login



UPLOAD_FOLDER = "static/uploads"
AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER

import re

def extract_field(text, field):

    # allow flexible matching of section headings
    pattern = rf"{field}.*?:?\s*(.*?)(?=\n[A-Z][^:]*:|\Z)"

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
@app.route("/analyze/", methods=["POST"])
def analyze():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        result_text = analyze_medicine(filepath)
        
        user_id = session.get("user_id")
        medicine = Medicine(
            user_id = user_id,
            image_path = filepath,
            medicine_name = extract_field(result_text, "Medicine Name"),
            strength = extract_field(result_text, "Strength"),
            composition = extract_field(result_text, "Composition / Active Ingredient"),
            usage = extract_field(result_text, "Usage / Diseases or Conditions Treated"),
            advantages = extract_field(result_text, "Advantages / Main Benefits"),
            disadvantages = extract_field(result_text, "Disadvantages / Common Side Effects"),
            serious_side_effects = extract_field(result_text, "Serious Side Effects"),
            who_should_avoid = extract_field(result_text, "Who Should Avoid This Medicine"),
            alternatives = extract_field(result_text, "Alternative Medicines")
        )

        # Only admins can save/view history in this version, or we can allow guest temporary session?
        # For now, guests don't have user_id, so medicine is not linked to any user if guest.
        # This is fine as per requirements.

        db.session.add(medicine)
        db.session.commit()
        
        print("\n===== GEMINI RESPONSE =====\n")
        print(result_text)

        print("\n===== PARSED ALTERNATIVES =====\n")
        print(extract_field(result_text, "Alternative Medicines"))
        return jsonify({"result": result_text})
        
    except Exception as e:
        print("ANALYZE ERROR:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/summarize", methods=["POST"])
@app.route("/summarize/", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        text = data.get("text")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        summary = summarize_medicine_details(text)
        return jsonify({"summary": summary})

    except Exception as e:
        print("SUMMARIZE ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/translate", methods=["POST"])
@app.route("/translate/", methods=["POST"])
def translate():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        text = data.get("text")
        lang = data.get("lang")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        translated = translate_text(text, lang)

        return jsonify({"translated": translated})

    except Exception as e:
        print("ROUTE ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/tts", methods=["POST"])
@app.route("/tts/", methods=["POST"])
def tts():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        text = data.get("text")
        lang = data.get("lang")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        audio_path = generate_audio(text, lang, app.config["AUDIO_FOLDER"])

        return jsonify({"audio_url": audio_path})

    except Exception as e:
        print("TTS ERROR:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/admin")
def admin():
    if not session.get("is_admin"):
        return "Access Restricted: You do not have permission to view this page.", 403

    medicines = Medicine.query.order_by(Medicine.created_at.desc()).all()
    return render_template("admin.html", medicines=medicines)

@app.route("/guest")
def guest():
    session["is_guest"] = True
    session["user_email"] = "Guest User"
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Restriction: Only admin can login
        if email != "vishwa.cp10@gmail.com":
            return render_template("login.html", error="Only admin can login!")
            
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_email"] = user.email
            session["is_admin"] = True
            session["is_guest"] = False
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid email or password!")
    return render_template("login.html")

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # In a real app, you would send an email here.
    # For this project, we'll just return a success message.
    return jsonify({"message": f"A password reset link has been sent to {email}"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))