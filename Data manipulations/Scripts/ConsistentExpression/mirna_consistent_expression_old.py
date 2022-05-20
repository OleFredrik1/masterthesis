from numpy import sign
import pandas as pd
from scipy.stats import ttest_ind, binomtest
from collections import defaultdict

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

res = defaultdict(list)

for study in studies:
    data = get_dataset(study)
    cancers = data[data["cancer"] == 1].iloc[:, :-1]
    healthy = data[data["cancer"] == 0].iloc[:, :-1]
    t_values = ttest_ind(cancers, healthy).statistic
    for seq, t_value in zip(data.columns[:-1], t_values):
        res[seq].append(t_value)

expressions = []
for l in res.values():
    for i, v1 in enumerate(l):
        for v2 in l[i+1:]:
            expressions.append(sign(v1) == sign(v2))

print(f"probability: {sum(expressions)/len(expressions)}")
print(f"p-value: {binomtest(sum(expressions), len(expressions), alternative='greater')}")
