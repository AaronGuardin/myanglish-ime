from difflib import SequenceMatcher


class FuzzyMatcher:
    """Find similar Myanglish words using similarity scoring."""

    def __init__(
        self,
        dictionary_words: list[str],
        threshold: float = 0.7,
    ):
        self.dictionary_words = dictionary_words
        self.threshold = threshold

    def find_matches(
        self,
        text: str,
        limit: int = 5,
    ) -> list[tuple[str, float]]:
        """Return similar dictionary words ranked by similarity."""

        matches: list[tuple[str, float]] = []

        for word in self.dictionary_words:
            score = SequenceMatcher(
                None,
                text,
                word,
            ).ratio()

            if score >= self.threshold:
                matches.append((word, score))

        matches.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return matches[:limit]