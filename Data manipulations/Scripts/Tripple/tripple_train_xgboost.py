from turtle import pen
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from itertools import combinations
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset, get_datasets_intersections

study_dict = {s:get_dataset(s) for s in studies}

single_scores = []
double_scores = []

for s1, s2, s3 in tqdm(combinations(studies, 3)):
    data1, data2, data3 = study_dict[s1], study_dict[s2], study_dict[s3]
    mirna_intersection1 = list(set(data1.columns) & set(data2.columns) - set(["cancer"])) + ["cancer"]
    mirna_intersection2 = list(set(data1.columns) & set(data2.columns) & set(data3.columns) - set(["cancer"])) + ["cancer"]
    if len(mirna_intersection2) <= 10:
        continue
    data1 = data1.loc[:, mirna_intersection1]
    data2 = data2.loc[:, mirna_intersection1]
    new_data3 = pd.DataFrame()
    for col in mirna_intersection1:
        if col in data3.columns:
            new_data3[col] = data3[col]
        else:
            new_data3[col] = np.nan
    data3 = new_data3
    xgb1 = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    xgb2 = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    xgb3 = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    xgb1.fit(data1.iloc[:, :-1], data1["cancer"])
    xgb2.fit(data2.iloc[:, :-1], data2["cancer"])
    joined = pd.concat([data1, data2])
    xgb3.fit(joined.iloc[:, :-1], joined["cancer"], sample_weight=len(data1)*[len(data2)] + len(data2) * [len(data1)])
    single_scores.append(roc_auc_score(data3["cancer"], xgb1.predict_proba(data3.iloc[:, :-1])[:, 1]))
    single_scores.append(roc_auc_score(data3["cancer"], xgb2.predict_proba(data3.iloc[:, :-1])[:, 1]))
    double_scores.append(roc_auc_score(data3["cancer"], xgb3.predict_proba(data3.iloc[:, :-1])[:, 1]))

single = pd.DataFrame(np.array(single_scores).transpose(), columns=["single"])
double = pd.DataFrame(np.array(double_scores).transpose(), columns=["double"])
single.to_csv(get_project_path() / "Outdata" / "tripple_single_xgb.csv")
double.to_csv(get_project_path() / "Outdata" / "tripple_double_xgb.csv")