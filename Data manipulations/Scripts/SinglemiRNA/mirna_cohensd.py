import pandas as pd
import numpy as np
from collections import defaultdict

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset
from Utils.converters import canonical_to_seq

candidates = ["hsa-miR-21", "hsa-miR-210", "hsa-miR-182", "hsa-miR-155", "hsa-miR-17"]
candidate_seq = canonical_to_seq(candidates)

df = pd.DataFrame(np.array([[np.nan for _ in candidates] for _ in studies]), index=studies, columns=candidates)

for study in studies:
    data = get_dataset(study)
    cancer = data[data["cancer"] == 1]
    healthy = data[data["cancer"] == 0]
    cohensd = (cancer.mean() - healthy.mean())/(((len(cancer) - 1) * cancer.std() + (len(healthy) - 1) * healthy.std()) / (len(data) - 2))
    for cand, seq in zip(candidates, candidate_seq):
        if seq in data.columns:
            df.loc[study][cand] = cohensd[seq] 

df.loc["mean"] = df.mean()
df.to_csv(get_project_path() / "Outdata" / "mirna_cohensd.csv", index_label="study", float_format='%.3f')
