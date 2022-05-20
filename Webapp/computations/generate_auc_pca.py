from collections import defaultdict
import json
import sys
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import numpy as np

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections, get_dataset

models = [(lambda: LogisticRegression(penalty="none", max_iter=1000), "logreg"), (lambda: SVC(probability=True), "SVM"), (lambda: RandomForestClassifier(), "random forest"), (lambda: XGBClassifier(use_label_encoder=False, eval_metric="logloss"), "xgb")]

aucs = {l: [[0.5 for _ in studies] for _ in studies] for _, l in models}

for i1, s1 in enumerate(studies):
    for i2, s2 in enumerate(studies):
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns[:-1]) < 4:
            continue
        if s1 == s2:
            for m, l in models:
                m3 = m()
                scores = cross_val_score(m3, data1.iloc[:, :-1], data1["cancer"], scoring="roc_auc", cv=min([5, data1["cancer"].sum(), (data1["cancer"] == 0).sum()]))
                aucs[l][i1][i2] = np.mean(scores)
            continue
        for m, l in models:
            m3 = m()
            m3.fit(data1.iloc[:, :-1], data1["cancer"])
            aucs[l][i1][i2] = roc_auc_score(data2["cancer"], m3.predict_proba(data2.iloc[:, :-1])[:, 1])

n_components = 10

new_res = {}
for _, l in models:
    pca_arr = np.array(aucs[l])
    pca = PCA(n_components=n_components)
    pca.fit(pca_arr)

    new_res[l] = {
        "loadings": pca.components_.T.tolist(),
        "variance explained": pca.explained_variance_ratio_.tolist()
    }

    transformed = pca.transform(np.array(aucs[l]))
    new_res[l]["data"] = transformed.tolist()

with open(Path(sys.path[0]) / "Outdata" / "AUC_PCA" / "data.json", "w") as f:
    f.write(json.dumps(new_res))