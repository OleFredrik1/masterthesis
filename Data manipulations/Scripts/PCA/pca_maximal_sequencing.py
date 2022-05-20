import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA
from scipy.stats import ttest_ind

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset, get_datasets_intersections

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv")

maximal_studies = list(metadata.loc[metadata["Technology"] == "Sequencing", "Study"])
maximal_studies.sort()

max_datasets = get_datasets_intersections(maximal_studies)
combined = pd.concat(max_datasets)

n_components = 10

pca = PCA(n_components=14)
pca.fit(combined.iloc[:, :-1])

print(len(max_datasets[0].columns))

res = []
for data in max_datasets:
    pca = PCA(n_components=n_components)
    pca.fit(data.iloc[:, :-1])
    res2 = []
    for data2 in max_datasets:
        transformed = pca.transform(data2.iloc[:,:-1])
        transformed_cancer = transformed[data2["cancer"] == 1]
        transformed_control = transformed[data2["cancer"] == 0]
        #res2.append(list(ttest_ind(transformed_cancer, transformed_control).pvalue))
        res2.append([roc_auc_score(data2["cancer"], transformed[:, i]) for i in range(n_components)])
    res2 = np.array(res2)
    res.append(np.median(res2, axis=0))

res = np.array(res)
print(np.sort(res.flatten()) * (len(max_datasets)**2))
df = pd.DataFrame(np.array(res), columns=[str(i) for i in range(1, n_components+1)], index=maximal_studies)
df.to_csv(get_project_path() / "Outdata" / "pca_maximal_sequencing.csv", index_label="Study")
