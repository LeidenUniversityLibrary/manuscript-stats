import pytest
from LanguageAnalysis import folio_side_to_ordinal


def test_folio_side_to_ordinal_positive():
    assert 1 == folio_side_to_ordinal(1, 'r')
    assert 2 == folio_side_to_ordinal(1, 'v')

def test_folio_side_to_ordinal_negative():
    with pytest.raises(NotImplementedError):
        folio_side_to_ordinal(-1,'r')

def test_roman_folio_numbers():
    pass