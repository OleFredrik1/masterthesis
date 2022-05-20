from turtle import pen
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from Utils.config import get_project_path
from Utils.datasets import get_dataset
from converters import canonical_to_seq

mirnas = ["hsa-miR-21", "hsa-miR-210", "hsa-miR-182", "hsa-miR-155", "hsa-miR-17"]
mirna_seq = canonical_to_seq(mirnas)

studies = ["Asakura2020", "Fehlmann2020", "Leidinger2014", "Patnaik2017", "Yao2019"]
datasets = [get_dataset(s).loc[:, mirna_seq + ["cancer"]] for s in studies]


aucs = []
for i in range(len(studies)):
    training_sets = datasets[:i] + datasets[i+1:]
    testset = datasets[i]
    logreg = LogisticRegression(penalty="none", max_iter=1000)
    joint = pd.concat(training_sets)
    logreg.fit(joint.iloc[:, :-1], joint["cancer"], sample_weight=sum([len(ts)*[1/len(ts)] for ts in training_sets],[]))
    aucs.append(roc_auc_score(testset["cancer"], logreg.predict_proba(testset.iloc[:, :-1])[:, 1]))

df = pd.DataFrame(np.array(aucs).transpose(), index=studies, columns=["AUC"])
df.to_csv(get_project_path() / "Outdata" / "common_cross_validation.csv", index_label="Testset")