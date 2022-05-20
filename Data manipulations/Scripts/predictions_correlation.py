from sklearn.linear_model import LogisticRegression
import numpy as np
from scipy.stats import pearsonr
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


res = []
for s1 in studies:
    row = []
    for s2 in studies:
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns[:-1]) < 4:
            row.extend(len(data2)*[0.5])
            continue
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(data1.iloc[:, :-1], data1["cancer"])
        row.extend(logreg.predict_proba(data2.iloc[:, :-1])[:, 1].tolist())
    res.append(row)

row = []
for study in studies:
    data = get_dataset(study)
    row.extend(list(data["cancer"]))

res.append(row)
corr, pval = corrcoef(np.array(res))

corrs, mean_fc = [], []
for i, study in enumerate(studies):
    if study == "Asakura2020":
        continue
    table = get_dataset(study)
    mean_fc.append((table[table["cancer"] == 1].iloc[:, :-1].mean() - table[table["cancer"] == 0].iloc[:, :-1].mean()).mean())
    corrs.append(corr[studies.index("Asakura2020"), i])

corr_asakura, pval_asakura = pearsonr(mean_fc, corrs)
pval = pval * pval.shape[0] * pval.shape[1]
with open(get_project_path() / "Outdata" / "predictions_correlation.pickle", "wb") as f: 
    pickle.dump({"correlation": corr.tolist(), "pvalues": pval.tolist(), "correlation_asakura": corr_asakura, "pvalue_asakura": pval_asakura}, f)
