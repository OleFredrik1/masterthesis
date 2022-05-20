import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
from scipy.stats.stats import ttest_1samp
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections, get_dataset

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv")

seq_studies = list(metadata.loc[metadata["Technology"] == "Sequencing", "Study"])
datasets = get_datasets_intersections(seq_studies)

training_data = pd.concat(datasets)
xgb = XGBClassifier(eval_metric="logloss", use_label_encoder=False)#LogisticRegression(penalty="none", max_iter=1000)
xgb.fit(training_data.iloc[:, :-1], training_data["cancer"])

other_datasets = [get_dataset(s) for s in studies]
res = []
mirnas = datasets[0].columns
for data in other_datasets:
    new_data = pd.DataFrame()
    for mirna in mirnas:
        if mirna in data.columns:
            new_data[mirna] = data[mirna]
        else:
            new_data[mirna] = np.nan
    res.append(roc_auc_score(new_data["cancer"], xgb.predict_proba(new_data.iloc[:, :-1])[:, 1]))


df = pd.DataFrame(np.array(res).transpose(), index=studies, columns=["aucs"])
df.to_csv(get_project_path() / "Outdata" / "auc_sequencing_cv2.csv", index_label="Study")
