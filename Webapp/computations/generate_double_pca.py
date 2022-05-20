import json
from sklearn.decomposition import PCA
from collections import defaultdict
import pandas as pd
import sys
from pathlib import Path

from Utils.config import studies
from Utils.datasets import get_datasets_intersections

meta = defaultdict(dict)
for s1 in studies:
    for s2 in studies:
        if s1 == s2:
            continue
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns) < 4:
            meta[s1][s2] = {s1: -1, s2: -1, "joint": -1}
            continue
        res = {}
        d1 = min([10, len(data1), len(data1.columns[:-1])])
        pca1 = PCA(n_components=d1)
        transformed1 = pca1.fit_transform(data1.iloc[:, :-1])
        transformed2 = pca1.transform(data2.iloc[:, :-1])
        df1 = {i: list(transformed1[:, i]) for i in range(d1)}
        df1["cancer"] = list(data1["cancer"])
        df2 = {i: list(transformed2[:, i]) for i in range(d1)}
        df2["cancer"] = list(data2["cancer"])
        res[s1] = {s1: df1, s2: df2, "variance explained": pca1.explained_variance_ratio_.tolist()}
        d2 = min([10, len(data2), len(data2.columns[:-1])])
        pca2 = PCA(n_components=d2)
        transformed2 = pca2.fit_transform(data2.iloc[:, :-1])
        transformed1 = pca2.transform(data1.iloc[:, :-1])
        df1 = {i: list(transformed1[:, i]) for i in range(d2)}
        df1["cancer"] = list(data1["cancer"])
        df2 = {i: list(transformed2[:, i]) for i in range(d2)}
        df2["cancer"] = list(data2["cancer"])
        res[s2] = {s1: df1, s2: df2, "variance explained": pca2.explained_variance_ratio_.tolist()}
        data = pd.concat([data1, data2])
        d3 = min([10, len(data), len(data.columns[:-1])])
        pca3 = PCA(n_components=d3)
        pca3.fit(data.iloc[:, :-1])
        transformed1 = pca3.transform(data1.iloc[:, :-1])
        transformed2 = pca3.transform(data2.iloc[:, :-1])
        df1 = {i: list(transformed1[:, i]) for i in range(d3)}
        df1["cancer"] = list(data1["cancer"])
        df2 = {i: list(transformed2[:, i]) for i in range(d3)}
        df2["cancer"] = list(data2["cancer"])
        res["joint"] = {s1: df1, s2: df2, "variance explained": pca3.explained_variance_ratio_.tolist()}
        meta[s1][s2] = {s1: d1, s2: d2, "joint": d3}
        with open(Path(sys.path[0]) / "Outdata" / "PCADouble" / f"{s1}_vs_{s2}.json", "w") as f:
            f.write(json.dumps(res))

with open(Path(sys.path[0]) / "Outdata" / "PCADouble" / "meta.json", "w") as f:
    f.write(json.dumps(meta))

