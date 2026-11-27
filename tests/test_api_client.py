from unittest.mock import Mock, patch

import pytest
import requests

from task2_api_client import fetch_documents


def test_success_returns_first_five_formatted_documents():
    response = Mock()
    response.raise_for_status.return_value = None

    response.json.return_value = [
        {
            "id": number,
            "title": "  Example post  ",
            "body": "First line.\nSecond line.",
        }
        for number in range(1, 7)
    ]

    with patch(
        "task2_api_client.requests.get",
        return_value=response,
    ) as mock_get:
        documents = fetch_documents()

    assert len(documents) == 5
    assert [document["doc_id"] for document in documents] == [1, 2, 3, 4, 5]

    assert documents[0] == {
        "doc_id": 1,
        "title": "Example post",
        "content": "First line. Second line.",
        "word_count": 4,
    }

    mock_get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts",
        timeout=10,
    )


def test_http_error_returns_two_fallback_documents():
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )

    with patch(
        "task2_api_client.requests.get",
        return_value=response,
    ):
        documents = fetch_documents()

    assert len(documents) == 2
    assert [document["doc_id"] for document in documents] == [-1, -2]

    for document in documents:
        assert set(document) == {"doc_id", "title", "content", "word_count"}
        assert document["title"].startswith("Mock document:")


@pytest.mark.parametrize(
    "error",
    [
        requests.exceptions.Timeout("Request took too long"),
        requests.exceptions.ConnectionError("Network unavailable"),
    ],
)
def test_network_failure_returns_fallback_documents(error, caplog):
    with patch(
        "task2_api_client.requests.get",
        side_effect=error,
    ):
        documents = fetch_documents()

    assert len(documents) == 2
    assert [document["doc_id"] for document in documents] == [-1, -2]
    assert "Using two mock fallback documents." in caplog.text
