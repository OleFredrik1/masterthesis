from cgitb import lookup
from collections import defaultdict
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon, ttest_ind
from itertools import combinations
from tqdm import tqdm

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset
from Utils.converters import get_seq_lookup_table

log_fold = defaultdict(list)
t_test = defaultdict(list)
lookup_table = get_seq_lookup_table()

for study in studies:
    data = get_dataset(study)
    cancers = data.loc[data["cancer"] == 1].iloc[:, :-1]
    healthy = data.loc[data["cancer"] == 0].iloc[:, :-1]
    for seq in data.columns[:-1]:
        ttest = ttest_ind(cancers[seq], healthy[seq])
        log_fold[seq].append(cancers[seq].mean() - healthy[seq].mean())
        t_test[seq].append(np.sign(ttest.statistic)/ttest.pvalue)

log_fold_res = [(wilcoxon(v).pvalue, seq) for seq, v in log_fold.items() if len(v) >= 10]
t_test_res = [(wilcoxon(v).pvalue, seq) for seq, v in t_test.items() if len(v) >= 10]
log_fold_res.sort()
t_test_res.sort()

out = []
for i in range(10):
    row = []
    pval, seq = log_fold_res[i]
    print(len(log_fold[seq]))
    row.append(lookup_table[seq])
    row.append(pval * len(log_fold_res))
    row.append("Up" if wilcoxon(log_fold[seq], alternative="greater").pvalue < wilcoxon(log_fold[seq]).pvalue else "Down")   
    pval, seq = t_test_res[i]
    row.append(lookup_table[seq])
    row.append(pval * len(t_test_res))
    row.append("Up" if wilcoxon(t_test[seq], alternative="greater").pvalue < wilcoxon(t_test[seq]).pvalue else "Down")
    out.append(row)

df = pd.DataFrame(np.array(out), columns=["miRNA log-fold-change", "p-value log-fold-change", "direction log-fold-change", "miRNA t-value", "p-value t-value", "direction t-value"])
df.to_csv(get_project_path() / "Outdata" / "signed_rank.csv", index=False)



