import pandas as pd
import numpy as np
from sklearn.metrics import explained_variance_score
from sklearn.linear_model import LinearRegression

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

outdata = pd.read_csv("../Others/study_metadata.csv", index_col=0)
outdata["uniform"] = 0
outdata["weighted"] = 0
outdata["mirnas"] = 0
outdata["cases"] = 0
outdata["controls"] = 0
outdata["total"] = 0

explained_vars_uniform = []
explained_vars_weighted = []
num_mirna_seq = []

for study in studies:
    data = get_dataset(study)
    linreg = LinearRegression()
    X = data["cancer"].to_numpy().reshape(-1, 1)
    linreg.fit(X, data.iloc[:,:-1])
    outdata.loc[study, "uniform"] = explained_variance_score(data.iloc[:,:-1], linreg.predict(X), multioutput="uniform_average")
    outdata.loc[study, "weighted"] = explained_variance_score(data.iloc[:,:-1], linreg.predict(X), multioutput="variance_weighted")
    outdata.loc[study, "mirnas"] = len(data.columns) - 1
    outdata.loc[study, "cases"] = data["cancer"].sum()
    outdata.loc[study, "total"] = len(data)

outdata["controls"] = outdata["total"] - outdata["cases"]

outdata.to_csv("../Outdata/studies_table.csv")

