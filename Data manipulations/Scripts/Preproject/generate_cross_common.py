from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import numpy as np
from tqdm import tqdm
import pandas as pd

from Utils.datasets import get_datasets_intersections
from Utils.config import studies


commons = ["Asakura2020", "Fehlman2020", "Patnaik2017", "Leidinger2015"]
tables = get_datasets_intersections(commons)

np.random.seed(0)
real_auc_scores = []

for i, study_a in enumerate(commons):
    model = LogisticRegression(max_iter=1000)
    training_table = pd.concat(tables[:i] + tables[i+1:])
    test_table = tables[i]
    model.fit(training_table.iloc[:, :-1], training_table["cancer"])
    real_auc_scores.append(roc_auc_score(test_table["cancer"], model.predict(test_table.iloc[:, :-1])))

print(real_auc_scores)
