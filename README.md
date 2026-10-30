Ticket Triage POC

A small proof of concept that classifies IT service desk tickets into categories, using keyword rules first and a Large Language Model (LLM) for the ambiguous cases.

I built it to explore a question that many service desks face: how can we sort incoming tickets automatically, while keeping a human in control when the answer is not clear?

The idea
ticket ──► rules (keywords)
              ├── one clear category ──► done
              └── Need_review ──► LLM (Gemini)
                                     ├── confident answer ──► category + reason
                                     └── not sure ──► human review
Rules first: fast, free and predictable. They handle the simple tickets.
LLM for ambiguous tickets: it reads the meaning of the ticket, not just the words, and explains its choice.
Human in the loop: when neither the rules nor the model are sure, the ticket is escalated as Need_review instead of being guessed.
Categories

Network, Hardware, Software, Security, Access, Email, and Need_review for tickets that are too vague or match several categories.

What it does today
1. Rule-based classifier (triage.py)
Reads 20 fictional tickets from tickets.csv (semicolon-separated, UTF-8).
Combines the title and description, and looks for category keywords.
Returns a category only when exactly one category matches.
Returns Need_review when no category matches, when several match, or when the ticket is too short.
evaluate() compares each prediction with the expected category and prints a score.

Result with rules only: [X]/20

2. Unit tests (test_triage.py)

pytest tests check three behaviours: a clear ticket gets its category, an ambiguous ticket goes to Need_review, and a too-short ticket goes to Need_review.

3. LLM classification (ai_classify.py)
Sends a ticket and a fixed list of allowed categories to the Gemini API.
Forces a JSON response with three fields: category, confidence (high / low) and reason.
Example: "Excel crashes when connected to the VPN" is classified as Network by the rules (they only see the word "VPN"), but as Software by the LLM, with the reason: "The user is experiencing issues with the Excel application crashing when connected to the VPN."
What I learned from the errors

The rules fail in three typical ways:

Missing keywords: easy to fix, but adding too many keywords overfits the test set.
Ambiguous labels: some tickets could reasonably belong to two categories.
Real limits of keyword matching: the rules read words, not meaning. A ticket mentioning "mails" and "virus" matches both Email and Security. This is where the LLM adds value.
Project structure
ticket-triage-poc/
├── tickets.csv        # 20 fictional tickets with their expected category
├── triage.py          # keyword rules + evaluation
├── test_triage.py     # pytest unit tests
├── ai_hello.py        # first call to the Gemini API
├── ai_classify.py     # LLM classification with JSON output
└── .env               # API key (not committed)
How to run it
bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install the dependencies
pip install google-genai python-dotenv pytest

# 3. Add your Gemini API key in a .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. Run the rule-based evaluation
python3 triage.py

# 5. Run the tests
pytest -v

# 6. Try the LLM classification
python3 ai_classify.py


