import os
import re
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_cors import CORS

# Load local environment variables
load_dotenv()

# Services
from services.translator_service import translate_text
from services.tts_service import generate_tts
from services.openai_service import analyze_medicine

app = Flask(__name__)
# No more session/secret key needed for basic analysis, but keeping for compatibility if needed
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "mediscan_standalone_key")
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure audio folder
AUDIO_FOLDER = "static/audio"
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER


def extract_field(text, field_name):
    """Helper to extract a specific field from the AI response model."""
    # allow flexible matching of section headings
    pattern = rf"{field_name}.*?:?\s*(.*?)(?=\n[A-Z][^:]*:|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Not Available"

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
        
        # No more database saving
        
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

        # For now, let's reuse the analyze_medicine logic but ask for a summary
        # or just return the text as is if we want simple behavior.
        # In a real app, you might have a specific summarize_medicine service.
        # Using existing service for simplicity.
        summary = f"Summary of medicine:\n{text[:500]}..." 
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
        lang = data.get("lang", "en")

        if not text:
            return jsonify({"error": "No text"}), 400

        audio_filename = generate_tts(text, lang, app.config["AUDIO_FOLDER"])

        return jsonify({"audio_url": f"/static/audio/{audio_filename}"})

    except Exception as e:
        print("TTS ERROR:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/test")
def test():
    return "App is working!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))