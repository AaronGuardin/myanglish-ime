from myanglish_ime.dictionary import DictionaryRepository
from myanglish_ime.fuzzy import FuzzyMatcher
from myanglish_ime.models import Candidate
from myanglish_ime.normalizer import InputNormalizer
from myanglish_ime.variants import VariantGenerator


class Transliterator:
    """Convert Myanglish input into Myanmar Unicode."""

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

        normalized_text = self.normalizer.normalize(text)

        all_candidates: list[Candidate] = []

        # 1. Exact lookup using generated variants.
        for variant in self.variant_generator.generate(normalized_text):
            candidates = self.dictionary.lookup(variant)
            all_candidates.extend(candidates)

        # If exact candidates exist, prefer them.
        if all_candidates:
            return sorted(
                all_candidates,
                key=lambda candidate: candidate.score,
                reverse=True,
            )

        # 2. Fuzzy matching fallback.
        fuzzy_matches = self.fuzzy_matcher.find_matches(
            normalized_text
        )

        for matched_word, similarity_score in fuzzy_matches:
            matched_candidates = self.dictionary.lookup(
                matched_word
            )

            for candidate in matched_candidates:
                all_candidates.append(
                    Candidate(
                        input_text=normalized_text,
                        output_text=candidate.output_text,
                        score=candidate.score * similarity_score,
                        source="fuzzy",
                    )
                )

        return sorted(
            all_candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

    def transliterate(self, text: str) -> str | None:
        """Return the highest-ranked transliteration result."""

        normalized_text = self.normalizer.normalize(text)

        words = normalized_text.split()

        # Word-by-word exact match check condition
        if len(words) > 1:
            exact_words: list[str] = []
            for word in words:
                word_candidates: list[Candidate] = []
                for variant in self.variant_generator.generate(word):
                    word_candidates.extend(self.dictionary.lookup(variant))
                
                if word_candidates:
                    best_candidate = sorted(
                        word_candidates,
                        key=lambda candidate: candidate.score,
                        reverse=True,
                    )[0]
                    exact_words.append(best_candidate.output_text)
                else:
                    break

            if len(exact_words) == len(words):
                return "".join(exact_words)

        candidates = self.candidates(normalized_text)

        if candidates:
            return candidates[0].output_text

        if len(words) <= 1:
            return None

        output_words: list[str] = []

        for word in words:
            word_candidates = self.candidates(word)

            if not word_candidates:
                return None

            output_words.append(word_candidates[0].output_text)

        return "".join(output_words)