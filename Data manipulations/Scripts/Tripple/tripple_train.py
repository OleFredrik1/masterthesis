from turtle import pen
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from itertools import combinations
from tqdm import tqdm

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset, get_datasets_intersections


study_dict = {s:get_dataset(s) for s in studies}

single_scores = []
double_scores = []

for s1, s2, s3 in tqdm(combinations(studies, 3)):
    data1, data2, data3 = study_dict[s1], study_dict[s2], study_dict[s3]
    mirna_intersection = list(set(data1.columns) & set(data2.columns) & set(data3.columns) - set(["cancer"])) + ["cancer"]
    if len(mirna_intersection) <= 10:
        continue
    data1 = data1.loc[:, mirna_intersection]
    data2 = data2.loc[:, mirna_intersection]
    data3 = data3.loc[:, mirna_intersection]
    linreg1 = LogisticRegression(penalty="none", multi_class="ovr", max_iter=1000) # standard logistic regression
    linreg2 = LogisticRegression(penalty="none", multi_class="ovr", max_iter=1000)
    linreg3 = LogisticRegression(penalty="none", multi_class="ovr", max_iter=1000)
    linreg1.fit(data1.iloc[:, :-1], data1["cancer"])
    linreg2.fit(data2.iloc[:, :-1], data2["cancer"])
    joined = pd.concat([data1, data2])
    linreg3.fit(joined.iloc[:, :-1], joined["cancer"], sample_weight=len(data1)*[1/len(data1)] + len(data2) * [1/len(data2)])
    single_scores.append(roc_auc_score(data3["cancer"], linreg1.predict_proba(data3.iloc[:, :-1])[:, 1]))
    single_scores.append(roc_auc_score(data3["cancer"], linreg2.predict_proba(data3.iloc[:, :-1])[:, 1]))
    double_scores.append(roc_auc_score(data3["cancer"], linreg3.predict_proba(data3.iloc[:, :-1])[:, 1]))

single = pd.DataFrame(np.array(single_scores).transpose(), columns=["single"])
double = pd.DataFrame(np.array(double_scores).transpose(), columns=["double"])
single.to_csv(get_project_path() / "Outdata" / "tripple_single.csv")
double.to_csv(get_project_path() / "Outdata" / "tripple_double.csv")