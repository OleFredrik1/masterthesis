import pandas as pd
from scipy.stats.stats import ttest_ind
from collections import defaultdict
from sklearn.metrics import roc_auc_score
import numpy as np

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset
from Utils.converters import canonical_to_seq

candidates = ["hsa-miR-21", "hsa-miR-210", "hsa-miR-182", "hsa-miR-155", "hsa-miR-17"]
candidate_seq = canonical_to_seq(candidates)

df = pd.DataFrame(np.array([[np.nan for _ in candidates] for _ in studies]), index=studies, columns=candidates)

for study in studies:
    data = get_dataset(study)
    for cand, seq in zip(candidates, candidate_seq):
        if seq in data.columns:
            df.loc[study][cand] = roc_auc_score(data["cancer"], data[seq])

df.loc["mean"] = df.mean()
df.to_csv(get_project_path() / "Outdata" / "mirna_auc.csv", index_label="study", float_format='%.3f')
