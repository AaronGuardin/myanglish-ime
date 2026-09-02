from myanglish_ime.variants import VariantGenerator


def test_original_text_is_preserved():
    generator = VariantGenerator()

    variants = generator.generate("kaung")

    assert variants == ["kaung"]


def test_repeated_characters_generate_variant():
    generator = VariantGenerator()

    variants = generator.generate("kaunggg")

    assert variants == ["kaunggg", "kaung"]


def test_double_characters_are_preserved():
    generator = VariantGenerator()

    variants = generator.generate("kaa")

    assert variants == ["kaa"]


def test_multiple_repeated_sequences():
    generator = VariantGenerator()

    variants = generator.generate("naayyy")

    assert variants == ["naayyy", "naay"]