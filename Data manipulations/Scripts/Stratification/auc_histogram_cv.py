import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
from scipy.stats.stats import ttest_1samp
from xgboost import XGBClassifier
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm
mpl.use("pgf")

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections, get_dataset

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

technologies = list(metadata["Technology"])
technologies = list(set(t for t in technologies if technologies.count(t) > 2))
print(technologies)

tot_auc = []
for tech in tqdm(technologies):
    aucs = []
    cur_studies = [get_dataset(s) for s in metadata.loc[metadata["Technology"] == tech].index]
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
    tot_auc.extend(aucs)
    df = pd.DataFrame(np.array(aucs).transpose(), columns=["aucs"])
    df.to_csv(get_project_path() / "Outdata" / f"auc_histogram_cv_{tech.lower().replace(' ', '_')}.csv")

body_fluids = list(metadata["Body fluid"])
body_fluids = list(set(t for t in body_fluids if body_fluids.count(t) > 2))
print(body_fluids)

for fluid in tqdm(body_fluids):
    aucs = []
    cur_studies = [get_dataset(s) for s in metadata.loc[metadata["Body fluid"] == fluid].index]
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
    tot_auc.extend(aucs)
    df = pd.DataFrame(np.array(aucs).transpose(), columns=["aucs"])
    df.to_csv(get_project_path() / "Outdata" / f"auc_histogram_cv_{fluid.lower().replace(' ', '_')}.csv")

df = pd.DataFrame(np.array(tot_auc).transpose(), columns=["aucs"])
df.to_csv(get_project_path() / "Outdata" / "auc_histogram_cv_all.csv")

sm.qqplot(np.array(tot_auc), line="s")
plt.savefig(get_project_path() / "Outdata" / "auc_qqplot_cv.pdf", bbox_inches="tight")


