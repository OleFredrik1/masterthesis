from collections import defaultdict
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from scipy.stats import ttest_ind
import numpy as np

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections, get_dataset

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

aucs = [[0.5 for _ in studies] for _ in studies]

for i1, s1 in enumerate(studies):
    for i2, s2 in enumerate(studies):
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns[:-1]) < 4:
            continue
        if s1 == s2:
            m3 = LogisticRegression(penalty="none", max_iter=1000)
            scores = cross_val_score(m3, data1.iloc[:, :-1], data1["cancer"], scoring="roc_auc", cv=min([5, data1["cancer"].sum(), (data1["cancer"] == 0).sum()]))
            aucs[i1][i2] = np.mean(scores)
            continue
        m3 = LogisticRegression(penalty="none", max_iter=1000)
        m3.fit(data1.iloc[:, :-1], data1["cancer"])
        aucs[i1][i2] = roc_auc_score(data2["cancer"], m3.predict_proba(data2.iloc[:, :-1])[:, 1])

pca_arr = np.array(aucs)
pca = PCA(n_components=1)
pca.fit(pca_arr)
transformed = pca.transform(pca_arr)[:, 0]
technologies = ["qRT-PCR", "Microarray", "Sequencing"]

out = {}
for i1, t1 in enumerate(technologies):
    for t2 in technologies[i1+1:]:
        a1 = transformed[list(map(studies.index, metadata[metadata["Technology"] == t1].index))]
        a2 = transformed[list(map(studies.index, metadata[metadata["Technology"] == t2].index))]
        ttest = ttest_ind(a1, a2)
        out[f"{t1}_vs_{t2}"] = [np.mean(a1), np.std(a1, ddof=1), np.mean(a2), np.std(a2, ddof=1), ttest.statistic, ttest.pvalue]

pd.DataFrame.from_dict(out, columns=["mean1", "std1", "mean2", "std2", "t-value", "p-value"], orient="index").to_csv(get_project_path() / "Outdata" / "auc_pca_t_test.csv", index_label="comparison")