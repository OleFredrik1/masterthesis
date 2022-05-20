from collections import defaultdict
import numpy as np
import pandas as pd

from Utils.converters import canonical_to_seq
from Utils.datasets import get_dataset
from Utils.config import studies, get_project_path

in_RBC_names = ["hsa-miR-486-5p", "hsa-miR-451a"]
controls_names = ["hsa-miR-16", "hsa-miR-93"]
in_RBC = canonical_to_seq(in_RBC_names)
controls = canonical_to_seq(controls_names)

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

res = []
for s in studies:
    row = []
    data = get_dataset(s)
    for r in in_RBC:
        for c in controls:
            if r in data.columns and c in data.columns and data[c].mean() != 0:
                #print(f"{s} ({metadata.loc[s, 'Technology']}, {metadata.loc[s, 'Body fluid']}): {((data[to_check].mean() - data[control].mean()) / data[control].mean()) * 100:.3f}%")
                row.append(f"{((data[r].mean() - data[c].mean()) / data[c].mean())*100:.3f}%")
            else:
                row.append("")
    if row.count("") != len(row):
        res.append([s] + row)

columns = ["study"] + [f"{r}_vs_{c}" for r in in_RBC_names for c in controls_names]
pd.DataFrame(res, columns=columns).to_csv(get_project_path() / "Outdata" / "relative_expression.csv", index=False)

