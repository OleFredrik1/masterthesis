import pandas as pd
import numpy as np
from sklearn.metrics import explained_variance_score
from sklearn.linear_model import LinearRegression

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

explained_vars_uniform = []
explained_vars_weighted = []
num_mirna_seq = []
totals = []

for study in studies:
    data = get_dataset(study)
    linreg = LinearRegression()
    X = data["cancer"].to_numpy().reshape(-1, 1)
    linreg.fit(X, data.iloc[:,:-1])
    explained_vars_uniform.append(explained_variance_score(data.iloc[:,:-1], linreg.predict(X), multioutput="uniform_average"))
    explained_vars_weighted.append(explained_variance_score(data.iloc[:,:-1], linreg.predict(X), multioutput="variance_weighted"))
    num_mirna_seq.append(len(data.columns) - 1)
    totals.append(len(data))

df = pd.DataFrame(np.array([explained_vars_uniform, explained_vars_weighted, num_mirna_seq, totals]).transpose(),
                  columns=["uniform", "weighted", "mirna sequences", "totals"])
df.index = studies
df.index.name = "study"
df.to_csv(get_project_path() / "Outdata" / "explained_variance.csv")
