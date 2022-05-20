import numpy as np
from sklearn.metrics import roc_auc_score
import pandas as pd
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression

from Utils.datasets import get_dataset
from Utils.config import get_project_path

studies = ["Chen2019", "Jin2017", "Nigita2018", "Yao2019"]
thresholds = [0, 1, 10, 100, 1000]

res = []
for i in thresholds:
    datasets = [get_dataset(f"{s}_threshold_{i}") for s in studies]
    intersection = list(set.intersection(*[set(d.columns) for d in datasets]) - set(["cancer"])) + ["cancer"]
    union = list(set.union(*[set(d.columns) for d in datasets]) - set(["cancer"])) + ["cancer"]
    datasets_union= []
    for data in datasets:
        new_data = pd.DataFrame()
        for c in union:
            if c in data.columns:
                new_data[c] = data[c]
            else:
                new_data[c] = np.nan
        datasets_union.append(new_data)
    datasets_inter = [d.loc[:, intersection] for d in datasets]
    auc_union = []
    auc_inter = []
    for i, test_inter in enumerate(datasets_inter):
        test_union = datasets_union[i]
        train_inter = pd.concat(datasets_inter[:i] + datasets_inter[i+1:])
        train_union = pd.concat(datasets_union[:i] + datasets_union[i+1:])
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(train_inter.iloc[:, :-1], train_inter["cancer"])
        auc_inter.append(roc_auc_score(test_inter["cancer"], logreg.predict_proba(test_inter.iloc[:, :-1])[:, 1]))
        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        xgb.fit(train_union.iloc[:, :-1], train_union["cancer"])
        auc_union.append(roc_auc_score(test_union["cancer"], xgb.predict_proba(test_union.iloc[:, :-1])[:, 1]))
    res.append([np.mean(auc_inter), len(intersection[:-1]), np.mean(auc_union), len(union[:-1])])

pd.DataFrame(res, columns=["intersection", "mirna-intersection", "union", "mirna-union"], index=thresholds).to_csv(get_project_path() / "Outdata" / "rpm_threshold_cv.csv", index_label="threshold")
    