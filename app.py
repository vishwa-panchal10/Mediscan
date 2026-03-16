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
from services.openai_service import analyze_medicine

load_dotenv()

app = Flask(__name__)
app.secret_key = "mediscan_super_secret_key"
CORS(app)

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediscan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Medicine(db.Model):

    id = db.Column(db.Integer, primary_key=True)

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

class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

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
        medicine = Medicine(

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

    if "admin_logged_in" not in session:
        return redirect(url_for("admin_login"))

    medicines = Medicine.query.order_by(Medicine.created_at.desc()).all()

    return render_template("admin.html", medicines=medicines)

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):

            session["admin_logged_in"] = True
            return redirect("/admin")

        else:
            return render_template("admin_login.html", error="You are not an admin!")

    return render_template("admin_login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)