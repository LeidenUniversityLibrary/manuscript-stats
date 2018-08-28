
import pandas as pd
from collections import defaultdict
from glob import glob
from pathlib import Path
import chardet
import roman
import yaml


def load_owners(filename: str):
    with open(filename, 'rb') as input_file:
        detected_encoding = chardet.detect(input_file.read())
        # owners = pd.read_csv(filename, encoding=detected_encoding['encoding'].lower(), index_col=0, usecols=[0, 1, 2, 3, 4, 5, 6], dtype={'item': int, 'title': str, 'language': str, 'start_folio': str, 'start_side': str, 'end_folio': str, 'end_side': str}, na_values=[""], error_bad_lines=False)
        owners = pd.read_csv(filename, encoding=detected_encoding['encoding'].lower(), index_col=0, na_values=[""], error_bad_lines=False)
    # print("Dropping empty rows")
    owners = owners.dropna(how='all')
    return owners


def extract_ms_id(filename):
    base_name = Path(filename).stem
    return base_name.split('_')[1]


def process_owners(filename: str):
    file = Path(filename).name
    parent_dir = Path(filename).parent.parent
    output_dir = parent_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # print("Trying to open")
    owners = load_owners(filename)

    owners.to_csv(output_dir / file, encoding="utf-8")

    ms_id = extract_ms_id(filename)


    return owners, ms_id


def main():
    files = list(glob('data/input/owner_*.csv'))
    ms_identifiers = []
    contents_frames = []
    for filename in files:
        print("Working on", filename)
        try:
            frames = process_owners(filename)
            contents_frames.append(frames[0])
            ms_identifiers.append(frames[1])
            print("Done")
        except Exception as e:
            print("ERROR in {0}: {1}".format(filename, e))
    all_owners = pd.concat(contents_frames, keys=ms_identifiers, names=["MS_ID"])
    all_owners.to_csv('data/output/all_owners.csv', encoding="utf-8")


if __name__ == '__main__':
    main()
