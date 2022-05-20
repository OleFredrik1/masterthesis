from collections import defaultdict
import json
import sys
from pathlib import Path
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import numpy as np

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

models = [(lambda: LogisticRegression(penalty="none", max_iter=1000), "logreg"), (lambda: SVC(probability=True), "SVM"), (lambda: RandomForestClassifier(), "random forest"), (lambda: XGBClassifier(use_label_encoder=False, eval_metric="logloss"), "xgb")]

meta = defaultdict(list)
res = defaultdict(lambda: defaultdict(dict))
res["meta"] = meta

for s1 in studies:
    for s2 in studies:
        if s1 == s2:
            continue
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns[:-1]) < 4:
            continue
        meta[s1].append(s2)
        out = res[f"{s1}_vs_{s2}"]
        for m, l in models:
            m1 = m()
            scores = cross_val_score(m1, data1.iloc[:, :-1], data1["cancer"], scoring="roc_auc", cv=min([5, data1["cancer"].sum(), (data1["cancer"] == 0).sum()]))
            out[l][s1] = np.mean(scores)
            m2 = m()
            scores = cross_val_score(m2, data2.iloc[:, :-1], data2["cancer"], scoring="roc_auc", cv=min([5, data2["cancer"].sum(), (data2["cancer"] == 0).sum()]))
            out[l][s2] = np.mean(scores)
            m3 = m()
            m3.fit(data1.iloc[:, :-1], data1["cancer"])
            out[l][f"{s1} to {s2}"] = roc_auc_score(data2["cancer"], m3.predict_proba(data2.iloc[:, :-1])[:,1])
            m4 = m()
            m4.fit(data2.iloc[:, :-1], data2["cancer"])
            out[l][f"{s2} to {s1}"] = roc_auc_score(data1["cancer"], m4.predict_proba(data1.iloc[:, :-1])[:,1])

with open(Path(sys.path[0]) / "Outdata" / "PairwiseMachineLearning" / "data.json", "w") as f:
    f.write(json.dumps(res))