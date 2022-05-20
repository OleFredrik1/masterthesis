from numpy import sign
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, binomtest
from collections import defaultdict

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

res = defaultdict(list)

for study in studies:
    data = get_dataset(study)
    cancers = data[data["cancer"] == 1].iloc[:, :-1]
    healthy = data[data["cancer"] == 0].iloc[:, :-1]
    t_values = ttest_ind(cancers, healthy)
    for seq, t_value, p_value in zip(data.columns[:-1], t_values.statistic, t_values.pvalue):
        res[seq].append((t_value, p_value))

vals = [(0.05* (10**(-i)), []) for i in range(10)]
for l in res.values():
    for i, v1 in enumerate(l):
        for v2 in l[i+1:]:
            for p_val, li in vals:
                if v1[1] < p_val and v2[1] < p_val:
                    li.append(sign(v1[0]) == sign(v2[0]))

res = [binomtest(sum(l), len(l), alternative="greater") for _, l in vals]
df = pd.DataFrame(np.array([[t.proportion_estimate, t.pvalue] for t in res]), index=[str(v) for v, _ in vals], columns=["probability", "pvalue"])
df.to_csv(get_project_path() / "Outdata" / "mirna_consistent_expression_pvalues.csv", index_label="Pairs")
