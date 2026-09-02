import json
from pathlib import Path

from myanglish_ime.models import Candidate


class DictionaryRepository:
    """Load and query transliteration dictionary data."""

    def __init__(self, dictionary_path: Path):
        self.dictionary_path = dictionary_path
        self._data = self._load()

    def _load(self) -> dict:
        """Load dictionary JSON from disk."""

        if not self.dictionary_path.exists():
            raise FileNotFoundError(
                f"Dictionary not found: {self.dictionary_path}"
            )

        with self.dictionary_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def lookup(self, text: str) -> list[Candidate]:
        """Return candidates for input text."""

        entries = self._data.get(text, [])

        return [
            Candidate(
                input_text=text,
                output_text=entry["output"],
                score=entry.get("score", 1.0),
            )
            for entry in entries
        ]

    def words(self) -> list[str]:
        """Return all dictionary input keys."""

        return list(self._data.keys())    