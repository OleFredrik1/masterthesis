import numpy as np

from Utils.datasets import get_dataset
from Utils.config import studies
from converters import canonical_to_seq

common_upregulated = ["hsa-miR-21", "hsa-miR-205", "hsa-miR-210", "hsa-miR-155", "hsa-miR-182", "hsa-miR-200b",
                      "hsa-miR-17", "hsa-miR-223", "hsa-miR-486", "hsa-miR-126"]#["hsa-miR-21", "hsa-miR-210", "hsa-miR-182", "hsa-miR-155", "hsa-miR-17", "hsa-miR-205", "hsa-miR-451", "hsa-miR-125a"]
#common_upregulated += ["hsa-miR-126", "hsa-miR-486"]
upreg_seq = canonical_to_seq(common_upregulated)
reverse = {u:c for u,c in zip(upreg_seq, common_upregulated)}
print(upreg_seq)

total_corrs = []
for study in studies:
    table = get_dataset(study)
    this_upreg = np.array(list(set(table.columns) & set(upreg_seq)))
    columns = [reverse[c] for c in this_upreg]
    controls, cancer = table[table["cancer"] == 0][this_upreg], table[table["cancer"] == 1][this_upreg]
    controls.columns = cancer.columns = columns
    print(f"--- {study} ---")
    print(cancer.mean() - controls.mean())
    print()