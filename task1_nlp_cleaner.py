import json
import re
from collections import Counter
from pathlib import Path

STOP_WORDS = {
    "a",
    "an",
    "the",
    "is",
    "on",
    "and",
    "do",
    "i",
    "my",
    "to",
    "from",
    "or",
    "can",
    "how",
    "what",
    "after",
    "in",
    "of",
    "for",
}


def clean_tickets(tickets: list[dict]) -> list[dict]:
    """Remove duplicate tickets and clean valid query text."""
    cleaned_tickets = []
    seen_ids = set()

    for ticket in tickets:
        ticket_id = ticket["ticket_id"]

        # Keep only the first occurrence of each ticket ID.
        if ticket_id in seen_ids:
            continue

        seen_ids.add(ticket_id)

        query = ticket.get("query")

        # Reject null values and other non-text values.
        if not isinstance(query, str):
            continue

        # Replace HTML tags with spaces so words stay separated.
        query = re.sub(r"<[^>]+>", " ", query)

        # Remove extra spaces, tabs, and line breaks.
        query = " ".join(query.split())

        if not query:
            continue

        # Preserve the original data by creating a new dictionary.
        cleaned_ticket = ticket.copy()
        cleaned_ticket["query"] = query
        cleaned_tickets.append(cleaned_ticket)

    return cleaned_tickets


# if __name__ == "__main__":
#     sample_tickets = [
#         {"ticket_id": "T-1", "query": " Hello<br>world!  "},
#         {"ticket_id": "T-1", "query": "Duplicate ticket"},
#         {"ticket_id": "T-2", "query": None},
#         {"ticket_id": "T-3", "query": " a  "},
#     ]

#     print(clean_tickets(sample_tickets))


def preprocess_text(text: str) -> list[str]:
    """Convert text into lowercase tokens without common stop words."""
    lowercase_text = text.lower()

    tokens = re.findall(r"[a-z0-9]+", lowercase_text)

    filtered_tokens = [token for token in tokens if token not in STOP_WORDS]

    return filtered_tokens


def analyze_tickets(cleaned_tickets: list[dict]) -> dict:
    """Summarize categories and token frequencies."""
    category_counts = Counter()
    keyword_counts = Counter()

    for ticket in cleaned_tickets:
        category_counts[ticket["category"]] += 1
        keyword_counts.update(ticket["tokens"])

    top_keywords = sorted(
        keyword_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[:5]

    return {
        "category_counts": dict(category_counts),
        "top_keywords": top_keywords,
    }


def main() -> None:
    data_directory = Path(__file__).resolve().parent / "data"
    input_path = data_directory / "support_tickets.json"
    output_path = data_directory / "cleaned_tickets.json"

    with input_path.open("r", encoding="utf-8") as file:
        tickets = json.load(file)

    cleaned_tickets = clean_tickets(tickets)

    for ticket in cleaned_tickets:
        ticket["tokens"] = preprocess_text(ticket["query"])

    summary = analyze_tickets(cleaned_tickets)

    print(f"Loaded tickets: {len(tickets)}")
    print(f"Cleaned tickets: {len(cleaned_tickets)}")

    print("\nTickets per category:")
    for category, count in sorted(summary["category_counts"].items()):
        print(f"  {category}: {count}")

    print("\nTop 5 keywords:")
    for keyword, count in summary["top_keywords"]:
        print(f"  {keyword}: {count}")

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(cleaned_tickets, file, indent=2, ensure_ascii=False)

    print(f"\nSaved cleaned tickets to: {output_path}")


if __name__ == "__main__":
    main()
