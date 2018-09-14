# Language analysis in manuscripts

This repository contains code and some accompanying documentation to support analysis of languages used in manuscripts.
The scripts also allow you to create a simple website using [GitHub Pages][ghp].

[ghp]: https://pages.github.com/

The code reads CSV files that contain information on texts in a manuscript, with for each text a title (optional),
language and start and end indication. It produces a new CSV file that contains the number of folio sides for
each text, correcting for sides that contain multiple texts.

It depends on [pandas](https://pandas.pydata.org/) for working with CSV files and doing the analyses.
The included [Jupyter](https://jupyter.org/) notebook is the first proof of concept.

## Character encodings

This programme tries to auto-detect the input character encoding using the [`chardet`][chardet] library and writes output using the UTF-8 encoding.

[chardet]: https://github.com/chardet/chardet

## Installation

The code doesn't need to be installed, other than downloaded to a suitable location. You may need to install dependencies.

### Use Python 3 in a virtualenv

To prevent interference with existing Python 3 installations, you should create a `virtualenv` for this project. This
example creates a virtualenv in `~/virtualenvs/` called `manuscript-stats`:

```bash
virtualenv ~/virtualenvs/manuscript-stats
source ~/virtualenvs/manuscript-stats/bin/activate
```

In your git tree, clone the repository and install the required dependencies:

```bash
git clone https://github.com/LeidenUniversityLibraries/manuscript-stats.git
cd manuscript-stats/
pip install -r requirements.txt
```

## Usage

### LanguageAnalysis.py

The main script is `LanguageAnalysis.py`. It reads the main overview of manuscripts and their metadata from `manuscripts.csv`
and the lists of contents for each manuscript from individual files named `contents_XXX.csv`, where XXX is the manuscript identifier used in the overview.

This script expects all input files to be in `data/input/`.

```bash
python LanguageAnalysis.py
```

When run, this command prints the name of the file it is working on and creates a normalised version in `data/output/`, if
the operations succeed. If something went wrong, the error is printed.

It also creates (in `data/output/`):

- `all_manuscripts.csv`: the main output that is a combination of the input `manuscripts.csv` and the calculated language coverage for each manuscript
- `all_contents.csv`: a concatenation of all normalised `contents_XXX.csv` files with page ranges converted to ordinal numbers and the total number of pages for each text calculated
- `all_languages.csv`: for each manuscript, this contains one row per language and the number of pages for that language
- `all_langs_pivot.csv`: a pivoted version of the `all_languages.csv` table with columns for absolute and relative numbers of pages in French, English, Latin and other languages

### normalise_owners.py

The `normalise_owners.py` script reads files named `owners_XXX.csv`, where again XXX is the manuscript identifier, and
creates both normalised copies and a concatenation of all normalised files named `all_owners.csv`. The information about owners
is not currently used in analyses, but it is presented in the web version of the results.

This script reads input files from `data/input/` and writes to `data/output/`.

### convert_for_web.py

The `convert_for_web.py` script reads the `all_manuscripts.csv`, `all_contents.csv` and `all_owners.csv` files and generates
a Markdown file for each manuscript with all structured data included in the YAML metadata. Using Jekyll (for example, as
provided by GitHub pages) you can create a web presentation of the manuscripts and the analysis results.

The script reads the files from `data/output/` and creates the Markdown files in `docs/_details/`.

## Notes on input files

In the development of these scripts, we encountered a few things about the input files that may require extra attention.

- When you use Microsoft Excel to prepare the CSV files, make sure the files don't have empty lines.

- Ranges of Roman numerals are handled by converting to their Arabic equivalents and adding 100000, so that the numbers don't
clash with the folia numbered in Arabic ranges. This doesn't work when there are multiple ranges of Roman numerals, but in
this dataset we are not aware of any.

- Do not mix folio numbering (`1r`, `3v`) with pagination (`1`, `6`) in one file.

## Author, licence

Created by Ben Companjen at the Centre for Digital Scholarship, Leiden University Libraries.
Copyright 2018, Leiden University Libraries.

This project is not yet licenced.
