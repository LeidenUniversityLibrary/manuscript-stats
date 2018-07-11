# Language analysis in manuscripts

This repository contains code and some accompanying documentation to support analysis of languages used in manuscripts.

The code reads CSV files that contain information on texts in a manuscript, with for each text a title (optional),
language and start and end indication. It produces a new CSV file that contains the number of folio sides for
each text, correcting for sides that contain multiple texts.

It depends on [pandas](https://pandas.pydata.org/) for working with CSV files and doing the analyses.
The included [Jupyter](https://jupyter.org/) notebook is the first proof of concept.

## Character encodings

This programme tries to auto-detect the input character encoding using the `chardet` library and writes output using the UTF-8 encoding.

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

Copy your CSV files to `data/input/`, using the filename pattern `contents_XXX.csv` (where XXX is an identifier, like a number).

```bash
python LanguageAnalysis.py
```

This command prints the name of the file it is working on and creates an output file of the same name in `data/output/`, if
the operations succeed. If something went wrong, the error is printed.

### Notes on input files

When you use Microsoft Excel to prepare the CSV files, make sure the files don't have empty lines.

Ranges of Roman numerals are handled by converting to their Arabic equivalents and adding 100000, so that the numbers don't
clash with the folia numbered in Arabic ranges. This doesn't work when there are multiple ranges of Roman numerals, but in
this dataset we are not aware of any.

Do not mix folio numbering (`1r`, `3v`) with pagination (`1`, `6`) in one file.

## Author, licence

Created by Ben Companjen at the Centre for Digital Scholarship, Leiden University Libraries.
Copyright 2018, Leiden University Libraries.

This project is not yet licenced.
