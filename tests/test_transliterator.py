from pathlib import Path
from myanglish_ime.fuzzy import FuzzyMatcher
import pytest
from myanglish_ime.variants import VariantGenerator
from myanglish_ime.dictionary import DictionaryRepository
from myanglish_ime.normalizer import InputNormalizer
from myanglish_ime.transliterator import Transliterator


@pytest.fixture
def transliterator():
    normalizer = InputNormalizer()

    dictionary = DictionaryRepository(
        Path("data/dictionary.json")
    )

    variant_generator = VariantGenerator()

    fuzzy_matcher = FuzzyMatcher(
        dictionary_words=dictionary.words(),
        threshold=0.7,
    )

    return Transliterator(
        normalizer=normalizer,
        dictionary=dictionary,
        variant_generator=variant_generator,
        fuzzy_matcher=fuzzy_matcher,
    )


def test_transliterate_nay(transliterator):
    assert transliterator.transliterate("nay") == "နေ"


def test_transliterate_uppercase(transliterator):
    assert transliterator.transliterate("NAY") == "နေ"


def test_transliterate_with_spaces(transliterator):
    assert transliterator.transliterate("  kaung  ") == "ကောင်း"


def test_transliterate_lar(transliterator):
    assert transliterator.transliterate("lar") == "လား"


def test_unknown_word(transliterator):
    assert transliterator.transliterate("xyzabc") is None

def test_transliterate_phrase(transliterator):
    result = transliterator.transliterate("nay kaung lar")

    assert result == "နေကောင်းလား"


def test_transliterate_phrase_with_extra_spaces(transliterator):
    result = transliterator.transliterate(
        "  nay   kaung   lar  "
    )

    assert result == "နေကောင်းလား"


def test_word_by_word_fallback(transliterator):
    result = transliterator.transliterate("nay kaung")

    assert result == "နေကောင်း"

def test_candidates_are_ranked(transliterator):
    candidates = transliterator.candidates("ma")

    assert len(candidates) == 3
    assert candidates[0].output_text == "မ"
    assert candidates[0].score == 1.0
    assert candidates[1].output_text == "မှာ"
    assert candidates[2].output_text == "မာ"


def test_transliterate_selects_best_candidate(transliterator):
    result = transliterator.transliterate("ma")

    assert result == "မ"

def test_transliterate_repeated_characters(transliterator):
    result = transliterator.transliterate("kaunggg")

    assert result == "ကောင်း"


def test_original_word_still_works(transliterator):
    result = transliterator.transliterate("kaung")

    assert result == "ကောင်း"      

def test_transliterate_fuzzy_match(transliterator):
    result = transliterator.transliterate("kaong")

    assert result == "ကောင်း"

def test_exact_match_beats_fuzzy_match(transliterator):
    result = transliterator.transliterate("kaung")

    assert result == "ကောင်း"

def test_fuzzy_does_not_expand_phrase(transliterator):
    candidates = transliterator.candidates("nay kaung")

    assert all(
        candidate.output_text != "နေကောင်းလား"
        for candidate in candidates
    )

def test_unknown_word_in_phrase(transliterator):
    result = transliterator.transliterate("nay xyz")

    assert result is None
    
def test_transliterate_with_question_mark(transliterator):
    result = transliterator.transliterate("nay?")

    assert result == "နေ?"


def test_transliterate_with_exclamation_mark(transliterator):
    result = transliterator.transliterate("mingalarpar!")

    assert result == "မင်္ဂလာပါ!"


def test_transliterate_phrase_with_punctuation(transliterator):
    result = transliterator.transliterate("nay kaung lar?")

    assert result == "နေကောင်းလား?"        

def test_split_trailing_punctuation(transliterator):
    text, punctuation = transliterator._split_punctuation("nay?")

    assert text == "nay"
    assert punctuation == "?"

def test_transliterate_ma_shi_bu(transliterator):
    result = transliterator.transliterate("ma shi bu")

    assert result == "မရှိဘူး"

def test_transliterate_ma(transliterator):
    result = transliterator.transliterate("ma")

    assert result == "မ"


def test_transliterate_ma_shi_buu(transliterator):
    result = transliterator.transliterate("ma shi buu")

    assert result == "မရှိဘူး"


def test_transliterate_ma_shi_buu_with_punctuation(transliterator):
    result = transliterator.transliterate("ma shi buu!")

    assert result == "မရှိဘူး!"

def test_word_by_word_composition(transliterator):
    result = transliterator.transliterate("ma shi")
    assert result == "မရှိ"


def test_word_by_word_composition_with_punctuation(transliterator):
    result = transliterator.transliterate("shi buu!")
    assert result == "ရှိဘူး!"

def test_transliterate_thwar_variant(transliterator):
    result = transliterator.transliterate("ma twar buu")

    assert result == "မသွားဘူး"