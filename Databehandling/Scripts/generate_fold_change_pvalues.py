import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

from Utils.config import studies, get_project_path, common_regulated
from Utils.datasets import get_datasets_intersections
from converters import canonical_to_seq

regulated_seq = canonical_to_seq(common_regulated)
np.random.seed(0)

real_p = []
random_p = []

for i, study_a in enumerate(studies):
    for j, study_b in enumerate(studies[i+1:]):
        j = i+j+1
        table_a, table_b = get_datasets_intersections([study_a, study_b])
        assert np.all(table_a.columns == table_b.columns)
        if len(table_a.columns) >= 10:
            cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
            control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
            cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
            control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
            fold_change_a = cancer_a.mean() - control_a.mean()
            fold_change_b = cancer_b.mean() - control_b.mean()
            corr1, p1 = pearsonr(fold_change_a, fold_change_b)
            shuffled_cols = np.copy(table_a.columns[:-1].to_numpy())
            np.random.shuffle(shuffled_cols)
            fold_change_a = cancer_a.loc[:, shuffled_cols].mean() - control_a.loc[:, shuffled_cols].mean()
            corr2, p2 = pearsonr(fold_change_a, fold_change_b)
            real_p.append(p1)
            random_p.append(p2)

print(real_p)
print(random_p)
