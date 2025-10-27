import os
import json
import re
import ast
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = os.getenv('BASE_URL')

# Debugging (optional)
print(f"Using OPENAI_API_KEY: {API_KEY[:8]}...")  # partial for safety
print(f"Using BASE_URL: {BASE_URL}")

# Initialize client
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# -------------------------------
# JSON PARSING HELPER
# -------------------------------
def safe_parse_json(raw_response: str):
    """
    Safely parse a JSON string returned by the LLM.
    Handles common issues like:
    - Python dict format (single quotes)
    - Extra text around JSON
    - Code fences (```json ... ```)
    Always returns a valid Python dict.
    """

    if not raw_response:
        return {"error": "Empty response from model."}

    # Step 1: Remove code fences or markdown formatting
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw_response.strip(), flags=re.MULTILINE).strip()

    # Step 2: Try parsing valid JSON first
    try:
        parsed = json.loads(cleaned)
        return parsed
    except json.JSONDecodeError:
        pass

    # Step 3: Try to extract a JSON-like portion
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        json_text = match.group(0)
    else:
        json_text = cleaned

    # Step 4: Convert Python-style single quotes to double quotes safely
    json_text = re.sub(r"(?<!\\)'", '"', json_text)

    # Step 5: Try JSON again
    try:
        parsed = json.loads(json_text)
        return parsed
    except json.JSONDecodeError:
        pass

    # Step 6: Try AST literal eval (for Python dicts)
    try:
        parsed = ast.literal_eval(cleaned)
        if isinstance(parsed, dict):
            return parsed
        else:
            return {"error": "Parsed output is not a dictionary.", "raw": cleaned}
    except Exception:
        return {"error": "Failed to parse model output as JSON.", "raw": cleaned}


# -------------------------------
# HELPER: FORCE JSON RETURN
# -------------------------------
def ensure_json_output(data):
    """
    Converts a Python dict into a valid JSON string.
    Ensures that all generation functions return JSON objects.
    """
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False, indent=2)
    else:
        return json.dumps({"error": "Invalid data structure returned."}, indent=2)


# -------------------------------
# GENERATION SERVICE FUNCTIONS
# -------------------------------

def generate_summary(document_text: str) -> str:
    """Generate an HTML summary from a document text."""
    system_prompt = """
    Generate a concise summary of the provided document. The output must be a JSON object containing the summary as an HTML string, conforming to the provided schema.

    **Content & HTML Rules:**
    1. The summary must accurately reflect the key information in the document.
    2. Generate semantic HTML for the summary content.
    3. Apply the following CSS classes EXACTLY as specified to their corresponding HTML tags:
        - '<h1>': class="text-4xl"
        - '<ul>': class="list-disc pl-8 list-outside"
        - '<ol>': class="list-decimal pl-8 list-outside"
        - '<code>': class="bg-base-200"
        - '<hr>': class="border-t border-base-content/25"

    **JSON Schema:**
    {
      "title": "string",
      "content": "string"
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": document_text}
            ]
        )
        output = response.choices[0].message.content.strip()
        parsed = safe_parse_json(output)
        return ensure_json_output(parsed)
    except Exception as e:
        return json.dumps({"error": f"Summary generation failed: {str(e)}"}, indent=2)


def generate_flashcards(document_text: str) -> str:
    """Generate flashcards from a document text."""
    system_prompt = """
    Generate a set of at least 10 flashcards based on the file provided.

    **Content Rules:**
    - Flashcards must be derived solely from the provided document.
    - The 'front' of each card must be a key term, name, or concept.
    - The 'back' of each card must be its corresponding definition or explanation.

    **JSON Schema:**
    {
      "title": "string",
      "flashcards": [
        {
          "front": "string",
          "back": "string"
        }
      ]
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": document_text}
            ]
        )
        output = response.choices[0].message.content.strip()
        parsed = safe_parse_json(output)
        return ensure_json_output(parsed)
    except Exception as e:
        return json.dumps({"error": f"Flashcard generation failed: {str(e)}"}, indent=2)


def generate_quiz(document_text: str) -> str:
    """Generate a quiz from a document text."""
    system_prompt = """
    Generate a quiz with at least 10 questions based on the file provided.

    **Content Rules:**
    - Questions must be derived solely from the provided text.
    - For multiple-choice questions, create plausible but incorrect distractor options.
    - The correctAnswers array must contain the 0-based index of the correct option.

    **JSON Schema:**
    {
      "title": "string",
      "quiz_content": [
        {
          "question": "string",
          "description": "string (can be empty)",
          "options": ["string"],
          "correctAnswers": [number]
        }
      ]
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": document_text}
            ]
        )
        output = response.choices[0].message.content.strip()
        parsed = safe_parse_json(output)
        return ensure_json_output(parsed)
    except Exception as e:
        return json.dumps({"error": f"Quiz generation failed: {str(e)}"}, indent=2)
