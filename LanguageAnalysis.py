# coding: utf-8

# # Creating a manuscript catalogue
# 
# In this proof of concept, we are building an online catalogue of French manuscripts.


import pandas as pd
from collections import defaultdict
from glob import glob
from pathlib import Path

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
    o = folio * 2
    if recto_verso == 'r':
        o -= 1
    return o


def fs2o(ser):
    """Add fields to series that contain start and end ordinal page numbers"""
    ser['ordinal_start'] = folio_side_to_ordinal(ser['start_folio'], ser['start_side'])
    ser['ordinal_end'] = folio_side_to_ordinal(ser['end_folio'], ser['end_side'])
    return ser


def count_sides_better(ser, sides_languages=None):
    if sides_languages is None:
        sides_languages = {}
    ser['count_in_between'] = max(ser['ordinal_end'] - 1 - ser['ordinal_start'], 0)
    ser['count_start'] = 1 / len(sides_languages[ser['ordinal_start']])
    ser['count_end'] = 1 / len(sides_languages[ser['ordinal_end']])
    ser['correction'] = 0
    if ser['ordinal_start'] == ser['ordinal_end']:
        ser['correction'] -= ser['count_end']
    ser['corrected_total_sides'] = ser['count_in_between'] + ser['count_start'] + ser['count_end'] + ser['correction']
    return ser


# These results can be written back to a CSV file.

# To calculate the total sides and percentages for each language we need to group the rows by language.
# We also need the total number of sides.


def process_manuscript(filename):
    file = Path(filename).name
    parent_dir = Path(filename).parent
    output_dir = parent_dir / "output"
    output_dir.mkdir(exist_ok=True)

    mss = pd.read_csv(filename)
    mss = mss.apply(fs2o, axis=1)

    sides_languages = defaultdict(list)
    for row_index, text in mss.iterrows():
        sides_languages[text['ordinal_start']].append(text['language'])
        if text['ordinal_start'] != text['ordinal_end']:
            sides_languages[text['ordinal_end']].append(text['language'])

    sorted(sides_languages.items())
    mss = mss.apply(count_sides_better, axis=1, sides_languages=sides_languages)
    mss.to_csv(output_dir / file, index=False)
    grouped_by_language = mss.groupby('language')
    total_sides = mss['corrected_total_sides'].sum()

    grouped_by_language['corrected_total_sides'].sum()

    sides_per_language = grouped_by_language.agg({'corrected_total_sides': sum})
    sides_per_language['ratio'] = sides_per_language['corrected_total_sides'].apply(lambda x: x / total_sides * 100)


def main():
    for filename in glob('data/contents_*.csv'):
        print("Working on", filename)
        try:
            process_manuscript(filename)
            print("Done")
        except Exception as e:
            print(e)



if __name__ == '__main__':
    main()
