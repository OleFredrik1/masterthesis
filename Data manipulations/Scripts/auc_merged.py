import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

datasets = [get_dataset(s) for s in studies]
minra_list = list(set.union(*[set(data.columns) for data in datasets]) - set(["cancer"])) + ["cancer"]
new_datasets = []
for data in datasets:
    new_data = pd.DataFrame()
    for mirna in minra_list:
        if mirna in data.columns:
            new_data[mirna] = data[mirna]
        else:
            new_data[mirna] = np.nan
    new_datasets.append(new_data)
datasets = new_datasets
aucs = []

for i in range(len(datasets)):
    training_data = datasets[:i] + datasets[i+1:]
    test_data = datasets[i]
    joined = pd.concat(training_data)
    xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    xgb.fit(joined.iloc[:, :-1], joined["cancer"])
    aucs.append(roc_auc_score(test_data["cancer"], xgb.predict_proba(test_data.iloc[:, :-1])[:, 1]))

df = pd.DataFrame(np.array(aucs).transpose(), columns=["AUC"], index=studies)
df.to_csv(get_project_path() / "Outdata" / "merged_auc.csv", index_label="Study")
