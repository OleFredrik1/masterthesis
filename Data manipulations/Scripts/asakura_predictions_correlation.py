from sklearn.linear_model import LogisticRegression
import numpy as np
from scipy.stats import pearsonr
from scipy.special import betainc
import pandas as pd
import pickle

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

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


studies.remove("Asakura2020")

res = []
out_studies = []
for study in studies:
    data1, data2 = get_datasets_intersections(["Asakura2020", study])
    if len(data1.columns[:-1]) < 4:
        continue
    out_studies.append(study)
    logreg = LogisticRegression(penalty="none", max_iter=1000)
    logreg.fit(data2.iloc[:, :-1], data2["cancer"])
    res.append(logreg.predict_proba(data1.iloc[:, :-1])[:, 1])

res.append(data1["cancer"])
corr, pval = corrcoef(np.array(res))
pval = pval * pval.shape[0] * pval.shape[1]
with open(get_project_path() / "Outdata" / "asakura_predictions_correlation.pickle", "wb") as f: 
    pickle.dump({"studies": out_studies, "correlation": corr.tolist(), "pvalues": pval.tolist()}, f)
