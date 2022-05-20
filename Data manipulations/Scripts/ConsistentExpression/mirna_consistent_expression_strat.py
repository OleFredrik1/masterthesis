from numpy import sign
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, binomtest
from collections import defaultdict

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset


metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)
technologies = list(set(t for t in metadata["Technology"] if list(metadata["Technology"]).count(t) > 2))
body_fluids = list(set(t for t in metadata["Body fluid"] if list(metadata["Body fluid"]).count(t) > 2))
res = defaultdict(list)

for study in studies:
    data = get_dataset(study)
    cancers = data[data["cancer"] == 1].iloc[:, :-1]
    healthy = data[data["cancer"] == 0].iloc[:, :-1]
    t_values = ttest_ind(cancers, healthy)
    for seq, t_value, p_value in zip(data.columns[:-1], t_values.statistic, t_values.pvalue):
        res[seq].append((t_value, p_value, study))

tech_vals =  [(t, []) for t in technologies]
fluid_vals = [(t, []) for t in body_fluids]
for l in res.values():
    for i, v1 in enumerate(l):
        for v2 in l[i+1:]:
            if v1[1] < 0.05 and v1[1] < 0.05:
                for tech, li in tech_vals:
                    if metadata.loc[v1[2], "Technology"] == metadata.loc[v2[2], "Technology"] == tech:
                        li.append(sign(v1[0]) == sign(v2[0])) 
                for fluid, li in fluid_vals:
                    if metadata.loc[v1[2], "Body fluid"] == metadata.loc[v2[2], "Body fluid"] == fluid:
                        li.append(sign(v1[0]) == sign(v2[0])) 


res = [binomtest(sum(l), len(l), alternative="greater") for _, l in tech_vals + fluid_vals]
df = pd.DataFrame(np.array([[t.proportion_estimate, t.pvalue] for t in res]), index=[str(v) for v, _ in tech_vals + fluid_vals], columns=["probability", "pvalue"])
df.to_csv(get_project_path() / "Outdata" / "mirna_consistent_expression_strat.csv", index_label="Group")
