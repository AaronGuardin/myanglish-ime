from pathlib import Path

from myanglish_ime.dictionary import DictionaryRepository


def test_lookup_existing_word():
    path = Path("data/dictionary.json")

    dictionary = DictionaryRepository(path)

    candidates = dictionary.lookup("nay")

    assert len(candidates) == 1
    assert candidates[0].output_text == "နေ"


def test_lookup_unknown_word():
    path = Path("data/dictionary.json")

    dictionary = DictionaryRepository(path)

    candidates = dictionary.lookup("unknownword")

    assert candidates == []