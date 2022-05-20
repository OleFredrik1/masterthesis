from collections import defaultdict
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon, ttest_ind
from itertools import combinations
from tqdm import tqdm

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

res = defaultdict(list)
study_mirnas = {}
diff_ex = {}

for study in studies:
    data = get_dataset(study)
    study_mirnas[study] = set(data.columns[:-1])
    cancers = data.loc[data["cancer"] == 1].iloc[:, :-1]
    healthy = data.loc[data["cancer"] == 0].iloc[:, :-1]
    for seq in data.columns[:-1]:
        res[seq].append((study, cancers[seq].mean() - healthy[seq].mean()))
        diff_ex[(study, seq)] = np.sign(cancers[seq].mean() - healthy[seq].mean())

most_consistent = []
least_consistent = []

for s1, s2 in tqdm(list(combinations(studies, 2))):
    mirnas1, mirnas2 = study_mirnas[s1], study_mirnas[s2]
    mirnas = mirnas1 & mirnas2
    if len(mirnas) < 20:
        continue
    mirna_ps = []
    for seq in mirnas:
        vals = [v[1] for v in res[seq] if v[0] not in [s1, s2]]
        if len(vals) >= 10:
            mirna_ps.append((wilcoxon(vals).pvalue, seq))
    if len(mirna_ps) < 20:
        continue
    mirna_ps.sort()
    most_consistent.extend(diff_ex[(s1, seq)] == diff_ex[(s2, seq)] for _, seq in mirna_ps[:10])
    least_consistent.extend(diff_ex[(s1, seq)] == diff_ex[(s2, seq)] for _, seq in mirna_ps[-10:])
print(len(most_consistent))
ttest = ttest_ind(most_consistent, least_consistent)
df = pd.DataFrame(np.array([[np.mean(most_consistent), np.std(most_consistent, ddof=1), np.mean(least_consistent), np.std(least_consistent, ddof=1), ttest.statistic, ttest.pvalue]]), columns=["mean most consistent", "std most consistent", "mean lest consistent", "std least consistent", "tvalue", "pvalue"])
df.to_csv(get_project_path() / "Outdata" / "signed_rank_cv.csv", index=False)



