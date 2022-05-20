import pandas as pd
import numpy as np
from sklearn.metrics import explained_variance_score
from sklearn.linear_model import LinearRegression

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

out = []
for s in studies:
    data = get_dataset(s)
    out.append([metadata.loc[s, "Technology"], metadata.loc[s, "Body fluid"], len(data.columns) - 1, (data["cancer"] == 1).sum(), (data["cancer"] == 0).sum(), len(data)])

pd.DataFrame(out, index=studies, columns=["Technology", "Body fluid", "miRNAs", "Cases", "Controls", "Total"]).to_csv(get_project_path() / "Outdata" / "study_table.csv", index_label="Study")

