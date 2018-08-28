from LanguageAnalysis import count_pages_for_text, get_languages_per_page
import pandas as pd


def test_single_page():
    """A single page counts as 1"""
    content = pd.Series({'ordinal_start': 10, 'ordinal_end': 10})
    total_languages = {10: ["French"]}
    obs = count_pages_for_text(content, total_languages)
    assert 1 == obs['corrected_total_sides']


def test_count_single_range():
    """Simple range without overlap with other page ranges"""
    content = pd.Series({'ordinal_start': 1, 'ordinal_end': 10})
    total_languages = {}
    for l in range(1, 11):
        total_languages[l] = ["French"]
    obs = count_pages_for_text(content, total_languages)
    assert 10 == obs['corrected_total_sides']


def test_count_double_range():
    """Two ranges that overlap with each other each count half"""
    content = pd.Series({'ordinal_start': 1, 'ordinal_end': 10})
    total_languages = {}
    for l in range(1, 11):
        total_languages[l] = ["French", "Latin"]
    obs = count_pages_for_text(content, total_languages)
    assert 5 == obs['corrected_total_sides']


def test_get_sides_languages():
    """sides_languages should have an entry for each page in a page range"""
    content = pd.DataFrame({'ordinal_start': [1,1], 'ordinal_end': [10,10], 'language': ["French", "Latin"]})
    obs = get_languages_per_page(content)
    assert 10 == len(obs)
