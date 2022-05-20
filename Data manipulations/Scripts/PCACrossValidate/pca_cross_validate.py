from operator import index
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier

from Utils.config import studies
from Utils.datasets import get_dataset, get_project_path

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)
datasets = {s: get_dataset(s) for s in studies}
pca_removed_datasets = {}

seq_datasets = list(metadata[metadata["Technology"] == "Sequencing"].index)
studies = list(metadata[metadata["Technology"] != "Sequencing"].index)
common_mirnas = list(set.intersection(*[set(datasets[s].columns) for s in seq_datasets]) - set(["cancer"])) + ["cancer"]
seq_datasets = [datasets[s].loc[:, common_mirnas] for s in seq_datasets]

def calculate():
    res = []
    for s in studies:
        data = datasets[s]
        common_mirnas = list(set(seq_datasets[0].columns) & set(data.columns) - set(["cancer"])) + ["cancer"]
        data = data.loc[:, common_mirnas]
        cur_seq_datasets = [ds.loc[:, common_mirnas] for ds in seq_datasets]
        seq_joined = pd.concat(cur_seq_datasets)
        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        data_internal_auc = np.mean(cross_val_score(xgb, data.iloc[:, :-1], data["cancer"], cv=min([5, (data["cancer"] == 1).sum(), (data["cancer"] == 0).sum()]), scoring="roc_auc"))
        seq_internal_aucs = []
        for i, testing_set in enumerate(cur_seq_datasets):
            training_set = pd.concat(cur_seq_datasets[:i] + cur_seq_datasets[i+1:])
            xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
            xgb.fit(training_set.iloc[:, :-1], training_set["cancer"])
            seq_internal_aucs.append(roc_auc_score(testing_set["cancer"], xgb.predict_proba(testing_set.iloc[:, :-1])[:, 1]))
        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        xgb.fit(seq_joined.iloc[:, :-1], seq_joined["cancer"])
        to_data_auc = roc_auc_score(data["cancer"], xgb.predict_proba(data.iloc[:, :-1])[:, 1])
        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        xgb.fit(data.iloc[:, :-1], data["cancer"])
        from_data_auc = roc_auc_score(seq_joined["cancer"], xgb.predict_proba(seq_joined.iloc[:, :-1])[:, 1])
        res.append([data_internal_auc, np.mean(seq_internal_aucs), to_data_auc, from_data_auc])
    res = np.array(res)
    res = np.concatenate([res, np.mean(res, axis=0).reshape((1, 4))])    
    return res

df = pd.DataFrame(calculate(), index=studies + ["Mean"], columns=["data internal", "seq internal", "from seq", "to seq"])
df.to_csv(get_project_path() / "Outdata" / "pca_cross_validate_no_pca.csv")


for s, data in datasets.items():
    pca = PCA(n_components=2)
    pca.fit(data.iloc[:, :-1])
    components = pca.components_
    data2 = data.copy()
    to_subtract = data2.iloc[:, :-1] @ components.transpose() @ components
    to_subtract.columns = data2.columns[:-1]
    data2.iloc[:, :-1] = data2.iloc[:, :-1] - to_subtract
    datasets[s] = data2

seq_datasets = list(metadata[metadata["Technology"] == "Sequencing"].index)
studies = list(metadata[metadata["Technology"] != "Sequencing"].index)
common_mirnas = list(set.intersection(*[set(datasets[s].columns) for s in seq_datasets]) - set(["cancer"])) + ["cancer"]
seq_datasets = [datasets[s].loc[:, common_mirnas] for s in seq_datasets]

df = pd.DataFrame(calculate(), index=studies + ["Mean"], columns=["data internal", "seq internal", "from seq", "to seq"])
df.to_csv(get_project_path() / "Outdata" / "pca_cross_validate_pca.csv")


