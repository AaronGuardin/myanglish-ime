import re


class InputNormalizer:
    """Normalize raw Myanglish input before transliteration."""

    def normalize(self, text: str) -> str:
        """
        Normalize Myanglish text.

        Steps:
        1. Convert to lowercase.
        2. Remove leading/trailing whitespace.
        3. Collapse repeated whitespace.
        """

        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text = text.lower()
        text = text.strip()

        # Convert multiple spaces into one space.
        text = re.sub(r"\s+", " ", text)

        return text