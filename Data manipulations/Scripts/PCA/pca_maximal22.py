import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA
from scipy.stats import ttest_ind
from tqdm import tqdm

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

n_components = 10
max_datasets = get_datasets_intersections(maximal_studies)

res = []
for data in tqdm(max_datasets):
    pca = PCA(n_components=n_components)
    pca.fit(data.iloc[:, :-1])
    res2 = []
    for data2 in max_datasets:
        transformed = pca.transform(data2.iloc[:,:-1])
        transformed_cancer = transformed[data2["cancer"] == 1]
        transformed_control = transformed[data2["cancer"] == 0]
        res2.append([roc_auc_score(data2["cancer"], transformed[:, i]) for i in range(n_components)])
    res2 = np.array(res2)
    res.append(np.median(res2, axis=0))

res = np.array(res)
print(np.sort(res.flatten()))
df = pd.DataFrame(np.array(res), columns=[str(i) for i in range(1, n_components+1)], index=maximal_studies)
df.to_csv(get_project_path() / "Outdata" / "pca_maximal2.csv", index_label="Study")
