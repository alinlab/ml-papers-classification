import os
import json

RAW_DIRS = ["raw/icml16"] #["raw/icml16", "raw/icml17", "raw/icml18", "raw/icml19"]
PROCESSED_DIR = "data"
category_dict = {
    # icml 16
    "Applications and Time-Series Analysis": [["Applications", "Time-Series Analysis"]],
    "Approximate Inference": [["Approximate Inference"]],
    "Bandit Problems": [["Bandit Problems"]],
    "Bayesian Nonparametric Methods": [["Baysian Methods"], ["Nonparametric Methods"]],
    "Causal Inference": [["Causal Inference"]],
    "Clustering": [["Clustering"]],
    "Crowdsourcing and Interactive Learning": [
        ["Crowdsourcing", "Interactive Learning"]
    ],
    "Dimensionality Reduction / Private Learning": [
        ["Dimensionality Reduction", "Private Learning"]
    ],
    "Feature Selection and Dimensionality Reduction": [
        ["Feature Selection", "Dimensionality Reduction"]
    ],
    "Gaussian Processes": [["Gaussian Processes"]],
    "Graph Analysis/ Spectral Methods": [["Graph Analysis", "Spectral Methods"]],
    "Graphical Models": [["Graphical Models"]],
    "Kernel Methods": [["Kernel Methods"]],
    "Large Scale Learning and Big Data": [["Large Scale Learning", "Big Data"]],
    "Learning Theory": [["Learning Theory"]],
    "Machine Learning Applications": [["Machine Learning Applications"]],
    "Matrix Factorization / Neuroscience Applications": [
        ["Matrix Factorization", "Neuroscience Applications"]
    ],
    "Matrix Factorization and Related Topics": [["Matrix Factorization"]],
    "Metric and  Manifold Learning / Kernel Methods": [
        ["Metric Learning", "Manifold Learning", "Kernel Methods"]
    ],
    "Monte Carlo Methods": [["Monte Carlo Methods"]],
    "Multi-label, multi-task, and neural networks": [
        ["Multi-Label Learning", "Multi-Task Learning"],
        ["Deep Learning"],
    ],
    "Neural Networks and Deep Learning": [["Deep Learning"]],
    "Neural Networks and Deep Learning&nbsp;I": [["Deep Learning"]],
    "Neural Networks and Deep Learning&nbsp;II": [["Deep Learning"]],
    "Neural Networks and Deep Learning&nbsp;II (Computer Vision)": [
        ["Deep Learning"],
        ["Computer Vision"],
    ],
    "Online Learning": [["Online Learning"]],
    "Optimization": [["Optimization"]],
    "Optimization (Combinatorial)": [["Optimization"], ["Combinatorial Optimization"]],
    "Optimization (Continuous)": [["Optimization"], ["Continuous Optimization"]],
    "Optimization / Online Learning": [["Optimization", "Online Learning"]],
    "Privacy, Anonymity, and Security": [["Privacy", "Anonymity", "Security"]],
    "Ranking and Preference Learning": [["Ranking", "Preference Learning"]],
    "Reinforcement Learning": [["Reinforcement Learning"]],
    "Sampling / Kernel Methods": [["Sampling", "Kernel Methods"]],
    "Sparsity and Compressed Sensing": [["Sparsity", "Compressed Sensing"]],
    "Statistical Learning Theory": [["Statistical Learning Theory"]],
    "Structured Prediction / Monte Carlo Methods": [
        ["Structured Prediction", "Monte Carlo Methods"]
    ],
    "Supervised Learning": [["Supervised Learning"]],
    "Transfer Learning / Learning Theory": [["Transfer Learning", "Learning Theroy"]],
    "Unsupervised Learning / Applications": [["Unsupervised Learning", "Applications"]],
    "Unsupervised Learning / Representation Learning": [
        ["Unsupervised Learning", "Representation Learning"]
    ],
    # icml17
    "Deep Learning : Analysis": [["Deep Learning"], ["Analysis"]],
    "Deep Learning : Backprop": [["Deep Learning"], ["Backprop"]],
    "Deep Learning : Fisher Approximations": [
        ["Deep Learning"],
        ["Fisher Approximations"],
    ],
    "Deep Learning : Hardware": [["Deep Learning"], ["Hardware"]],
    "Deep Learning : Invariances": [["Deep Learning"], ["Invariances"]],
    "Deep Learning : Learning To Learn": [["Deep Learning"], ["Learning To Learn"]],
    "Deep Learning : Metalearning": [["Deep Learning"], ["Meta Learning"]],
    "Deep Learning : Probabilistic": [["Deep Learning"], ["Probabilistic"]],
    "Game Theory And Multiagents": [["Game Theory", "Multi-Agents"]],
    "Semisupervised And Curriculum Learning": [
        ["Semi-Supervised Learning", "Curriculum Learning"]
    ],
    "Transfer And Multitask Learning": [["Transfer Learning", "Multi-Task Learning"]],
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

print("Processed {} papers with {} categories".format(paper_id, len(categories)))
