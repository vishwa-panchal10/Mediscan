import os
from openai import OpenAI
from PIL import Image
import base64
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gpt-4.1-mini"  # or "gpt-4.1" if you have access

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)


def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def analyze_medicine(image_path):
    base64_image = encode_image(image_path)

    prompt = """
You are a highly knowledgeable and precise medical assistant AI.

Step 1: Image Validation
Carefully examine the uploaded image.

Check if the image contains a MEDICINE STRIP with silver foil packaging where medicine names or text are printed.

If the image only contains loose tablets/pills or if the medicine name is not visible on the strip,
then respond ONLY with the following message:

"Unable to detect a medicine strip with visible medicine name. Please upload a clear image of the medicine strip foil."

Do NOT generate any medicine information in that case.

Step 2: Medicine Information Extraction
Carefully analyze the uploaded medicine image and extract:
- Medicine Name
- Strength (if unclear, estimate the most common strength for that medicine)
- Active Ingredient (very important)
- Any visible manufacturer details

Step 3: Medicine Information Generation
Using strong medical knowledge, generate COMPLETE, PRACTICAL, and MEDICALLY ACCURATE information.

IMPORTANT INSTRUCTIONS:
- Do NOT give generic answers
- Always give SPECIFIC diseases/conditions (e.g., acne, UTI, pneumonia, chlamydia)
- Always mention if medicine works ONLY for bacterial infections (if applicable)
- Always include at least 4–6 clear usage points
- Always include important real-world precautions and risks
- If the exact brand data is unclear, rely on the active ingredient knowledge

CRITICAL MEDICAL REQUIREMENTS:
- Include common AND important side effects (e.g., photosensitivity for doxycycline)
- Include at least 2–3 serious side effects (even if rare)
- Include practical warnings (e.g., avoid milk, sunlight, alcohol, drug interactions if relevant)
- Include specific groups who should avoid (children, pregnant women, liver/kidney issues, etc.)
- Do NOT skip important safety information

Formatting Rules:
- Medicine Name must be written in ONE LINE after the colon.
- Other sections must contain plain text bullet-style lines WITHOUT using symbols like *, •, -, or markdown
- Each point must be short (1–2 lines max)
- Minimum 2-3 points per section wherever applicable
- Do NOT write paragraphs
- Do NOT say “Information not available from image”
- Be precise, structured, and medically useful

Medicine Name:

Strength:

Composition / Active Ingredient:

Usage / Diseases or Conditions Treated:

Advantages / Main Benefits:

Disadvantages / Common Side Effects:

Serious Side Effects:

Who Should Avoid This Medicine:

Alternative Medicines (Same Composition):
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content


def summarize_medicine_details(text):
    prompt = f"""
You are a medical assistant AI. Based on the following extracted medicine details, provide a concise summary in 5 to 10 important points.
The points should be written as PLAIN TEXT lines. Do NOT use any symbols like *, •, -, or markdown.
Each point should be clear and concise.

Medicine Details:
{text}

Summary Points:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content
