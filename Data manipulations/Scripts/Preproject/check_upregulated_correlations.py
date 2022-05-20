import numpy as np
from scipy.stats.stats import pearsonr

from Utils.datasets import get_dataset
from Utils.config import studies
from converters import canonical_to_seq


common_upregulated = ["hsa-miR-21", "hsa-miR-205", "hsa-miR-210", "hsa-miR-155", "hsa-miR-182", "hsa-miR-200b",
                      "hsa-miR-17", "hsa-miR-223", "hsa-miR-486"]#["hsa-miR-21", "hsa-miR-210", "hsa-miR-182", "hsa-miR-155", "hsa-miR-17", "hsa-miR-205", "hsa-miR-451", "hsa-miR-125a"]
#common_upregulated += ["hsa-miR-126", "hsa-miR-486"]
upreg_seq = canonical_to_seq(common_upregulated)
reverse = {u:c for u,c in zip(upreg_seq, common_upregulated)}
print(upreg_seq)

for study in studies:
    s = 0
    t = 0
    print(f"--- {study} ---")
    table = get_dataset(study)
    this_upreg = np.array(list(set(table.columns) & set(upreg_seq)))
    controls, cancer = table[table["cancer"] == 0], table[table["cancer"] == 1]
    for i, mirna1 in enumerate(this_upreg):
        for mirna2 in this_upreg[i+1:]:
            r1 = cancer[mirna1].mean() - controls[mirna1].mean()
            r2 = cancer[mirna2].mean() - controls[mirna2].mean()
            t += 1
            s += (r1 * r2) > 0
    print(s/t if t>0 else "None")
    print()