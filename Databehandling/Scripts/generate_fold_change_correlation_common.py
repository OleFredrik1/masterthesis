import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

from Utils.config import studies, get_project_path, common_regulated
from Utils.datasets import get_datasets_intersections
from converters import canonical_to_seq

regulated_seq = canonical_to_seq(common_regulated)

general_corr = []
special_corr = []
general_p = []
special_p = []
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
            intersect_common = np.array(list(set(table_a.columns[:-1]) & set(regulated_seq)))
            if len(intersect_common) > 2:
                fold_change_a = cancer_a.loc[:, intersect_common].mean() - control_a.loc[:, intersect_common].mean()
                fold_change_b = cancer_b.loc[:, intersect_common].mean() - control_b.loc[:, intersect_common].mean()
                corr2, p2 = pearsonr(fold_change_a, fold_change_b)
                general_corr.append(corr1)
                special_corr.append(corr2)
                general_p.append(p1)
                special_p.append(p2)

print(general_corr)
print(special_corr)
print()
print(general_p)
print(special_p)