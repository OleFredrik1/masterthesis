import pandas as pd
import numpy as np
from scipy.stats import pearsonr, ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from Utils.config import staged_studies, get_project_path
from Utils.datasets import get_datasets_staged_intersections

aucs_in = []
aucs_out = []
for i, s1 in enumerate(staged_studies):
    for s2 in staged_studies:
        data1, data2 = get_datasets_staged_intersections([s1, s2])
        if len(data1.columns) <= 10 or (data1["stage"] >= 3).sum() == 0 \
             or (data2["stage"] >= 3).sum() == 0 \
             or data1["stage"].isin([1,2]).sum() == 0 \
             or data2["stage"].isin([1,2]).sum() == 0 \
             or s1 == s2:
            continue
        data1_in = data1[data1["stage"].isin([0,3,4])]
        data2_in = data2[data2["stage"].isin([0,3,4])]
        data1_out = data1[data1["stage"].isin([0,1,2])]
        data2_out = data2[data2["stage"].isin([0,1,2])]
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(data1_in.iloc[:, :-2], data1_in["cancer"])
        aucs_in.append(roc_auc_score(data2_in["cancer"], logreg.predict_proba(data2_in.iloc[:, :-2])[:, 1]))
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(data1_out.iloc[:, :-2], data1_out["cancer"])
        aucs_out.append(roc_auc_score(data2_out["cancer"], logreg.predict_proba(data2_out.iloc[:, :-2])[:, 1]))
        

ttest = ttest_ind(aucs_in, aucs_out)
df = pd.DataFrame(np.array([[np.mean(aucs_in), np.std(aucs_in, ddof=1), np.mean(aucs_out), np.std(aucs_out, ddof=1), ttest.statistic, ttest.pvalue]]), columns=["in-mean", "in-std", "out-mean", "out-std", "t-value", "p-value"])
df.to_csv(get_project_path() / "Outdata" / "auc_stages_pairs.csv", index=False)