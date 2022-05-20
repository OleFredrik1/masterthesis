import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from scipy.stats import ttest_1samp

from Utils.config import staged_studies, get_project_path
from Utils.datasets import get_dataset_staged

datasets = [get_dataset_staged(s) for s in staged_studies]
minra_list = list(set.union(*[set(data.columns) for data in datasets]) - set(["cancer", "stage"])) + ["cancer", "stage"]
new_datasets = []
for data in datasets:
    new_data = pd.DataFrame()
    for mirna in minra_list:
        if mirna in data.columns:
            new_data[mirna] = data[mirna]
        else:
            new_data[mirna] = np.nan
    new_datasets.append(new_data)
datasets = new_datasets
aucs_early = []
aucs_late = []

for i in range(len(datasets)):
    training_data = datasets[:i] + datasets[i+1:]
    test_data = datasets[i]
    joined = pd.concat(training_data)
    if test_data["stage"].isin([1,2]).sum() > 0:
        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        early_joined = joined[joined["stage"].isin([0,1,2])]
        xgb.fit(early_joined.iloc[:, :-2], early_joined["cancer"])
        early_test = test_data[test_data["stage"].isin([0,1,2])]
        aucs_early.append(roc_auc_score(early_test["cancer"], xgb.predict_proba(early_test.iloc[:, :-2])[:, 1]))
    if test_data["stage"].isin([3,4]).sum() > 0: 
        xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        late_joined = joined[joined["stage"].isin([0,3,4])]
        xgb.fit(late_joined.iloc[:, :-2], late_joined["cancer"])
        late_test = test_data[test_data["stage"].isin([0,3,4])]
        aucs_late.append(roc_auc_score(late_test["cancer"], xgb.predict_proba(late_test.iloc[:, :-2])[:, 1]))

res = []
ttest = ttest_1samp(aucs_early, 0.5)
res.append([np.mean(aucs_early), np.std(aucs_early, ddof=1), ttest.statistic, ttest.pvalue])
ttest = ttest_1samp(aucs_late, 0.5)
res.append([np.mean(aucs_late), np.std(aucs_late, ddof=1), ttest.statistic, ttest.pvalue])

df = pd.DataFrame(np.array(res), columns=["Mean", "Std", "t-value", "p-value"], index=["Early", "Late"])
df.to_csv(get_project_path() / "Outdata" / "auc_merged_stages.csv", index_label="Stage")
