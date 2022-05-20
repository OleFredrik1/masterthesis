from collections import defaultdict
import pandas as pd
import numpy as np

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset
from Utils.converters import canonical_to_seq

metadata = pd.read_csv(get_project_path() / "Dataset" / "Technology-body-fluid.csv", index_col=0)

in_RBC_names = ["hsa-miR-486-5p", "hsa-miR-451a"]
in_RBC = canonical_to_seq(in_RBC_names)

res = defaultdict(lambda: defaultdict(list))
for s in studies:
    data = get_dataset(s)
    for name, seq in zip(in_RBC_names, in_RBC):
        if seq in data.columns:
            res[metadata.loc[s, "Body fluid"]][name].append(data[seq].std())

print(res)

for k, v in res.items():
    res[k] = [np.mean(v[name]) if name in v else "" for name in in_RBC_names]

pd.DataFrame.from_dict(res, orient="index", columns=in_RBC_names).to_csv(get_project_path() / "Outdata" / "relative_variance_body_fluid.csv", index_label="study")

