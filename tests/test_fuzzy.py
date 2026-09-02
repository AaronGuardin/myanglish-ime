from myanglish_ime.fuzzy import FuzzyMatcher


def test_find_similar_word():
    matcher = FuzzyMatcher(
        dictionary_words=[
            "nay",
            "kaung",
            "lar",
        ]
    )

    matches = matcher.find_matches("kaong")

    assert matches[0][0] == "kaung"


def test_no_match_below_threshold():
    matcher = FuzzyMatcher(
        dictionary_words=[
            "nay",
            "kaung",
            "lar",
        ],
        threshold=0.8,
    )

    matches = matcher.find_matches("xyz")

    assert matches == []


def test_results_are_ranked():
    matcher = FuzzyMatcher(
        dictionary_words=[
            "kaung",
            "kyaung",
            "nay",
        ],
        threshold=0.5,
    )

    matches = matcher.find_matches("kaong")

    assert matches[0][0] == "kaung"