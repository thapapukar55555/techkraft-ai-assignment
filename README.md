# TechKraft AI Intern Take-Home Assignment

A Python project covering support-ticket cleaning, basic NLP,
public API integration and AI safety concepts.

## Project structure

```text
techkraft-ai-assignment/
├── data/
│   ├── support_tickets.json
│   └── cleaned_tickets.json
├── tests/
│   ├── test_nlp_cleaner.py
│   └── test_api_client.py
├── task1_nlp_cleaner.py
├── task2_api_client.py
├── ANSWERS.md
├── requirements.txt
└── .gitignore
```

Tested locally with Python 3.11.5 on Windows.

GitHub Actions is configured to run Ruff checks, formatting checks
and pytest on Python 3.11 after pushes and pull requests.

## Setup

The following commands use Windows PowerShell. Run them from the
project's root folder.

Create an isolated Python environment:

```powershell
py -m venv .pukarvenv
```

Install dependencies using that environment:

```powershell
.\.pukarvenv\Scripts\python.exe -m pip install -r requirements.txt
```

Download the WordNet dictionary used for noun lemmatization:

```powershell
.\.pukarvenv\Scripts\python.exe -m nltk.downloader wordnet
```

The initial WordNet download requires an internet connection. Once the
data is installed, lemmatization and the automated tests can run offline.
GitHub Actions downloads WordNet before running checks.

No paid API key is required. The live API example needs an internet
connection; the automated API tests use mocked responses.

## Part 1: Ticket cleaning and NLP

```powershell
.\.pukarvenv\Scripts\python.exe task1_nlp_cleaner.py
```

The script:

- Keeps the first occurrence of each ticket ID.
- Removes invalid queries and cleans HTML tags and whitespace.
- Extracts lowercase alphanumeric tokens and removes stop words.
- Applies basic noun lemmatization using NLTK WordNet.
- Prints category counts and the five most frequent keywords.
- Writes cleaned records and tokens to `data/cleaned_tickets.json`.

Expected results for the supplied dataset:

- Input records: 9
- Cleaned records: 6
- Categories: IT 3, HR 2, Finance 1
- Top keywords: day (2), vpn (2), cannot (1), company (1), connect (1)

## Part 2: API client

```powershell
.\.pukarvenv\Scripts\python.exe task2_api_client.py
```

The client requests posts from JSONPlaceholder and transforms the
first five into records containing:

- `doc_id`
- `title`
- `content`
- `word_count`

It uses a request timeout, checks HTTP status codes, validates response
structure and logs progress and failures.

Handled request or response failures return two clearly labelled mock
documents in the same output format.

## Tests

```powershell
.\.pukarvenv\Scripts\python.exe -m pytest -q
```

The current suite contains 14 checks covering:

- Duplicate removal and invalid queries.
- Text preprocessing and preservation of original input.
- Noun lemmatization of plural and singular word forms.
- Successful API formatting and the five-post limit.
- The configured request timeout.
- Fallback behavior for HTTP errors, timeouts and connection failures.
- Logging of the fallback warning.

Mocked HTTP responses keep tests independent of internet availability.

## Design decisions and limitations

- Cleaning, preprocessing, analysis and API transformation are separate
  functions so their behavior can be tested independently.
- Keyword-frequency ties are sorted alphabetically for reproducibility.
- Tokenization targets the English sample data and splits hyphenated
  words into separate tokens.
- HTML cleanup handles simple tags in the supplied dataset.
- Basic noun lemmatization groups variants such as "days" and "day".
  Tokens are treated as nouns without contextual part-of-speech tagging,
  so this does not normalize every verb or resolve ambiguous words.
- Fallback documents use negative IDs and explicit mock titles so they
  are distinguishable from real API posts.

## Written answers

See `ANSWERS.md` for the HR assistant prompts, RAG chunking strategy
and prompt-injection defenses.

## Development note

Tests should be run with `python -m pytest` from the project root.
Running a test file directly from the `tests` directory can prevent
imports of the project modules.