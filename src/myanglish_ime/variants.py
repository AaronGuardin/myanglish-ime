import itertools
import re


class VariantGenerator:
    """Generate likely canonical variants of Myanglish input."""

    # Bidirectional Mapping: 'twar' နှင့် 'twr' မှ 'thwar' သို့ ပြန်လည်ပြောင်းလဲနိုင်ရန်
    REPLACEMENTS: dict[str, list[str]] = {
        "thwar": ["twar", "twr"],
        "twar": ["thwar", "twr"],
        "twr": ["thwar", "twar"],
    }

    def generate(self, text: str) -> list[str]:
        """Generate possible normalized variants."""
        if not text:
            return []

        variants = [text]

        # ၁။ ၃ လုံးနှင့်အထက် ထပ်နေသော စာလုံးများကို ၁ လုံးတည်းသို့ လျှော့ချခြင်း
        collapsed = self._collapse_repeated_characters(text)
        if collapsed != text:
            variants.append(collapsed)

        # ၂။ Target စာလုံးများအတွက် Variant များ ထုတ်ပေးခြင်း
        for target in [text, collapsed]:
            variants.extend(self._generate_mapped_variants(target))

        return self._unique(variants)

    @staticmethod
    def _collapse_repeated_characters(text: str) -> str:
        """Collapse runs of 3 or more repeated characters to one."""
        return re.sub(r"(.)\1{2,}", r"\1", text)

    @classmethod
    def _generate_mapped_variants(cls, text: str) -> list[str]:
        """Generate canonical variants for phrases and words."""
        words = text.split()
        if not words:
            return []

        word_choices: list[list[str]] = []
        has_replacements = False

        for word in words:
            clean_word = re.sub(r"[^\w]", "", word)
            options = [word]

            if clean_word in cls.REPLACEMENTS:
                has_replacements = True
                for rep in cls.REPLACEMENTS[clean_word]:
                    replaced = re.sub(
                        r"\b" + re.escape(clean_word) + r"\b", rep, word
                    )
                    options.append(replaced)

            word_choices.append(cls._unique(options))

        if not has_replacements:
            return []

        variants = []
        for combo in itertools.product(*word_choices):
            candidate_phrase = " ".join(combo)
            if candidate_phrase != text:
                variants.append(candidate_phrase)

        return variants

    @staticmethod
    def _unique(variants: list[str]) -> list[str]:
        """Remove duplicate variants while preserving insertion order."""
        return list(dict.fromkeys(variants))