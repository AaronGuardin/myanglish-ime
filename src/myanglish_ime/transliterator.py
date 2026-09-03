import re
from myanglish_ime.dictionary import DictionaryRepository
from myanglish_ime.fuzzy import FuzzyMatcher
from myanglish_ime.models import Candidate
from myanglish_ime.normalizer import InputNormalizer
from myanglish_ime.variants import VariantGenerator


class Transliterator:
    """Convert Myanglish input into Myanmar Unicode."""

    @staticmethod
    def _split_punctuation(text: str) -> tuple[str, str]:
        """Separate trailing punctuation from transliteration input."""
        match = re.match(r"^(.*?)([.!?,。！？]*)$", text)
        if not match:
            return text, ""
        return match.group(1), match.group(2)

    def __init__(
        self,
        normalizer: InputNormalizer,
        dictionary: DictionaryRepository,
        variant_generator: VariantGenerator,
        fuzzy_matcher: FuzzyMatcher,
    ):
        self.normalizer = normalizer
        self.dictionary = dictionary
        self.variant_generator = variant_generator
        self.fuzzy_matcher = fuzzy_matcher

    def candidates(self, text: str) -> list[Candidate]:
        """Return ranked transliteration candidates."""
        clean_text, _ = self._split_punctuation(text)
        normalized_text = self.normalizer.normalize(clean_text)

        if not normalized_text:
            return []

        seen_outputs: set[str] = set()
        all_candidates: list[Candidate] = []

        # 1. Exact lookup using generated variants.
        for variant in self.variant_generator.generate(normalized_text):
            dict_candidates = self.dictionary.lookup(variant)
            for cand in dict_candidates:
                if cand.output_text not in seen_outputs:
                    seen_outputs.add(cand.output_text)
                    all_candidates.append(cand)

        if all_candidates:
            return sorted(all_candidates, key=lambda c: c.score, reverse=True)

        # 2. Fuzzy matching fallback.
        fuzzy_matches = self.fuzzy_matcher.find_matches(normalized_text)
        input_word_count = len(normalized_text.split())

        for matched_word, similarity_score in fuzzy_matches:
            if len(matched_word.split()) != input_word_count:
                continue

            matched_candidates = self.dictionary.lookup(matched_word)
            for candidate in matched_candidates:
                if candidate.output_text not in seen_outputs:
                    seen_outputs.add(candidate.output_text)

                    all_candidates.append(
                        Candidate(
                            input_text=normalized_text,
                            output_text=candidate.output_text,
                            score=candidate.score * similarity_score,
                            source="fuzzy",
                        )
                    )

        return sorted(all_candidates, key=lambda c: c.score, reverse=True)

    def transliterate(self, text: str) -> str | None:
        """Return the highest-ranked transliteration result."""
        if not text:
            return None

        clean_text, punctuation = self._split_punctuation(text)
        normalized_text = self.normalizer.normalize(clean_text)

        if not normalized_text:
            return None

        # 1. Full phrase translation
        candidates = self.candidates(normalized_text)
        if candidates:
            return candidates[0].output_text + punctuation

        # 2. Word-by-word fallback
        words = normalized_text.split()
        if len(words) <= 1:
            return None

        output_words: list[str] = []
        for word in words:
            word_candidates = self.candidates(word)
            if not word_candidates:
                return None
            output_words.append(word_candidates[0].output_text)

        return "".join(output_words) + punctuation