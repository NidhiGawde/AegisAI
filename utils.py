
import json
import re


def parse_json_response(response: str) -> dict:
    """Parse JSON even when the LLM wraps it in Markdown fences."""

    cleaned = response.strip()

    # Remove Markdown code fences
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Could not parse JSON response:\n{response}"
        ) from error







