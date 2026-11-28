import pytest

from task1_nlp_cleaner import clean_tickets, preprocess_text


def test_duplicate_ticket_keeps_first_occurrence():
    tickets = [
        {"ticket_id": "T-1", "query": "First question"},
        {"ticket_id": "T-1", "query": "Second question"},
    ]

    result = clean_tickets(tickets)

    assert len(result) == 1
    assert result[0]["query"] == "First question"


@pytest.mark.parametrize("query", [None, "", " \t\n ", "<br>", " "])
def test_invalid_queries_are_removed(query):
    tickets = [{"ticket_id": "T-1", "query": query}]

    result = clean_tickets(tickets)

    assert result == []


def test_preprocessing_removes_stop_words_and_punctuation():
    text = "How do I reset my VPN password??"

    result = preprocess_text(text)

    assert result == ["reset", "vpn", "password"]


def test_cleaning_does_not_modify_original_ticket():
    original = {"ticket_id": "T-1", "query": " Hello<br>world! "}

    result = clean_tickets([original])

    assert original["query"] == " Hello<br>world! "
    assert result[0]["query"] == "Hello world!"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("days day", ["day", "day"]),
        (
            "companies company employees",
            ["company", "company", "employee"],
        ),
    ],
)
def test_preprocessing_normalizes_noun_forms(text, expected):
    assert preprocess_text(text) == expected
