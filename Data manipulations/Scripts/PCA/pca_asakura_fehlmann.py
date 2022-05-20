import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from sklearn.decomposition import PCA

from Utils.config import get_project_path
from Utils.datasets import get_datasets_intersections

data1, data2 = get_datasets_intersections(["Asakura2020", "Fehlmann2020"])
for n in range(2):
    if n == 1:
        data1, data2 = data2, data1
    cancer1 = data1.loc[data1["cancer"] == 1].iloc[:, :-1]
    healthy1 = data1.loc[data1["cancer"] == 0].iloc[:, :-1]
    cancer2 = data2.loc[data2["cancer"] == 1].iloc[:, :-1]
    healthy2 = data2.loc[data2["cancer"] == 0].iloc[:, :-1]

    pca1 = PCA(n_components=10)
    pca1.fit(data1.iloc[:, :-1])
    cancer1_proj = pca1.transform(cancer1)
    healthy1_proj = pca1.transform(healthy1)
    cancer2_proj = pca1.transform(cancer2)
    healthy2_proj = pca1.transform(healthy2)
    res = []
    for i in range(10):
        ttest1 = ttest_ind(cancer1_proj[:, i], healthy1_proj[:, i])
        ttest2 = ttest_ind(cancer2_proj[:, i], healthy2_proj[:, i])
        res.append([i+1, pca1.explained_variance_ratio_[i], ttest1.statistic, ttest1.pvalue, ttest2.statistic, ttest2.pvalue])
    df = pd.DataFrame(np.array(res), columns=["Component #", "Explained variance proportion", "t-value1", "p-value1", "t-value2", "p-value2"])
    df.to_csv(get_project_path() / "Outdata" / f"pca_asakura_fehlmann_{'asakura' if n == 0 else 'fehlmann'}.csv", index=False)
