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

res = []
for i, test_data in enumerate(datasets):
    training_data = pd.concat(datasets[:i] + datasets[i+1:])
    logreg = XGBClassifier(eval_metric="logloss", use_label_encoder=False)#LogisticRegression(penalty="none", max_iter=1000)
    logreg.fit(training_data.iloc[:, :-1], training_data["cancer"])
    res.append(roc_auc_score(test_data["cancer"], logreg.predict_proba(test_data.iloc[:, :-1])[:, 1]))


df = pd.DataFrame(np.array(res).transpose(), index=seq_studies, columns=["aucs"])
df.to_csv(get_project_path() / "Outdata" / "auc_sequencing_cv.csv", index_label="Study")
