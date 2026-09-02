import re


class VariantGenerator:
    """Generate likely canonical variants of Myanglish input."""

    def generate(self, text: str) -> list[str]:
        """
        Generate possible normalized variants.

        The original text is always included as the first variant.
        """

        variants = [text]

        collapsed = self._collapse_repeated_characters(text)

        if collapsed != text:
            variants.append(collapsed)

        return variants

    @staticmethod
    def _collapse_repeated_characters(text: str) -> str:
        """Collapse runs of 3 or more repeated characters to one."""

        return re.sub(r"(.)\1{2,}", r"\1", text)