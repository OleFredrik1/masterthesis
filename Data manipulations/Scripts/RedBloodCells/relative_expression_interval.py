import pandas as pd
import numpy as np
import scipy.stats as st

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset
from Utils.converters import canonical_to_seq


in_RBC_names = ["hsa-miR-486-5p", "hsa-miR-451a"]
in_RBC = canonical_to_seq(in_RBC_names)

res = []
for s in studies:
    data = get_dataset(s)
    row = []
    for seq in in_RBC:
        if seq in data.columns:
            lower, upper = st.t.interval(0.95, len(data[seq])-1, loc=data[seq].mean(), scale=(len(data[seq])-1) / len(data[seq]) * data[seq].std())
            row.append(data[seq].apply(lambda x: lower <= x <= upper).mean())
        else:
            row.append("")
    if row.count("") != 2:
        res.append([s] + row)

pd.DataFrame(res, columns=["study"] + in_RBC_names).to_csv(get_project_path() / "Outdata" / "relative_expression_interval.csv", index=False)

