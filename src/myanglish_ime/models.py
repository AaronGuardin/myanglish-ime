from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    """A Myanmar transliteration candidate."""

    input_text: str
    output_text: str
    score: float = 1.0
    source: str = "dictionary"