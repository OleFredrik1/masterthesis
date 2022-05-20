import pandas as pd
import numpy as np

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
            row.append(data[seq].std())
        else:
            row.append("")
    if row.count("") != 2:
        res.append([s] + row)

pd.DataFrame(res, columns=["study"] + in_RBC_names).to_csv(get_project_path() / "Outdata" / "relative_variance.csv", index=False)
