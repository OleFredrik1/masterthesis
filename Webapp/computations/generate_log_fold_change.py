from collections import defaultdict
from pathlib import Path
from scipy.stats import linregress, ttest_ind
import json
import sys

from Utils.config import studies
from Utils.datasets import get_datasets_intersections
from Utils.converters import get_seq_lookup_table

lookup_table = get_seq_lookup_table()
get_mirna = lambda x: lookup_table[x] if x in lookup_table else "Unknown"
meta = defaultdict(list)
for s1 in studies:
    for s2 in studies:
        if s1 == s2:
            continue
        data1, data2 = get_datasets_intersections([s1, s2])
        if len(data1.columns[:-1]) < 4:
            continue
        meta[s1].append(s2)
        cancer1 = data1.loc[data1["cancer"] == 1].iloc[:, :-1]
        control1 = data1[data1["cancer"] == 0].iloc[:, :-1]
        cancer2 = data2[data2["cancer"] == 1].iloc[:, :-1]
        control2 = data2[data2["cancer"] == 0].iloc[:, :-1]
        fold_change1 = cancer1.mean() - control1.mean()
        fold_change2 = cancer2.mean() - control2.mean()
        slope, intercept, corr, p, _ = linregress(fold_change1, fold_change2)
        with open(Path(sys.path[0]) / "Outdata" / "LogFoldChange" / f"{s1}_vs_{s2}.json", "w") as f:
            f.write(json.dumps({
                "corr": corr, "p-value": p, "slope": slope, "intercept": intercept, s1: list(fold_change1),
                 s2: list(fold_change2), "mirnas": list(map(get_mirna, data1.columns[:-1])),
                 "p-values": {s1: ttest_ind(cancer1, control1).pvalue.tolist(), s2: ttest_ind(cancer2, control2).pvalue.tolist()}
                 }))

with open(Path(sys.path[0]) / "Outdata" / "LogFoldChange" / "meta.json", "w") as f:
    f.write(json.dumps(meta))