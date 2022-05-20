import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
from scipy.stats.stats import ttest_ind

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

technologies = list(metadata["Technology"])
technologies = list(set(t for t in technologies if technologies.count(t) > 2))
print(technologies)

res = []
for tech in tqdm(technologies):
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
            c = [metadata.loc[s1, "Technology"], metadata.loc[s2, "Technology"]].count(tech)
            if c == 1:
                out_auc.append(auc)
            if c == 2:
                in_auc.append(auc)
    t_test = ttest_ind(in_auc, out_auc)
    res.append([np.mean(in_auc), np.std(in_auc, ddof=1), np.mean(out_auc), np.std(out_auc, ddof=1), t_test.statistic, t_test.pvalue])

df = pd.DataFrame(np.array(res), index = technologies, columns=["in-mean", "in-std", "out-mean", "out-std", "t-value", "p-value"])
df.to_csv(get_project_path() / "Outdata" / "auc_technology_pairs.csv", index_label="technology")