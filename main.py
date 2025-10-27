# Kani ra nga py file inyong hilabtan ug ipadagan,,, thankssss

import sys
import traceback
from pdf_utils import extract_text_from_pdf, tokenize_text
from llm_service import generate_summary, generate_flashcards, generate_quiz

def main():

    # i-modify lang ang path sa material na gusto ninyo ipaslak diri, example kaning IAS notes lugar
    pdf_path = "./materials/IAS Notes.pdf"

    # Text extraction and tokenization
    try:
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            raise ValueError("No text extracted from the PDF.")
        
        print("Tokenizing text into sentences...")
        tokens = tokenize_text(text)
        print(f"Extracted {len(tokens)} sentences.\n")
    
    except FileNotFoundError:
        print(f"Error: The file at {pdf_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred during PDF processing:")
        traceback.print_exc()
        sys.exit(1)

    # Feed text to LLM service
    results = {}

    # summary notes
    try:
        print("Generating summary from document...")
        results['summary'] = generate_summary(text)
        print("Successfully generated!\n")
    except Exception as e:
        print("An error occurred during summary generation:")
        traceback.print_exc()
        results['summary'] = {"error": str(e)}

    # flashcards
    try:
        print("Generating flashcards from document...")
        results['flashcards'] = generate_flashcards(text)
        print("Successfully generated!\n")
    except Exception as e:
        print("An error occurred during flashcard generation:")
        traceback.print_exc()
        results['flashcards'] = {"error": str(e)}

    # quiz
    try:
        print("Generating quiz from document...")
        results['quiz'] = generate_quiz(text)
        print("Successfully generated!\n")
    except Exception as e:
        print("An error occurred during quiz generation:")
        traceback.print_exc()
        results['quiz'] = {"error": str(e)}

    # Output results
    print("\n=== RESULTS ===")
    for key, value in results.items():
        print(f"\n--- {key.upper()} ---")
        print(value)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print("An unexpected error occurred:")
        traceback.print_exc()
        sys.exit(1)
