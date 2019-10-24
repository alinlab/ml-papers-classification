# ml-papers-classification

This is dataset and source codes for category classification of (recent years) ML conference papers in {ICML, NeurIPS}. Currently, only ICML datasets are available for preprocessing. Run the preprocessing script to generate the dataset:

```
python process.py
```

The dataset is stored in the data folder with .json formats. Each paper is represented with dictionary of title, url, content and category.

## Category Formatting Information

The provided dataset is a multi-label dataset with possibly noisy labels. To provide information, we express each category in special format.

Specifically, there can exist multiple categories (first order of hierarchy): 

```
"category": [[“Optimization”], [“Combinatorial Optimization”]]
```

This means that category is both “optimization” and “combinatorial optimization”.

There also exist noisy labels (second order of hierarchy):

```
"category": [[“Semi-Supervised Learning”, “Transfer Learning”]]
```

This means that category if one of “semi-supervised learning” or “transfer learning” (we do not know the answer).

In combination, 

```
"category": [[“Optimization”], [“Semi-Supervised Learning”, “Transfer Learning”]]
```

This means that category is “optimization” and one of “semi-supervised learning” or “transfer learning”.

UNLABELED DATASET can exist, with category as follows:

```
"category": []
```