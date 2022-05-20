from sklearn.linear_model import LogisticRegression
import numpy as np
from scipy.stats import pearsonr, ttest_ind
from scipy.special import betainc
import pandas as pd
import pickle

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections, get_dataset


# From https://stackoverflow.com/questions/24432101/correlation-coefficients-and-p-values-for-all-pairs-of-rows-of-a-matrix
def corrcoef(matrix):
    r = np.corrcoef(matrix)
    rf = r[np.triu_indices(r.shape[0], 1)]
    df = matrix.shape[1] - 2
    ts = rf * rf * (df / (1 - rf * rf))
    pf = betainc(0.5 * df, 0.5, df / (df + ts))
    p = np.zeros(shape=r.shape)
    p[np.triu_indices(p.shape[0], 1)] = pf
    p[np.tril_indices(p.shape[0], -1)] = p.T[np.tril_indices(p.shape[0], -1)]
    p[np.diag_indices(p.shape[0])] = np.zeros(p.shape[0])
    return r, p


res_zero = []
res_non_zero = []
for s1 in studies:
    row_non_zero = []
    row_zero = []
    for s2 in studies:
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns[:-1]) < 4:
            row_non_zero.extend(len(data2)*[-1])
            row_zero.extend(len(data2)*[-1])
            continue
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(data1.iloc[:, :-1], data1["cancer"])
        row_non_zero.extend(logreg.predict_proba(data2.iloc[:, :-1])[:, 1].tolist())
        data1, data2 = get_datasets_intersections([s1, s2], zero_mean_fold_change=True)
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(data1.iloc[:, :-1], data1["cancer"])
        row_zero.extend(logreg.predict_proba(data2.iloc[:, :-1])[:, 1].tolist())
    res_non_zero.append(np.array(row_non_zero))
    res_zero.append(np.array(row_zero))

res_non_zero = np.array(res_non_zero)
res_zero = np.array(res_zero)

r_non_zero = []
r_zero = []

for i in range(len(res_zero)):
    for j in range(i+1, len(res_zero)):
        mask = np.logical_and(res_zero[i] != -1, res_zero[j] != -1)
        if np.sum(mask) == 0:
            continue
        r_non_zero.append(np.corrcoef(res_non_zero[i, mask], res_non_zero[j, mask])[0, 1])
        r_zero.append(np.corrcoef(res_zero[i, mask], res_zero[j, mask])[0, 1])

r_non_zero = np.array(r_non_zero)
r_zero = np.array(r_zero)

ttest_r = ttest_ind(r_zero, r_non_zero)
ttest_r2 = ttest_ind(r_zero**2, r_non_zero**2)
pd.DataFrame([[np.mean(r_zero), np.std(r_zero, ddof=1), np.mean(r_non_zero), np.std(r_non_zero, ddof=1), ttest_r.statistic, ttest_r.pvalue], [np.mean(r_zero**2), np.std(r_zero**2, ddof=1), np.mean(r_non_zero**2), np.std(r_non_zero**2, ddof=1), ttest_r2.statistic, ttest_r2.pvalue]], columns=["mean (zero mean FC)", "std (zero mean FC)", "mean (non-zero mean FC)", "std (non-zero mean FC)", "t-value", "p-value"], index=["r", "r2"]).to_csv(get_project_path() / "Outdata" / "zero_mean_fold_change_predictions_correlation.csv", index_label="Type")

