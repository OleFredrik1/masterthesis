from sklearn.decomposition import PCA
import pandas as pd
import sys
from pathlib import Path
import json

from Utils.config import studies
from Utils.datasets import get_dataset

num_pc = {}

for study in studies:
    data = get_dataset(study)
    d = min([10, len(data), len(data.columns[:-1])])
    num_pc[study] = d
    pca = PCA(n_components=d)
    transformed = pca.fit_transform(data.iloc[:, :-1])
    df = {i:list(transformed[:, i]) for i in range(d)}
    df["cancer"] = list(data["cancer"])
    df["variance explained"] = pca.explained_variance_ratio_.tolist()
    with open(Path(sys.path[0])  / "Outdata" / "PCASingle" / (study + ".json"), "w") as f:
        f.write(json.dumps(df))

out = {"numberOfComponents": num_pc}
with open(Path(sys.path[0])  / "Outdata" / "PCASingle" / "meta.json", "w") as f:
    f.write(json.dumps(out))
