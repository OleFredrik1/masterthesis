from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import numpy as np
from tqdm import tqdm

from Utils.datasets import get_datasets_intersections
from Utils.config import studies

np.random.seed(0)
real_auc_scores = []
random1_auc_scores = []
random2_auc_scores = []

for i, study_a in tqdm(list(enumerate(studies)), desc="outer"):
    for j, study_b in tqdm(list(enumerate(studies[:i] + studies[i+1:])), desc="inner", leave=False):
        j = i+j+1
        table_a, table_b = get_datasets_intersections([study_a, study_b], standardized=True)
        assert np.all(table_a.columns == table_b.columns)
        if len(table_a.columns) >= 10:
            model = LogisticRegression(max_iter=1000)
            try:
                model.fit(table_a.iloc[:, :-1], table_a["cancer"])
                predictions = model.predict(table_b.iloc[:, :-1])
            except Exception as e:
                print(study_a, study_b)
                raise e
            real_auc_scores.append(roc_auc_score(table_b["cancer"], predictions))
            random_cancer = np.copy(table_b["cancer"].to_numpy())
            np.random.shuffle(random_cancer)
            random1_auc_scores.append(roc_auc_score(random_cancer,  predictions))
            random_cols = np.copy(table_a.columns[:-1].to_numpy())
            np.random.shuffle(random_cols)
            predictions = model.predict(table_b.loc[:, random_cols])
            random2_auc_scores.append(roc_auc_score(table_b["cancer"], predictions))

print(real_auc_scores)
print(random1_auc_scores)
print(random2_auc_scores)