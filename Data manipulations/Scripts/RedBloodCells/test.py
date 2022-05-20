from collections import defaultdict
import numpy as np
import pandas as pd

from Utils.converters import canonical_to_seq
from Utils.datasets import get_dataset
from Utils.config import studies, get_project_path

to_check, control = canonical_to_seq(["hsa-miR-486-5p", "hsa-miR-21-5p"])
metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

res = defaultdict(list)
for s in studies:
    data = get_dataset(s)
    if to_check in data.columns and control in data.columns and data[control].mean() != 0:
        #print(f"{s} ({metadata.loc[s, 'Technology']}, {metadata.loc[s, 'Body fluid']}): {((data[to_check].mean() - data[control].mean()) / data[control].mean()) * 100:.3f}%")
        res[metadata.loc[s, "Body fluid"]].append(((data[to_check].mean() - data[control].mean()) / data[control].mean()))

for k, v  in res.items():
    print(f"{k}: {np.median(v) * 100:.3f}%")

