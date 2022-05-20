import pandas as pd
import numpy as np
from scipy.stats import pearsonr, ttest_ind

from Utils.config import staged_studies, get_project_path
from Utils.datasets import get_datasets_staged_intersections

res_in = []
res_out = []
for i, s1 in enumerate(staged_studies):
    for s2 in staged_studies[i+1:]:
        data1, data2 = get_datasets_staged_intersections([s1, s2])
        if len(data1.columns) <= 10:
            continue
        cancer1 = data1.loc[data1["cancer"] == 1]
        cancer1 = cancer1.loc[cancer1["stage"] >= 3].iloc[:, :-2]
        controls1 = data1.loc[data1["cancer"] == 0].iloc[:, :-2]
        cancer2 = data2.loc[data2["cancer"] == 1]
        cancer2 = cancer2.loc[cancer2["stage"] >= 3].iloc[:, :-2]
        controls2 = data2.loc[data2["cancer"] == 0].iloc[:, :-2]
        if len(cancer1) == 0 or len(cancer2) == 0:
            continue
        fold_change_1 = cancer1.mean() - controls1.mean()
        fold_change_2 = cancer2.mean() - controls2.mean()
        res_in.append(pearsonr(fold_change_1, fold_change_2)[0])
        cancer1 = data1.loc[data1["cancer"] == 1]
        cancer1 = cancer1.loc[cancer1["stage"] < 3].iloc[:, :-2]
        controls1 = data1.loc[data1["cancer"] == 0].iloc[:, :-2]
        cancer2 = data2.loc[data2["cancer"] == 1]
        cancer2 = cancer2.loc[cancer2["stage"] < 3].iloc[:, :-2]
        controls2 = data2.loc[data2["cancer"] == 0].iloc[:, :-2]
        if len(cancer1) == 0 or len(cancer2) == 0:
            continue
        fold_change_1 = cancer1.mean() - controls1.mean()
        fold_change_2 = cancer2.mean() - controls2.mean()
        res_out.append(pearsonr(fold_change_1, fold_change_2)[0])

ttest = ttest_ind(res_in, res_out)
df = pd.DataFrame(np.array([[np.mean(res_in), np.std(res_in, ddof=1), np.mean(res_out), np.std(res_out, ddof=1), ttest.statistic, ttest.pvalue]]), columns=["in-mean", "in-std", "out-mean", "out-std", "t-value", "p-value"])
df.to_csv(get_project_path() / "Outdata" / "log_fold_change_correlation_late.csv", index=False)