from sklearn.metrics import roc_auc_score
import numpy as np
from tqdm import tqdm

from Utils.datasets import get_dataset
from Utils.config import studies, common_regulated
from converters import canonical_to_seq

common_seq = canonical_to_seq(common_regulated)

np.random.seed(0)
real_auc_scores = []
random_auc_scores = []

for i, study in enumerate(studies):
    table = get_dataset(study)
    common_intersect = np.array(list(set(table.columns[:-1]) & set(common_seq)))
    random_seq = np.random.choice(table.columns[:-1], size=len(common_intersect))
    real_auc_scores += [roc_auc_score(table["cancer"], table[r]) for r in common_intersect]
    random_auc_scores += [roc_auc_score(table["cancer"], table[r]) for r in random_seq]

print(real_auc_scores)
print(random_auc_scores)
