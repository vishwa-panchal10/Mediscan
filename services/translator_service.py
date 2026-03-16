from deep_translator import GoogleTranslator


def translate_text(text, lang_code):

    try:
        if not text:
            return "No text provided."

        translator = GoogleTranslator(
            source="auto",
            target=lang_code
        )

        lines = text.split("\n")
        translated_lines = []

        for line in lines:
            if line.strip() == "":
                translated_lines.append("")
            else:
                translated_line = translator.translate(line)
                translated_lines.append(translated_line)

        return "\n".join(translated_lines)

    except Exception as e:
        print("TRANSLATION ERROR:", e)
        raise Exception("Google translation failed.")