
import pandas as pd
from collections import defaultdict
from glob import glob
from pathlib import Path
import chardet
import roman
import yaml

# Going from folio side ID to an ordinal page number helps calculate the number of pages.
#
# - 1r = 1
# - 1v = 2
# - 2r = 3
# - 2v = 4
#
# etc. So multiply by 2 and subtract 1 if there's an `r` in the folio side ID.


# But these numbers do not account for sides with two or more texts – those sides count as 1 for each text.
#
# Instead, we can calculate how much of each side that is the start or end for a text should count for each language.
# Let's assume all texts on a side take equal parts of the side. Then if a side has two (parts of) English texts
# and one Latin text, the side counts as $1/3$ for each text.
#
# We need to create an index for all sides that contain the start and/or end of a text.


def folio_side_to_ordinal(folio, recto_verso):
    """Calculate the ordinal page number from folio number and recto/verso indication"""
    was_roman = False
    if type(folio) == str:
        try:
            folio = roman.fromRoman(folio.upper())
            was_roman = True
        except:
            folio = int(folio)
    if folio < 1:
        raise NotImplementedError()
    o = folio * 2
    if was_roman:
        o += 100000
    if recto_verso == 'r':
        o -= 1
    return o


def fs2o(ser: pd.Series):
    """Add fields to series that contain start and end ordinal page numbers"""
    if pd.isna(ser['start_side']):
        ser['ordinal_start'] = ser['start_folio']
        ser['ordinal_end'] = ser['end_folio']
    else:
        ser['ordinal_start'] = folio_side_to_ordinal(ser['start_folio'], ser['start_side'])
        ser['ordinal_end'] = folio_side_to_ordinal(ser['end_folio'], ser['end_side'])
    return ser


def fix_range_ends(ser: pd.Series):
    """If no end of range is specified, copy the beginning of the range"""
    if pd.isna(ser['end_folio']):
        ser['end_folio'] = ser['start_folio']
        ser['end_side'] = ser['start_side']
    return ser


def load_contents(filename: str):
    with open(filename, 'rb') as input_file:
        detected_encoding = chardet.detect(input_file.read())
        mss = pd.read_csv(filename, encoding=detected_encoding['encoding'].lower(), index_col=0, usecols=[0, 1, 2, 3, 4, 5, 6], dtype={'item': int, 'title': str, 'language': str, 'start_folio': str, 'start_side': str, 'end_folio': str, 'end_side': str}, na_values=[""], error_bad_lines=False)
    # print("Dropping empty rows")
    mss = mss.dropna(how='all')
    # Remove whitespace from language names
    mss['language'] = mss['language'].str.strip()
    # print("Fixing folio numbers")
    mss = mss.apply(fix_range_ends, axis=1)
    mss['start_folio'] = pd.to_numeric(mss['start_folio'], errors='ignore')
    mss['end_folio'] = pd.to_numeric(mss['end_folio'], errors='ignore')
    return mss