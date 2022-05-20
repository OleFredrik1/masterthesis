import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from sklearn.decomposition import PCA

from Utils.config import get_project_path, studies
from Utils.datasets import get_datasets_intersections, get_dataset

data1, data2 = get_datasets_intersections(["Asakura2020", "Fehlmann2020"])
pca1 = PCA(n_components=10)
pca1.fit(data1.iloc[:, :-1])

#studies.remove("Asakura2020")
#studies.remove("Fehlmann2020")
res = []
for study in studies:
    raw_data = get_dataset(study)
    intersec = set(raw_data.columns) & set(data1.columns) - set(["cancer"])
    if len(intersec)/len(data1.columns[:-1]) < 0.5:
        continue
    data = pd.DataFrame(index=raw_data.index)
    for mirna in data1.columns:
        if mirna in raw_data.columns:
            data[mirna] = raw_data[mirna]
        else:
            data[mirna] = 0
    if data.isna().sum().sum() > 0:
        raise Exception(f"{study} has some nan")
    cancer = data.loc[data["cancer"] == 1].iloc[:, :-1]
    healthy = data.loc[data["cancer"] == 0].iloc[:, :-1]
    cancer_proj = pca1.transform(cancer)
    healthy_proj = pca1.transform(healthy)
    ttest = ttest_ind(cancer_proj[:, 2], healthy_proj[:, 2])
    res.append([study, ttest.statistic, ttest.pvalue, len(intersec)/len(data1.columns[:-1])])

df = pd.DataFrame(np.array(res), columns=["Study", "t-value", "p-value", "proportion of miRNA"])
df.to_csv(get_project_path() / "Outdata" / "pca_asakura_external.csv", index=False)