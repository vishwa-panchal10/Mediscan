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
You are a professional medical assistant AI.

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
- Strength
- Active Ingredient
- Any visible manufacturer details


Step 3: Medicine Information Generation
Using medical knowledge, provide COMPLETE detailed information about the extracted medicine.

Return the output STRICTLY in the following structured format.

Formatting Rules:
- Medicine Name must be written in ONE LINE after the colon.
- Other sections must contain short bullet points.
- Do NOT use symbols like *, •, -, or markdown.
- Keep each point clear and concise (1–2 lines maximum).
- Do NOT say “Information not available from image”.
- If brand data is missing, provide details based on active ingredient.

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