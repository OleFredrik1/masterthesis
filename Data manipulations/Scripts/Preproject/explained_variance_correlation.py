from scipy.stats.stats import pearsonr
import pandas as pd
import numpy as np

data = pd.read_csv("../Outdata/explained_variance.csv")
r, p = pearsonr(np.log(data["weighted"]), np.log(data["mirna sequences"]))
print(f"Correlation mirna sequences: {r}, p={p}")
r, p = pearsonr(np.log(data["weighted"]), np.log(data["totals"]))
print(f"Correlation total: {r}, p={p}")
