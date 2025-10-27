# README

**About:** This source code is meant to run and call LLM API services using GPT 4o mini. This is part of our project where we also aim to evaluate the performance of the previous QuickEase v1 app which used GPT 4o-mini model as their primary LLM, as compared to our project QuickEase v2 (which is a revamp of the v1) where we used two models Gemini 2.5 flash and Gemini 2.0 flash as our primary and secondary LLM to provide AI-powered services that are the main functionalities included in the app.

**Rules:**

1. Only modify a few lines at `main.py`, which requires inputting the material's file path.
2. You may explore the entire source code freely but DO NOT modify other files. Contact the owner Christine Mosqueda if you want to suggest modifications or if you want to clarify something.

**How to use in your local machine?**

1. Fork this repo on github.

   1. Open the repository page on GitHub.
   2. Click the Fork button (top-right). This creates a copy under your GitHub account.

2. Clone your fork to your local machine.

   ```
   # Example (use your fork URL)
   git clone https://github.com/your-username/quickease-llm-service.git
   cd quickease-llm-service
   ```

3. Create and activate a Python virtual environment, make sure you have py 3.8+ installed.

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   You should see **(venv)** at the start of your prompt when activated.

4. Install dependencies. On the terminal with venv active, run `pip install -r requirements.txt`

5. Create your own **.env** because this source code expects environment variables for sensitive data (API key, base url). Ask the owner for the BASE_URL and how to get OPENAI_API_KEY if you don't know how to.

   The contents inside your **.env** file should look exactly like this:

   ```
   OPENAI_API_KEY=YOUR_API_KEY_HERE
   BASE_URL=https://base-url-endpoint
   ```

6. If not already included in requirements.txt, install spaCy model. On the terminal, run `python -m spacy download en_core_web_sm`

7. Edit `main.py` to point to a PDF file that you want to test. Double check the existence of file(s) inside the **materials/** directory.

   ```
   pdf_path = "./materials/IAS Notes.pdf"
   ```

8. Run the project. On the terminal, enter `python main.py`
   You should see the pipeline run:
   - PDF extraction → tokenization
   - 3 LLM calls (summary, flashcards, quiz)
   - JSON outputs printed to console
