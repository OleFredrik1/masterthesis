from collections import defaultdict
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, ttest_ind

from Utils.config import get_project_path, studies
from Utils.datasets import get_datasets_intersections

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)
technologies = list(set(t for t in metadata["Technology"] if list(metadata["Technology"]).count(t) > 2))
body_fluids = list(set(t for t in metadata["Body fluid"] if list(metadata["Body fluid"]).count(t) > 2))
res = defaultdict(list)

in_data = []
out_data = []
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
        if metadata.loc[s1, "Technology"] == metadata.loc[s2, "Technology"] or metadata.loc[s1, "Body fluid"] == metadata.loc[s2, "Body fluid"]:
            in_data.append(corr)
        else:
            out_data.append(corr) 

ttest = ttest_ind(in_data, out_data)
out = [[np.mean(in_data), np.std(in_data, ddof=1), np.mean(out_data), np.std(out_data, ddof=1), ttest.statistic, ttest.pvalue]]
df = pd.DataFrame(np.array(out), columns=["mean IG", "std IG", "mean OG", "std OG", "t-value", "p-value"])
df.to_csv(get_project_path() / "Outdata" / "log_fold_change_corr_strat_all.csv", index=False)