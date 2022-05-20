import pandas as pd
import numpy as np
from scipy.stats import pearsonr, ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score

from Utils.config import staged_studies, get_project_path
from Utils.datasets import get_dataset_staged

aucs = []
for s1 in staged_studies:
    row = []
    data1 = get_dataset_staged(s1)
    data1_late = data1[data1["stage"].isin([0,3,4])]
    data1_early = data1[data1["stage"].isin([0,1,2])]
    logreg = LogisticRegression(penalty="none", max_iter=1000)
    m = min([5, data1_early["cancer"].sum(), (data1_early["cancer"] == 0).sum()])
    if m < 2:
        row.append(np.nan)
    else:
        scores = cross_val_score(logreg, data1_early.iloc[:, :-2], data1_early["cancer"], scoring="roc_auc", cv=m)
        row.append(np.mean(scores))
    logreg = LogisticRegression(penalty="none", max_iter=1000)
    m = min([5, data1_late["cancer"].sum(), (data1_late["cancer"] == 0).sum()])
    if m < 2:
        row.append(np.nan)
    else:
        scores = cross_val_score(logreg, data1_late.iloc[:, :-2], data1_late["cancer"], scoring="roc_auc", cv=m)
        row.append(np.mean(scores))
    aucs.append(row)
    

df = pd.DataFrame(np.array(aucs), columns=["Mean early", "Mean late"], index=staged_studies)
df.to_csv(get_project_path() / "Outdata" / "auc_stages_internal.csv", index_label="Study")