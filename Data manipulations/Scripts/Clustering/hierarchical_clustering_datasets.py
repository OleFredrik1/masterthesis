import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import scipy.spatial.distance as ssd
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use("pgf")

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

max_dist = 0
res = np.zeros((len(studies), len(studies)))
for i, s1 in enumerate(studies):
    for j, s2 in enumerate(studies[i+1:]):
        j += i+1
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns) == 1:
            res[i,j] = np.inf
            res[j,i] = np.inf
            continue
        healthy1 = data1[data1["cancer"] == 1].iloc[:, :-1]
        cancer1 = data1[data1["cancer"] == 0].iloc[:, :-1]
        healthy2 = data2[data2["cancer"] == 1].iloc[:, :-1]
        cancer2 = data2[data2["cancer"] == 0].iloc[:, :-1]
        fold_change1 = cancer1.mean() - healthy1.mean()
        fold_change2 = cancer2.mean() - healthy2.mean()
        squared_dist = np.power(fold_change1-fold_change2, 2)
        mean_dist = np.mean(squared_dist)
        max_dist = max(max_dist, mean_dist)
        res[i,j] = mean_dist
        res[j,i] = mean_dist

studies_label = []
for s in studies:
    ind = s.index("2")
    studies_label.append(s[:ind] + " (" + s[ind:] + ")")

res[np.isinf(res)] = max_dist
res = ssd.squareform(res)
clustering = linkage(res, method="ward", optimal_ordering=True)
plt.figure()
dendrogram(clustering, labels=studies_label, orientation="right")
plt.gca().get_xaxis().set_visible(False)
plt.savefig(get_project_path() / "Outdata" / "hierarchical_clustering_datasets.pdf", bbox_inches="tight")

