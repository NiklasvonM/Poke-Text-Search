import pytest

from poketextsearch.scraping import clean_string_for_url


@pytest.mark.parametrize(
    ["name", "expected"],
    [
        ("Bulbasaur", "Bulbasaur"),
        ("Farfetch'd", "Farfetch%27d"),
        ("Mr. Mime", "Mr._Mime"),
        ("Mime Jr.", "Mime_Jr"),
        ("Nidoran♀", "Nidoran"),
        ("Nidoran♂", "Nidoran"),
        ("Flabébé", "Flab%C3%A9b%C3%A9"),
        ("Type:_Null", "Type_Null"),
    ],
)
def test_clean_string_for_url(name: str, expected: str) -> None:
    result = clean_string_for_url(name)
    assert result == expected
