import pytest

from myanglish_ime.normalizer import InputNormalizer


@pytest.fixture
def normalizer():
    return InputNormalizer()


def test_lowercase(normalizer):
    assert normalizer.normalize("NAY") == "nay"


def test_trim_whitespace(normalizer):
    assert normalizer.normalize("   nay   ") == "nay"


def test_collapse_spaces(normalizer):
    assert normalizer.normalize("nay    kaung") == "nay kaung"


def test_repeated_characters_are_preserved(normalizer):
    assert normalizer.normalize("nayyyyy") == "nayyyyy"


def test_invalid_type(normalizer):
    with pytest.raises(TypeError):
        normalizer.normalize(123)