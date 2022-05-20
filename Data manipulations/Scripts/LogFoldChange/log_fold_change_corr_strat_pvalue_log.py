from collections import defaultdict
from importlib.metadata import metadata
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, ttest_ind

from Utils.config import get_project_path, studies
from Utils.datasets import get_datasets_intersections

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

in_data = []
for i, s1 in enumerate(studies):
    for s2 in studies[i+1:]:
        table_a, table_b = get_datasets_intersections([s1, s2])
        if len(table_a.columns) <= 10:
            continue
        cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
        control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
        cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
        control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
        fold_change_a = cancer_a.mean() - control_a.mean()
        fold_change_b = cancer_b.mean() - control_b.mean()
        corr, p = pearsonr(fold_change_a, fold_change_b)
        cur_tech = [metadata.loc[s1, "Technology"], metadata.loc[s2, "Technology"]]
        cur_bf = [metadata.loc[s1, "Body fluid"], metadata.loc[s2, "Body fluid"]]
        if cur_tech[0] == cur_tech[1] or cur_bf[0] == cur_bf[1]:
            in_data.append(p)

out = np.array([in_data, np.log(in_data)]).transpose()


df = pd.DataFrame(out, columns=["p-values", "log p-values"])
df.to_csv(get_project_path() / "Outdata" / "log_fold_change_corr_strat_pvalue_log.csv", index=False)