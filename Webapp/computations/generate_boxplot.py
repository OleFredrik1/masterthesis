from collections import defaultdict
from pathlib import Path
import sys
import json
import numpy as np
from scipy.stats import ttest_ind

from Utils.config import studies
from Utils.datasets import get_dataset
from Utils.converters import get_seq_lookup_table

lookup = get_seq_lookup_table()
out = defaultdict(dict)
meta = {"p-values": {}}
for study in studies:
    data = get_dataset(study)
    for mirna in data.columns[:-1]:
        if mirna in lookup:
            mirbase = lookup[mirna]
        else:
            continue
        if "cases" not in out[mirbase]:
            out[mirbase]["cases"] = defaultdict(list)
        if "controls" not in out[mirbase]:
            out[mirbase]["controls"] = defaultdict(list)
        if "p-values" not in out[mirbase]:
            out[mirbase]["p-values"] = {}
        if "separation" not in out[mirbase]:
            out[mirbase]["separation"] = {}
        cases = list(data.loc[data["cancer"] == 1, mirna])
        out[mirbase]["cases"]["studies"].extend(len(cases) * [study])
        out[mirbase]["cases"]["values"].extend(cases)
        controls = list(data.loc[data["cancer"] == 0, mirna])
        out[mirbase]["controls"]["studies"].extend(len(controls) * [study])
        out[mirbase]["controls"]["values"].extend(controls)
        out[mirbase]["p-values"][study] = ttest_ind(cases, controls).pvalue
        out[mirbase]["separation"][study] = np.mean(cases) - np.mean(controls)
    meta[study] = {"cases": len(cases), "controls": len(controls), "mirnas": len(data.columns[:-1])}

mirnas = list(out.keys())
real_mirnas = []
num_p_values = 0
for mirna in mirnas:
    try:
        with open(Path(sys.path[0]) / "Outdata" / "Boxplot" / f"{mirna}.json", "w") as f:
            pass
        real_mirnas.append(mirna)
        num_p_values += len(out[mirna]["p-values"])
    except:
        pass

for mirna in real_mirnas:
    meta["p-values"][mirna] = ttest_ind(out[mirna]["cases"]["values"], out[mirna]["controls"]["values"]).pvalue * len(real_mirnas)
    with open(Path(sys.path[0]) / "Outdata" / "Boxplot" / f"{mirna}.json", "w") as f:
        out[mirna]["p-values"] = {s: num_p_values * p for s, p in out[mirna]["p-values"].items()}
        f.write(json.dumps(out[mirna]))

meta["mirnas"] = real_mirnas
with open(Path(sys.path[0]) / "Outdata" / "Boxplot" / "meta.json", "w") as f:
    f.write(json.dumps(meta))
