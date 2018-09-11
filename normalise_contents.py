
import pandas as pd
from glob import glob
from pathlib import Path
import chardet
import roman

# Normalise file encoding and remove extraneous columns


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
    if not pd.isna(mss['start_side']).any():
        mss['start_side'] = mss['start_side'].str.strip()
        mss['end_side'] = mss['end_side'].str.strip()
    # print("Fixing folio numbers")
    mss = mss.apply(fix_range_ends, axis=1)
    mss['start_folio'] = pd.to_numeric(mss['start_folio'], errors='ignore')
    mss['end_folio'] = pd.to_numeric(mss['end_folio'], errors='ignore')
    return mss


def extract_ms_id(filename):
    base_name = Path(filename).stem
    return base_name.split('_')[1]


def process_manuscript(filename: str):
    file = Path(filename).name
    parent_dir = Path(filename).parent.parent
    output_dir = parent_dir / "normalised"
    output_dir.mkdir(exist_ok=True)

    # print("Trying to open")
    mss = load_contents(filename)

    mss.to_csv(output_dir / file, encoding="utf-8")

    ms_id = extract_ms_id(filename)

    return mss, ms_id


def main():
    files = list(glob('data/input/contents_*.csv'))
    ms_identifiers = []
    contents_frames = []
    for filename in files:
        print("Working on", filename)
        try:
            frames = process_manuscript(filename)
            contents_frames.append(frames[0])
            ms_identifiers.append(frames[1])
            print("Done")
        except Exception as e:
            print("ERROR in {0}: {1}".format(filename, e))
    all_mss = pd.concat(contents_frames, keys=ms_identifiers, names=["MS_ID"])
    all_mss.to_csv('data/normalised/all_contents.csv', encoding="utf-8")


if __name__ == '__main__':
    main()
