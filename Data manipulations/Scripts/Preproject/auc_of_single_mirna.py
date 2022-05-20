import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score

from Utils.datasets import get_dataset, get_project_path
from Utils.config import studies

mirna = "ACUGCAGUGAAGGCACUUGUAG"

out = []
for study in studies:
    data = get_dataset(study)
    if mirna in data.columns:
        auc = roc_auc_score(data["cancer"], data[mirna])
        out.append([study, auc])

out = sorted(out, key=lambda x:x[1], reverse=True)
df = pd.DataFrame(np.array(out), columns=["study", "AUC"])
df.to_csv(get_project_path() / "Outdata" / "AUC-miR-17-3p.csv", index=False)