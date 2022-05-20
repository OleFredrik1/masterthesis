import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

data = [["*" for s1 in studies] for s2 in studies]
for i, study_a in enumerate(studies):
    for j, study_b in enumerate(studies[i+1:]):
        j = i+j+1
        table_a, table_b = get_datasets_intersections([study_a, study_b])
        if len(table_a.columns) >= 10:
            cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
            control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
            cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
            control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
            fold_change_a = cancer_a.mean() - control_a.mean()
            fold_change_b = cancer_b.mean() - control_b.mean()
            corr = pearsonr(fold_change_a, fold_change_b)[0]
            data[i][j] = data[j][i] = corr

df = pd.DataFrame(np.array(data))
df.index = studies
df.columns = studies
df.to_csv(get_project_path() / "Outdata" / "FoldChangeCorrelation.csv")
