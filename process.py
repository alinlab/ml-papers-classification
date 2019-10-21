import os
import json

RAW_DIRS = ["raw/icml17"]#, "icml_raw/icml18", "icml_raw/icml19"]
PROCESSED_DIR = "data"
category_dict = {
    "Deep Learning : Analysis": [["Deep Learning"], ["Analysis"]],
    "Deep Learning : Backprop": [["Deep Learning"], ["Backprop"]],
    "Deep Learning : Fisher Approximations": [["Deep Learning"], ["Fisher Approximations"]],
    "Deep Learning : Hardware": [["Deep Learning"], ["Hardware"]], 
    "Deep Learning : Invariances": [["Deep Learning"], ["Invariances"]],
    "Deep Learning : Learning To Learn": [["Deep Learning"], ["Learning To Learn"]],
    "Deep Learning : Metalearning": [["Deep Learning"], ["Meta Learning"]],
    "Deep Learning : Probabilistic": [["Deep Learning"], ["Probabilistic"]],
    "Game Theory And Multiagents": [["Game Theory", "Multi-Agents"]],
    "Semisupervised And Curriculum Learning": [["Semi-Supervised Learning", "Curriculum Learning"]],
    "Transfer And Multitask Learning": [["Transfer Learning", "Multi-Task Learning"]]
}

def extract_category(line):
    line = line[:-1]
    if line in category_dict:
        category = category_dict[line]
    else:
        category = [[line]]
    
    return category

os.makedirs(PROCESSED_DIR, exist_ok=True)
paper_id = 0
categories = set()
for raw_dir in RAW_DIRS:
    with open(os.path.join(raw_dir, "papers_categories.txt"), "r") as f: 
        while True:
            line = f.readline()
            if not line:
                break
            
            category = extract_category(line)
            for c in category:
                categories = categories.union(set(c))

    with open(os.path.join(raw_dir, "papers_info.txt"), "r") as f:
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

            paper_path = os.path.join(PROCESSED_DIR, "{:04d}.json".format(paper_id))
            with open(paper_path, "w") as f2:
                json.dump(paper, f2)

categories = sorted(list(categories))
categories_path = os.path.join(PROCESSED_DIR, "categories.json")
with open(categories_path, "w") as f2:
    json.dump(categories, f2)