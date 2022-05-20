import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from Utils.config import get_project_path, studies
from Utils.datasets import get_datasets_intersections

np.random.seed(0)

out = []
for mod in range(2):
    res = []
    for i, s1 in enumerate(studies):
        for s2 in studies[i+1:]:
            data1, data2 = get_datasets_intersections([s1, s2])
            if len(data1.columns) <= 10:
                continue
            logreg = [XGBClassifier(use_label_encoder=False, eval_metric="logloss"), LogisticRegression(penalty="none", max_iter=1000)][mod]
            data1 = data1.iloc[:, :-1]
            data2 = data2.iloc[:, :-1]
            data1["dataset"] = 0
            data2["dataset"] = 1
            data = pd.concat([data1, data2])
            X_train, X_test, y_train, y_test = train_test_split(data.iloc[:, :-1], data["dataset"], test_size=0.33, random_state=0, stratify=data["dataset"])
            logreg.fit(X_train, y_train)
            auc = roc_auc_score(y_test, logreg.predict_proba(X_test)[:, 1])
            res.append(auc)
    out.append([np.mean(res), np.std(res, ddof=1)])

df = pd.DataFrame(np.array(out), index=["XGBoost", "Logistic Regression"], columns=["mean", "std"])
df.to_csv(get_project_path() / "Outdata" / "separate_datasets.csv", index_label="model")