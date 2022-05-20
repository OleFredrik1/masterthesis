import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

from Utils.config import get_project_path
from Utils.datasets import get_datasets_intersections

studies = ["Asakura2020", "Fehlmann2020", "Patnaik2017", "Keller2014"]

for i, s1 in enumerate(studies):
    for s2 in studies[i+1:]:
        data1, data2 = get_datasets_intersections([s1, s2])
        data1 = data1.iloc[:, :-1]
        data2 = data2.iloc[:, :-1]
        joined = pd.concat([data1, data2])
        pca = PCA(n_components=2)
        pca.fit(joined)
        df = pd.DataFrame(pca.transform(joined), columns=["PCA1", "PCA2"])
        df["Type"] = len(data1)*["A"] + len(data2)*["B"]
        df.to_csv(get_project_path() / "Outdata" / "PCA" / "RemoveTwo" / "Before" / f"{s1}_vs_{s2}.csv")
        pca1 = PCA(n_components=2)
        pca1.fit(data1)
        components = pca1.components_    
        to_subtract = data1 @ components.transpose() @ components
        to_subtract.columns = data1.columns
        data1 -= to_subtract
        pca2 = PCA(n_components=2)
        pca2.fit(data2)
        components = pca2.components_    
        to_subtract = data2 @ components.transpose() @ components
        to_subtract.columns = data2.columns
        data2 -= to_subtract
        joined = pd.concat([data1, data2])
        pca = PCA(n_components=2)
        pca.fit(joined)
        df = pd.DataFrame(pca.transform(joined), columns=["PCA1", "PCA2"])
        df["Type"] = len(data1)*["A"] + len(data2)*["B"]
        df.to_csv(get_project_path() / "Outdata" / "PCA" / "RemoveTwo" / "After" / f"{s1}_vs_{s2}.csv")