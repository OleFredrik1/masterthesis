import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
from scipy.stats.stats import ttest_ind

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

microarrays = list(metadata["Subtype"])
microarrays = list(set(t for t in microarrays if microarrays.count(t) >= 2 and "microarray" in t))
print(microarrays)

studies = [s for s in studies if metadata.loc[s, "Technology"] == "Microarray"]

in_auc = []
out_auc = []
for s1 in tqdm(studies, leave=False):
    for s2 in studies:
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns) < 10 or s1 == s2:
            continue
        logreg = LogisticRegression(penalty="none", max_iter=1000)
        logreg.fit(data1.iloc[:, :-1], data1["cancer"])
        auc = roc_auc_score(data2["cancer"], logreg.predict_proba(data2.iloc[:, :-1])[:, 1])
        if metadata.loc[s1, "Subtype"] == metadata.loc[s2, "Subtype"]:
            in_auc.append(auc)
        else:
            out_auc.append(auc)
t_test = ttest_ind(in_auc, out_auc)
res = [[np.mean(in_auc), np.std(in_auc, ddof=1), np.mean(out_auc), np.std(out_auc, ddof=1), t_test.statistic, t_test.pvalue]]

df = pd.DataFrame(np.array(res), columns=["in-mean", "in-std", "out-mean", "out-std", "t-value", "p-value"])
df.to_csv(get_project_path() / "Outdata" / "auc_microarray_pairs.csv", index=False)