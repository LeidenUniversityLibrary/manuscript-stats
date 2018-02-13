# Language analysis in manuscripts

This repository contains code and some accompanying documentation to support analysis of languages used in manuscripts.

The code reads CSV files that contain information on texts in a manuscript, with for each text a title (optional),
language and start and end indication. It produces a new CSV file that contains the number of folio sides for
each text, correcting for sides that contain multiple texts.

It depends on [pandas](https://pandas.pydata.org/) for working with CSV files and doing the analyses.
The included [Jupyter]() notebook is the first proof of concept.

## Installation

The code doesn't need to be installed, other than downloaded to a suitable location. You may need to install dependencies.

### Use Python 3 in a virtualenv

To prevent interference with existing Python 3 installations, you should create a `virtualenv` for this project.

```bash
git clone https://github.com/LeidenUniversityLibraries/manuscript-stats.git
cd manuscript-stats/
```

## Usage

Copy your CSV files to `data/`, using the filename pattern `contents_XXX.csv` (where XXX is an identifier, like a number).

```bash
python LanguageAnalysis.py
```

This command prints the name of the file it is working on and creates an output file of the same name in `output/`, if
the operations succeed. If something went wrong, the error is printed.

## Author, licence

Created by Ben Companjen at the Centre for Digital Scholarship, Leiden University Libraries.
Copyright 2018, Leiden University Libraries.

This project is not yet licenced.
