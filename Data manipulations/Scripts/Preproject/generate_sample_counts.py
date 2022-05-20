import pandas as pd
import numpy as np

from Utils.config import studies
from Utils.datasets import get_dataset

cases = []
controls = []
for study in studies:
    table = get_dataset(study)
    cases.append(table["cancer"].sum())
    controls.append(len(table) - table["cancer"].sum())

out_data = pd.DataFrame(np.array([controls, cases]).transpose(), columns=["Controls", "Cases"])
out_data["Total"] = out_data["Cases"] + out_data["Controls"]
out_data.sort_values("Total", ascending=False, inplace=True)
del out_data["Total"]
out_data.to_csv("../Outdata/samples_count.csv", index=False)
