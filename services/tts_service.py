from gtts import gTTS
import os
import uuid
import re

SUPPORTED_LANGS = {
    "en": "en",
    "hi": "hi",
    "gu": "gu",
    "ta": "ta",
    "te": "te",
    "kn": "kn",
    "ml": "ml",
    "mr": "mr",
    "bn": "bn",
    "pa": "pa",
    "or": "or"
}

def clean_text(text):
    text = re.sub(r"[•\-]", "", text)
    text = text.replace(":", ". ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def generate_audio(text, lang_code, folder):

    if lang_code not in SUPPORTED_LANGS:
        lang_code = "en"  # fallback to English

    clean = clean_text(text)

    filename = f"{uuid.uuid4()}.mp3"
    path = os.path.join(folder, filename)

    tts = gTTS(text=clean, lang=lang_code)
    tts.save(path)

    return f"/static/audio/{filename}"