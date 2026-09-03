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

def test_generate_thwar_variants():
    generator = VariantGenerator()

    variants = generator.generate("thwar")

    assert "thwar" in variants
    assert "twar" in variants
    assert "twr" in variants

def test_phrase_thwar_variants():
    generator = VariantGenerator()

    variants = generator.generate("ma thwar buu")

    assert "ma thwar buu" in variants
    assert "ma twar buu" in variants
    assert "ma twr buu" in variants

