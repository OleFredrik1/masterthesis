import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections


zero_auc = []
non_zero_auc = []
for s1 in studies:
    for s2 in studies:
        if s1 == s2:
            continue
        data1, data2 = get_datasets_intersections([s1, s2], zero_mean_fold_change=True)
        if len(data1.columns[:-1]) < 10:
            continue
        logreg = LogisticRegression(max_iter=1000, penalty="none")
        logreg.fit(data1.iloc[:, :-1], data1["cancer"])
        zero_auc.append(roc_auc_score(data2["cancer"], logreg.predict_proba(data2.iloc[:, :-1])[:, 1]))
        data1, data2 = get_datasets_intersections([s1, s2], zero_mean_fold_change=False)
        logreg = LogisticRegression(max_iter=1000, penalty="none")
        logreg.fit(data1.iloc[:, :-1], data1["cancer"])
        non_zero_auc.append(roc_auc_score(data2["cancer"], logreg.predict_proba(data2.iloc[:, :-1])[:, 1]))

ttest = ttest_ind(zero_auc, non_zero_auc)
pd.DataFrame([[np.mean(non_zero_auc), np.std(non_zero_auc, ddof=1), np.mean(zero_auc), np.std(zero_auc, ddof=1), ttest.statistic, ttest.pvalue]], columns=["mean (non-zero mean FC)", "std (non-zero mean FC)", "mean (zero mean FC)", "std (zero mean FC)", "t-value", "p-value"]).to_csv(get_project_path() / "Outdata" / "auc_zero_mean_fold_change.csv", index=False)