import pandas as pd
from scipy.stats.stats import ttest_ind
from collections import defaultdict

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

res = defaultdict(list)

for study in studies:
    data = get_dataset(study)
    cancers = data[data["cancer"] == 1].iloc[:, :-1]
    healthy = data[data["cancer"] == 0].iloc[:, :-1]
    pvalues = ttest_ind(cancers, healthy).statistic
    for seq, p in zip(data.columns[:-1], pvalues):
        res[seq].append((study, p))

print(res)

