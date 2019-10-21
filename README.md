# ml-papers-classification

This is dataset and source codes for category classification of (recent years) ML conference papers in {ICML, NeurIPS}.

## Label Formatting Information
There can exist multiple categories (first order of hierarchy): 
'''
CATEGORY = [[“Optimization”], [“Combinatorial Optimization”]]
'''
This means that category is both “optimization” and “combinatorial optimization”

There also exist noisy labels (second order of hierarchy):
'''
CATEGORY = [[“Semi-Supervised Learning”, “Transfer Learning”]]
'''
This means that category if one of “semi-supervised learning” or “transfer learning” (we do not know the answer)

In combination, 
'''
CATEGORY = [[“Optimization”], [“Semi-Supervised Learning”, “Transfer Learning”]]
'''
This means that category is “optimization” and one of “semi-supervised learning” or “transfer learning”
