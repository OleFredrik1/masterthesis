import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

datasets = { s:get_dataset(s) for s in studies }

def check_subset(possible_subset, possible_mirnas):
    if len(possible_subset) <= 1:
        return False
    for study in studies:
        if study in possible_subset:
            continue
        if len(possible_mirnas & set(datasets[study].columns)) >= 10:
            return False
    return True

    

def generate_maximal_subsets(current_subset, current_mirnas, index, return_list):
    if check_subset(current_subset, current_mirnas):
        return_list.append(current_subset)
    for i, study in enumerate(studies[index:]):
        if len(current_mirnas & set(datasets[study].columns)) >= 10:
            generate_maximal_subsets(current_subset | set([study]), current_mirnas & set(datasets[study].columns), index + i + 1, return_list)

all_mirnas = set.union(*[set(datasets[s].columns) for s in studies]) - set(["cancer"])
ret = []
generate_maximal_subsets(set(), all_mirnas, 0, ret)
print(len(ret))

aucs = []

for subset in ret:
    cur_datasets = [datasets[s] for s in subset]
    mirna_intersection = list(set.intersection(*[set(data.columns) for data in cur_datasets]) - set(["cancer"])) + ["cancer"]
    cur_datasets = [data.loc[:, mirna_intersection] for data in cur_datasets]
    for i in range(len(subset)):
        training_sets = cur_datasets[:i] + cur_datasets[i+1:]
        test_set = cur_datasets[i]
        joined = pd.concat(training_sets)
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(joined.iloc[:, :-1], joined["cancer"])
        aucs.append(roc_auc_score(test_set["cancer"], logreg.predict_proba(test_set.iloc[:, :-1])[:, 1]))

df = pd.DataFrame(np.array(aucs).transpose(), columns=["AUC"])
df.to_csv(get_project_path() / "Outdata" / "auc_maximal.csv")
