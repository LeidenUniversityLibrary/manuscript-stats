import pytest
from LanguageAnalysis import folio_side_to_ordinal


def test_folio_side_to_ordinal_positive():
    assert 1 == folio_side_to_ordinal(1, 'r')
    assert 2 == folio_side_to_ordinal(1, 'v')


def test_folio_side_to_ordinal_negative():
    with pytest.raises(NotImplementedError):
        folio_side_to_ordinal(-1, 'r')


def test_roman_folio_numbers():
    # This is a hack: I expect that no manuscript page number in the Arabic range will go over 100000.
    # By adding 100000 to the converted Roman numeral I can use the same data structures without getting messy.
    # I also expect that in any given manuscript there is only one range with Roman numerals, i.e. any Roman folio
    # number will at most appear once in a manuscript.
    assert 100001 == folio_side_to_ordinal('I', 'r')
    assert 100001 == folio_side_to_ordinal('i', 'r')
    assert 100020 == folio_side_to_ordinal('x', 'v')
