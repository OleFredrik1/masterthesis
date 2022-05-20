import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
from scipy.stats.stats import ttest_1samp
from xgboost import XGBClassifier, training

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections, get_dataset

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

microarrays = list(metadata["Subtype"])
microarrays = list(set(t for t in microarrays if microarrays.count(t) >= 2 and "microarray" in t))
print(microarrays)


aucs = []
for microarray in tqdm(microarrays):
    cur_studies = [get_dataset(s) for s in metadata.loc[metadata["Subtype"] == microarray].index]
    mirnas = list(set.union(*[set(s.columns) for s in cur_studies]) - set(["cancer"])) + ["cancer"]
    datasets = []
    for study in cur_studies:
        df = pd.DataFrame()
        for mirna in mirnas:
            if mirna in study.columns:
                df[mirna] = study[mirna]
            else:
                df[mirna] = np.nan
        datasets.append(df)
    for i, test_set in enumerate(datasets):
        training_set = pd.concat(datasets[:i] + datasets[i+1:])
        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        xgb.fit(training_set.iloc[:, :-1], training_set["cancer"])
        aucs.append(roc_auc_score(test_set["cancer"], xgb.predict_proba(test_set.iloc[:, :-1])[:, 1]))

ttest = ttest_1samp(aucs, 0.5, alternative="greater")
res = [[np.mean(aucs), np.std(aucs, ddof=1), ttest.statistic, ttest.pvalue]]

df = pd.DataFrame(np.array(res), columns=["mean", "std", "t-value", "p-value"])
df.to_csv(get_project_path() / "Outdata" / "auc_microarray_cv.csv", index=False)
