from collections import defaultdict
from importlib.metadata import metadata
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, ttest_ind

from Utils.config import get_project_path, studies
from Utils.datasets import get_datasets_intersections

np.random.seed(0)

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)
technologies = list(set(t for t in metadata["Technology"] if list(metadata["Technology"]).count(t) > 2))
body_fluids = list(set(t for t in metadata["Body fluid"] if list(metadata["Body fluid"]).count(t) > 2))
res = defaultdict(list)

for i, s1 in enumerate(studies):
    for s2 in studies[i+1:]:
        table_a, table_b = get_datasets_intersections([s1, s2])
        if len(table_a.columns) <= 10:
            continue
        cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
        control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
        cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
        control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
        fold_change_a = cancer_a.mean() - control_a.mean()
        fold_change_b = cancer_b.mean() - control_b.mean()
        corr1, p1 = pearsonr(fold_change_a, fold_change_b)
        table_a["cancer"] = table_a["cancer"].sample(frac=1).values
        table_b["cancer"] = table_b["cancer"].sample(frac=1).values
        cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
        control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
        cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
        control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
        fold_change_a = cancer_a.mean() - control_a.mean()
        fold_change_b = cancer_b.mean() - control_b.mean()
        corr2, p2 = pearsonr(fold_change_a, fold_change_b)
        cur_tech = [metadata.loc[s1, "Technology"], metadata.loc[s2, "Technology"]]
        cur_bf = [metadata.loc[s1, "Body fluid"], metadata.loc[s2, "Body fluid"]]
        for tech in technologies:
            if cur_tech.count(tech) == 2:
                res[(tech, "det")].append(corr1)
                res[(tech, "ran")].append(corr2)
        for bf in body_fluids:
            if cur_bf.count(bf) == 2:
                res[(bf, "det")].append(corr1) 
                res[(bf, "ran")].append(corr2) 

out = []
for tech in technologies:
    det_data, ran_data = res[(tech, "det")], res[(tech, "ran")]
    row = [tech, np.mean(det_data), np.std(det_data, ddof=1), np.mean(ran_data), np.std(ran_data, ddof=1)]
    ttest = ttest_ind(det_data, ran_data)
    row.extend([ttest.statistic, ttest.pvalue])
    out.append(row)

for bf in body_fluids:
    det_data, ran_data = res[(bf, "det")], res[(bf, "ran")]
    row = [bf, np.mean(det_data), np.std(det_data, ddof=1), np.mean(ran_data), np.std(ran_data, ddof=1)]
    ttest = ttest_ind(det_data, ran_data)
    row.extend([ttest.statistic, ttest.pvalue])
    out.append(row)


df = pd.DataFrame(np.array(out), columns=["Group", "mean deterministic", "std deterministic", "mean random", "std random", "t-value", "p-value"])
df.to_csv(get_project_path() / "Outdata" / "log_fold_change_corr_strat_rand.csv", index=False)