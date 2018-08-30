# coding: utf-8

# # Creating a manuscript catalogue
# 
# In this proof of concept, we are building an online catalogue of French manuscripts.


import pandas as pd
from collections import defaultdict
from glob import glob
from pathlib import Path
import chardet
import roman

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
            # print("Roman!")
            folio = roman.fromRoman(folio.upper())
            was_roman = True
        except:
            folio = int(folio)
    if folio < 1:
        raise NotImplementedError()
    if pd.isna(recto_verso):
        o = folio
    elif recto_verso == 'v':
        o = folio * 2
    elif recto_verso == 'r':
        o = folio * 2 - 1
    else:
        raise RuntimeError("Recto/Verso must be '', 'r' or 'v'")
    if was_roman:
        o += 100000
    return o


def fs2o(ser: pd.Series):
    """Add fields to series that contain start and end ordinal page numbers"""
    ser['ordinal_start'] = folio_side_to_ordinal(ser['start_folio'], ser['start_side'])
    ser['ordinal_end'] = folio_side_to_ordinal(ser['end_folio'], ser['end_side'])
    return ser


def fix_range_ends(ser: pd.Series):
    """If no end of range is specified, copy the beginning of the range"""
    if pd.isna(ser['end_folio']):
        ser['end_folio'] = ser['start_folio']
        ser['end_side'] = ser['start_side']
    return ser


def count_pages_for_text(ser: pd.Series, languages_per_page=None):
    if languages_per_page is None:
        languages_per_page = {}
    values = [1 / len(languages_per_page[p]) for p in range(ser['ordinal_start'], ser['ordinal_end'] + 1)]
    ser['total_sides'] = sum(values)
    return ser


# These results can be written back to a CSV file.

# To calculate the total sides and percentages for each language we need to group the rows by language.
# We also need the total number of sides.

def get_languages_per_page(mss: pd.DataFrame):
    languages_per_page = defaultdict(list)
    # print(mss)
    for row_index, text in mss.iterrows():
        for page in range(text['ordinal_start'], text['ordinal_end']+1):
            languages_per_page[page].append(text['language'])
    return languages_per_page


def extract_ms_id(filename):
    base_name = Path(filename).stem
    return base_name.split('_')[1]


def load_contents(filename: str):
    with open(filename, 'rb') as input_file:
        detected_encoding = chardet.detect(input_file.read())
        mss = pd.read_csv(filename, encoding=detected_encoding['encoding'].lower(), index_col=0, usecols=[0, 1, 2, 3, 4, 5, 6], dtype={'item': int, 'title': str, 'language': str, 'start_folio': str, 'start_side': str, 'end_folio': str, 'end_side': str}, na_values=[""], error_bad_lines=False)
    # print("Dropping empty rows")
    mss = mss.dropna(how='all')
    # Remove whitespace from language names, folio sides
    mss['language'] = mss['language'].str.strip()
    if not pd.isna(mss['start_side']).any():
        mss['start_side'] = mss['start_side'].str.strip()
        mss['end_side'] = mss['end_side'].str.strip()
    # print("Fixing folio numbers")
    mss = mss.apply(fix_range_ends, axis=1)
    mss['start_folio'] = pd.to_numeric(mss['start_folio'], errors='ignore')
    mss['end_folio'] = pd.to_numeric(mss['end_folio'], errors='ignore')
    return mss


def merge_analysis_results(all_manuscripts, all_langs_pivot):
    result = all_manuscripts.join(all_langs_pivot, how='left', on="MS_ID")
    return result


def process_manuscript(filename: str):
    file = Path(filename).name
    parent_dir = Path(filename).parent.parent
    output_dir = parent_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # print("Trying to open")
    mss = load_contents(filename)

    # Convert folio + side to ordinal numbers
    # print("before fs2o")
    mss = mss.apply(fs2o, axis=1)

    # print("before get languages")
    sides_languages = get_languages_per_page(mss)

    # print("Count!")
    mss = mss.apply(count_pages_for_text, axis=1, languages_per_page=sides_languages)
    mss.to_csv(output_dir / file, encoding="utf-8")

    # print("Save to HTML")
    ms_id = extract_ms_id(filename)
    # print("Summarise")
    grouped_by_language = mss.groupby('language')
    total_sides = mss['total_sides'].sum()

    # Summarise the use of languages and write the absolute number and ratio of pages per language
    # to a new CSV file
    sides_per_language = grouped_by_language.agg({'total_sides': sum})
    sides_per_language['percentage'] = sides_per_language['total_sides'].apply(lambda x: x / total_sides * 100)
    sides_per_language.to_csv(output_dir / file.replace("contents", "languages"), encoding="utf-8")

    return mss, sides_per_language, ms_id


def main():
    # Read list of manuscripts
    ms_descriptions = pd.read_csv("data/input/manuscripts.csv", index_col=False, na_values=[""], error_bad_lines=False)

    files = list(glob('data/input/contents_*.csv'))
    ms_identifiers = []
    contents_frames = []
    languages_frames = []
    for filename in files:
        print("Working on", filename)
        try:
            frames = process_manuscript(filename)
            contents_frames.append(frames[0])
            languages_frames.append(frames[1])
            ms_identifiers.append(frames[2])
            print("Done")
        except Exception as e:
            print("ERROR in {0}: {1}".format(filename, e))
    all_mss = pd.concat(contents_frames, keys=ms_identifiers, names=["MS_ID"])
    all_mss.to_csv('data/output/all_contents.csv', encoding="utf-8")

    all_languages = pd.concat(languages_frames, keys=ms_identifiers, names=["MS_ID"])

    all_languages.reset_index(inplace=True)
    print(all_languages.head())
    all_languages.to_csv("data/output/all_languages.csv", index=False, encoding="utf-8")
    all_langs_pivot = all_languages.pivot(index="MS_ID", columns="language")
    all_langs_pivot.columns = ['_'.join(col).strip() for col in all_langs_pivot.columns.values]
    print(all_langs_pivot.head())
    all_langs_pivot.to_csv("data/output/all_langs_pivot.csv", encoding="utf-8")
    merged_results = merge_analysis_results(ms_descriptions, all_langs_pivot)
    # Make sure empty values are sensible, i.e. empty spaces for strings and 0 for numbers
    fill_values = {'Place_of_production': "",'Produced_for': "", 'Notes': "", 'F_%': 0.,'L_%': 0.,'E_%': 0.,'O_%': 0.,'F_Sides': 0.,'L_Sides': 0.,'E_Sides': 0.,'O_Sides': 0.,'total_sides_English': 0.,'total_sides_French': 0.,'total_sides_Latin': 0.,'total_sides_Other': 0.,'percentage_English': 0.,'percentage_French': 0.,'percentage_Latin': 0.,'percentage_Other': 0.}
    merged_results.fillna(fill_values, inplace=True)
    merged_results.to_csv("data/output/all_manuscripts.csv", index_label="Item", encoding="utf-8")


if __name__ == '__main__':
    main()
