import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

from Utils.config import studies, get_project_path, common_regulated
from Utils.datasets import get_datasets_intersections
from converters import canonical_to_seq

np.random.seed(0)

real_p = []
mirna_shuffled_p = []
case_shuffled_p = []

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
            table_a["cancer"] = table_a["cancer"].sample(frac=1).values
            table_b["cancer"] = table_b["cancer"].sample(frac=1).values
            cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
            control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
            cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
            control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
            fold_change_a = cancer_a.mean() - control_a.mean()
            fold_change_b = cancer_b.mean() - control_b.mean()
            corr3, p3 = pearsonr(fold_change_a, fold_change_b)
            real_p.append(p1)
            mirna_shuffled_p.append(p2)
            case_shuffled_p.append(p3)

out_data = pd.DataFrame(np.array([real_p, mirna_shuffled_p, case_shuffled_p]).transpose(), columns=["real", "mirna-shuffled", "case-shuffled"])
out_data.to_csv(get_project_path() / "Outdata" / "log_fold_change_pvalues.csv", index=False)
