import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA
from scipy.stats import ttest_ind

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset, get_datasets_intersections

datasets = { s:get_dataset(s) for s in studies }
for s, data in datasets.items():
    data.name = s

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
#generate_maximal_subsets(set(), all_mirnas, 0, ret)
#ret_len = [len(r) for r in ret]
#print(ret[np.argmax(ret_len)])
#maximal_studies = list(ret[np.argmax(ret_len)])
maximal_studies = ['Leidinger2016', 'Jin2017', 'Patnaik2012', 'Chen2019', 'Keller2009', 'Fehlmann2020', 'Halvorsen2016', 'Keller2014', 'Yao2019', 'Nigita2018', 
'Reis2020', 'Leidinger2011', 'Patnaik2017', 'Leidinger2014', 'Asakura2020', 'Wozniak2015', 'Boeri2011']
maximal_studies.sort()

max_datasets = get_datasets_intersections(maximal_studies)
combined = pd.concat(max_datasets)

pca = PCA(n_components=14)
pca.fit(combined.iloc[:, :-1])

res = []
for data in max_datasets:
    transformed = pca.transform(data.iloc[:,:-1])
    transformed_cancer = transformed[data["cancer"] == 1]
    transformed_control = transformed[data["cancer"] == 0]
    #res.append(list(ttest_ind(transformed_cancer, transformed_control).statistic))
    res.append([roc_auc_score(data["cancer"], transformed[:, i]) for i in range(14)])

res = np.array(res)
res = np.maximum(res, 1-res)
res = np.concatenate((res, np.median(res, axis=0).reshape(1,14)))
df = pd.DataFrame(np.array(res), columns=[str(i) for i in range(1, 15)], index=maximal_studies + ["median"])
df.to_csv(get_project_path() / "Outdata" / "pca_maximal.csv", index_label="Study")
