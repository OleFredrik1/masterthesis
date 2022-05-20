import numpy as np
from sklearn.metrics import auc, roc_auc_score
import pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy.stats import ttest_ind

from Utils.datasets import get_dataset, get_datasets_intersections
from Utils.config import get_project_path, studies

threshold_studies = ["Chen2019", "Jin2017", "Nigita2018", "Yao2019"]
threshold_dataset = pd.concat(get_datasets_intersections([s + "_threshold_1000" for s in threshold_studies]))
no_threshold_dataset = pd.concat(get_datasets_intersections(threshold_studies))

for s in threshold_studies:
    studies.remove(s)

res = []
for s in studies:
    data = get_dataset(s)
    intersection_threshold = list(set(threshold_dataset.columns) & set(data.columns) - set(["cancer"]))
    intersection_no_threshold = list(set(threshold_dataset.columns) & set(data.columns) - set(["cancer"]))
    if len(intersection_threshold) < 5:
        continue
    logreg1 = LogisticRegression(penalty="none", max_iter=1000)
    logreg1.fit(no_threshold_dataset.loc[:, intersection_no_threshold], no_threshold_dataset["cancer"])
    auc1 = roc_auc_score(data["cancer"], logreg1.predict_proba(data.loc[:, intersection_no_threshold])[:,1])
    logreg2 = LogisticRegression(penalty="none", max_iter=1000)
    logreg2.fit(threshold_dataset.loc[:, intersection_threshold], threshold_dataset["cancer"])
    auc2 = roc_auc_score(data["cancer"], logreg2.predict_proba(data.loc[:, intersection_threshold])[:,1])
    res.append([s, auc1, auc2])

outres = np.array([[v[1], v[2]] for v in res])
ttest = ttest_ind(outres[:, 1], outres[:, 0])
pd.DataFrame([[ttest.statistic, ttest.pvalue]], columns=["statistic", "pvalue"]).to_csv(get_project_path() / "Outdata" / "rpm_threshold_aucs_pvalue.csv", index=False)

res.append(["mean", np.mean([v[1] for v in res]), np.mean([v[2] for v in res])])
pd.DataFrame(res, columns=["study", "auc no threshold", "auc threshold"]).to_csv(get_project_path() / "Outdata" / "rpm_threshold_aucs.csv", index=False)