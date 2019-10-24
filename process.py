import os
import json
from icml_category_dict import (
    category_dict_icml15,
    category_dict_icml16,
    category_dict_icml17,
    category_dict_icml18,
    category_dict_icml19,
)

ICML_DIRS = [
    "raw/icml16",
    "raw/icml16",
    "raw/icml17",
    "raw/icml18",
    "raw/icml19"
]
NIPS_DIRS = [
    "raw/nips16",
    "raw/nips17",
    "raw/nips18",
]
PROCESSED_DIR = "data"

icml_category_dict = dict()
icml_category_dict.update(category_dict_icml15)
icml_category_dict.update(category_dict_icml16)
icml_category_dict.update(category_dict_icml17)
icml_category_dict.update(category_dict_icml18)
icml_category_dict.update(category_dict_icml19)


def extract_category(line):
    line = line[:-1]
    if line in icml_category_dict:
        category = icml_category_dict[line]
    else:
        words = line.split(" | ")
        category = [[nips_category_dict.get(w, w) for w in words]]

    return category


os.makedirs(PROCESSED_DIR, exist_ok=True)
paper_id = 0
categories = set()
for icml_dir in ICML_DIRS:
    with open(os.path.join(icml_dir, "papers_categories.txt"), "r") as f:
        while True:
            line = f.readline()
            if not line:
                break

            category = extract_category(line)
            for c in category:
                categories = categories.union(set(c))

    with open(os.path.join(icml_dir, "papers_info.txt"), "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            paper = dict()
            paper["title"] = line[:-1]
            paper["url"] = f.readline()[:-1]
            paper["category"] = extract_category(f.readline())
            paper["content"] = f.readline()[:-1]
            f.readline()
            paper_id += 1

            paper_path = os.path.join(
                PROCESSED_DIR, "{:04d}.json".format(paper_id)
            )
            with open(paper_path, "w") as f2:
                json.dump(paper, f2)

categories = sorted(list(categories))
categories_path = os.path.join(PROCESSED_DIR, "categories.json")
with open(categories_path, "w") as f2:
    json.dump(categories, f2)

for nips_dir in NIPS_DIRS:
    with open(os.path.join(nips_dir, "papers_info.txt"), "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            paper = dict()
            paper["title"] = line[:-1]
            paper["url"] = f.readline()[:-1]
            paper["category"] = []
            paper["content"] = f.readline()[:-1]
            f.readline()
            paper_id += 1

            paper_path = os.path.join(
                PROCESSED_DIR, "{:04d}.json".format(paper_id)
            )
            with open(paper_path, "w") as f2:
                json.dump(paper, f2)
    

print(
    "Processed {} papers with {} categories".format(paper_id, len(categories))
)
