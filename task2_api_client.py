import json
import logging

import requests

logger = logging.getLogger(__name__)


def transform_posts(posts: list[dict]) -> list[dict]:
    """Convert the first five API posts into document records."""
    documents = []

    for post in posts[:5]:
        body = post["body"]

        document = {
            "doc_id": post["id"],
            "title": post["title"].strip(),
            "content": body.replace("\n", " ").strip(),
            # "words": body.split(),
            "word_count": len(body.split()),
        }

        documents.append(document)

    return documents


def get_fallback_documents() -> list[dict]:
    """Return two clearly labelled mock documents."""
    mock_posts = [
        {
            "id": -1,
            "title": "Mock document: API unavailable",
            "body": "This is sample content used during an API failure.",
        },
        {
            "id": -2,
            "title": "Mock document: offline example",
            "body": "This document allows downstream processing to continue.",
        },
    ]

    return transform_posts(mock_posts)


def fetch_documents(
    url: str = "https://jsonplaceholder.typicode.com/posts",
) -> list[dict]:
    """Fetch documents, returning mock data if the request fails."""
    logger.info("Starting API request: %s", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        posts = response.json()

        if not isinstance(posts, list):
            raise ValueError("Expected a JSON list of posts.")

        for post in posts[:5]:
            if (
                not isinstance(post, dict)
                or not isinstance(post.get("id"), int)
                or not isinstance(post.get("title"), str)
                or not isinstance(post.get("body"), str)
            ):
                raise ValueError("A post has missing or invalid fields.")

        documents = transform_posts(posts)

        logger.info("Successfully fetched %d documents.", len(documents))
        return documents

    except requests.exceptions.Timeout:
        logger.error("The API request timed out.")

    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to the API.")

    except requests.exceptions.HTTPError as error:
        logger.error("The API returned an HTTP error: %s", error)

    except requests.exceptions.RequestException as error:
        logger.error("The API request failed: %s", error)

    except ValueError as error:
        logger.error("The API returned unusable data: %s", error)

    logger.warning("Using two mock fallback documents.")
    return get_fallback_documents()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    documents = fetch_documents()
    print(json.dumps(documents, indent=2))
