import os
from google import genai
from PIL import Image

MODEL_NAME = "gemini-2.5-flash"

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("WARNING: GOOGLE_API_KEY not found")

client = genai.Client(api_key=API_KEY)

def analyze_medicine(image_path):
    try:
        image = Image.open(image_path)
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

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, image]
        )

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", e)
        raise
