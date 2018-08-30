from LanguageAnalysis import fs2o
import pandas as pd
import numpy as np


def test_roman_ordinal():
    """Roman numerals used as ordinal numbers should also be converted to the 100000+ range"""
    ser = pd.Series([1,'Additional leaf of the Wroxham continuation in a different hand','French','i',np.nan,'i',np.nan], index=['item','title','language','start_folio','start_side','end_folio','end_side'])
    assert 100001 == fs2o(ser)['ordinal_start']
