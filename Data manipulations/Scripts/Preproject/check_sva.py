import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
from tqdm import tqdm

from Utils.config import studies
from Utils.datasets import get_datasets_intersections



for study_a in ["Asakura2020", "Asakura2020_transformed", "Asakura2020_adjusted"]:
    p_vals = []
    for study_b in tqdm(studies[1:]):
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
            p_vals.append(p1)
    print(p_vals)
