import os

def save_result_as_text(result_text, result_type, source_path):
    """
    Saves the result text (summary, flashcards, or quiz) into a .txt file.
    The output file is saved inside a 'results' directory.
    File name format: <source_name>_<result_type>.txt
    """

    # Ensure the 'results' directory exists
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    # Extract base filename (e.g. 'IAS Notes' from './materials/IAS Notes.pdf')
    base_name = os.path.splitext(os.path.basename(source_path))[0]

    # Create filename based on source and result type
    file_name = f"{base_name}_{result_type}.txt"
    file_path = os.path.join(results_dir, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result_text if isinstance(result_text, str) else str(result_text))
        print(f"Saved {result_type} result to: {file_path}")
    except Exception as e:
        print(f"Failed to save {result_type} result: {e}")
