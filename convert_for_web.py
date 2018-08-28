# Just the steps to compile Markdown files with YAML metadata and data, so that Jekyll can produce the HTML.


import pandas as pd
from collections import defaultdict
from glob import glob
from pathlib import Path
import chardet
import roman
import yaml


def save_as_yaml_md(data: dict, filename: str):
    """Save details for a manuscript in the YAML metadata of a Markdown file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(data, f, default_flow_style=False)
        f.write("\n---\n")


def contents_as_dicts(contents: pd.DataFrame):
    """"""
    return contents.to_dict(orient='records')


def convert_ms_to_dict(ser: pd.Series, contents, owners):
    """Create a dict of the cataloguing info and contents for a manuscript"""
    # print(ser.name)
    # print(ser.index)
    data = dict(ser.to_dict())
    data["MS_ID"] = ser.name
    # Split sources on ' ; '
    # print(data["MS_Sources"])
    data["sources"] = data["MS_Sources"].split(' ; ')
    del data["MS_Sources"]

    # If there is a contents file for this manuscript, include its contents
    if ser.name in contents.groups:
        data["contents"] = contents_as_dicts(contents.get_group(ser.name))

    # If there is a owners file for this manuscript, include its contents
    if ser.name in owners.groups:
        data["owners"] = contents_as_dicts(owners.get_group(ser.name))
    save_as_yaml_md(data, "docs/_details/ms_" + ser.name + ".md")
    # return data


def main():
    # Read list of manuscripts
    ms_descriptions = pd.read_csv("data/output/all_manuscripts.csv", index_col=0, na_values=[""], error_bad_lines=False)
    fill_values = {'MS_Sources': "",'Place_of_production': "",'Produced_for': "",'F_%': 0.,'L_%': 0.,'E_%': 0.,'O_%': 0.,'F_Sides': 0.,'L_Sides': 0.,'E_Sides': 0.,'O_Sides': 0.,'total_sides_English': 0.,'total_sides_French': 0.,'total_sides_Latin': 0.,'total_sides_Other': 0.,'percentage_English': 0.,'percentage_French': 0.,'percentage_Latin': 0.,'percentage_Other': 0.}
    ms_descriptions.fillna(fill_values, inplace=True)

    all_mss = pd.read_csv('data/output/all_contents.csv', encoding="utf-8")
    all_mss_grouped = all_mss.groupby("MS_ID")

    all_owners = pd.read_csv('data/output/all_owners.csv', encoding="utf-8", dtype={'MS_ID': str, 'owner_ID': int, 'owner_descr': str, 'owner_date': str, 'owner_type': str, 'owner_gender': str, 'owner_source': str}, na_values=[""], error_bad_lines=False)
    all_owners_grouped = all_owners.groupby("MS_ID")
    ms_descriptions.apply(convert_ms_to_dict, axis=1, contents=all_mss_grouped, owners=all_owners_grouped)


if __name__ == '__main__':
    main()
