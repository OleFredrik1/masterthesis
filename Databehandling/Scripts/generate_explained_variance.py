from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score
import pandas as pd

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

df = pd.DataFrame(columns=["Study", "Uniformly weighted", "Variance weighted"])
for study in studies:
    new_row = {"Study": study}
    table = get_dataset(study)
    linreg = LinearRegression()
    X = table["cancer"].to_numpy().reshape(-1, 1)
    Y = table.iloc[:, :-1]
    linreg.fit(X, Y)
    fitted = linreg.predict(X)
    new_row["Uniformly weighted"] = explained_variance_score(Y, fitted, multioutput="uniform_average")
    new_row["Variance weighted"] = explained_variance_score(Y, fitted, multioutput="variance_weighted")
    df = df.append(new_row, ignore_index=True)

df.to_csv(get_project_path() / "Outdata" / "ExplainedVariance.csv", index=False)

