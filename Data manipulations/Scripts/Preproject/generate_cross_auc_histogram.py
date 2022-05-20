import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

aucs = []
for i, study_a in enumerate(studies):
    for j, study_b in enumerate(studies):
        if i == j:
            continue
        table_a, table_b = get_datasets_intersections([study_a, study_b], True)
        if len(table_a.columns) >= 10:
            logreg = LogisticRegression(max_iter=1000)
            logreg.fit(table_a.iloc[:, :-1], table_a["cancer"])
            preds = logreg.predict_proba(table_b.iloc[:, :-1])[:, 1]
            aucs.append(roc_auc_score(table_b["cancer"], preds))

df = pd.DataFrame(np.array(aucs).transpose(), columns=["auc"])
df.to_csv(get_project_path() / "Outdata" / "auc_histogram.csv")
