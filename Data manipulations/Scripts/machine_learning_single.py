import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

models = [lambda: LogisticRegression(penalty="none", max_iter=1000), lambda: SVC(), lambda: RandomForestClassifier(), lambda: XGBClassifier(use_label_encoder=False, eval_metric="logloss")]
res = []

for study in studies:
    data = get_dataset(study)
    row = [study]
    for m in models:
        model = m()
        scores = cross_val_score(model, data.iloc[:, :-1], data["cancer"], scoring="roc_auc", cv=min([5, data["cancer"].sum(), (data["cancer"] == 0).sum()]))
        row.append(np.mean(scores))
    res.append(row)

df = pd.DataFrame(np.array(res), columns=["Study", "Logistic Regression", "SVM", "Random Forest", "XGBoost"])
df.to_csv(get_project_path() / "Outdata" / "machine_learning_single.csv", index=False)