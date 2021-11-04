import pandas as pd

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

for i, study_a in enumerate(studies):
    for study_b in studies[i+1:]:
        table_a, table_b = get_datasets_intersections([study_a, study_b])
        if len(table_a.columns) >= 10:
            cancer_a = table_a.loc[table_a["cancer"] == 1].iloc[:, :-1]
            control_a = table_a[table_a["cancer"] == 0].iloc[:, :-1]
            cancer_b = table_b[table_b["cancer"] == 1].iloc[:, :-1]
            control_b = table_b[table_b["cancer"] == 0].iloc[:, :-1]
            fold_change_a = cancer_a.mean() - control_a.mean()
            fold_change_b = cancer_b.mean() - control_b.mean()
            df = pd.DataFrame({"Fold change A": fold_change_a, "Fold change B": fold_change_b})
            df.to_csv(get_project_path() / "Outdata" / "FoldChangeCorrelations" / f"{study_a}_v_{study_b}.csv", index=False)