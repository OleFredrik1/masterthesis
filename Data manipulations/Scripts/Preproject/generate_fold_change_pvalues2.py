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
        table_a, table_b = get_datasets_intersections([study_a, study_b], True)
        assert np.all(table_a.columns == table_b.columns)
        if len(table_a.columns) >= 10:
            cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
            control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
            cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
            control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
            fold_change_a = cancer_a.mean() - control_a.mean()
            fold_change_b = cancer_b.mean() - control_b.mean()
            corr1, p1 = pearsonr(fold_change_a, fold_change_b)
            if corr1 < 0 and p1 < 0.05:
                print(study_a, study_b, corr1, p1)
