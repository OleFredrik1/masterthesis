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



res = {
    d: {
        s: {
            "controls": [len(studies)*[0.5] for i in range((d["cancer"] == 0).sum())],
            "cases": [len(studies)*[0.5] for i in range((d["cancer"] == 1).sum())]
        } for s, d in zip(studies, get_datasets_intersections(studies))
    } for _, d in models
}

meta = defaultdict(list)

for s1 in studies:
    for i, s2 in enumerate(studies):
        if s1 == s2:
            continue
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns[:-1]) < 4:
            continue
        meta[s1].append(s2)
        for m, l in models:
            m3 = m()
            m3.fit(data2.iloc[:, :-1], data2["cancer"])
            preds1 = m3.predict_proba(data1.loc[data1["cancer"] == 0, :].iloc[:, :-1])[:,1]
            for j, p in enumerate(preds1):
                res[l][s1]["controls"][j][i] = p
            preds2 = m3.predict_proba(data1.loc[data1["cancer"] == 1, :].iloc[:, :-1])[:,1]
            for j, p in enumerate(preds2):
                res[l][s1]["cases"][j][i] = p

out_meta = {}
for _, l in models:
    for s in studies:
        pca_arr = np.array([r for t in ["cases", "controls"] for r in res[l][s][t]])
        n_components = min([10, len(pca_arr), len(pca_arr[0])])
        out_meta[s] = n_components
        pca = PCA(n_components=n_components)
        pca.fit(pca_arr)

        new_res = {
            "data": {
                t: {
                    "controls": [],
                    "cases": []
                } for t in range(n_components)
            },
            "loadings": pca.components_.T.tolist(),
            "variance explained": pca.explained_variance_ratio_.tolist(),
            "studies": meta[s]
        }

        for c in ["cases", "controls"]:
            transformed = pca.transform(np.array(res[l][s][c]))
            for i in range(n_components):
                new_res["data"][i][c] = list(map(float,transformed[:, i]))

        with open(Path(sys.path[0]) / "Outdata" / "SamplePvaluePCA" / "Single" / f"{s}_{l}.json", "w") as f:
            f.write(json.dumps(new_res))


with open(Path(sys.path[0]) / "Outdata" / "SamplePvaluePCA" / "Single" / "meta.json", "w") as f:
    f.write(json.dumps(out_meta))