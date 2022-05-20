import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from tqdm import tqdm


from Utils.config import studies
from Utils.datasets import get_datasets_intersections

studies.remove("Boeri2011")

for study_a in ["Boeri2011", "Boeri2011_adjusted"]: #["Asakura2020", "Asakura2020_transformed", "Asakura2020_adjusted"]:
    auc_s = []
    for study_b in tqdm(studies):
        table_a, table_b = get_datasets_intersections([study_a, study_b])
        assert np.all(table_a.columns == table_b.columns)
        if len(table_a.columns) >= 10:
            logreg = LogisticRegression(max_iter=1000)
            logreg.fit(table_a.iloc[:, :-1], table_a["cancer"])
            y_pred = logreg.predict(table_b.iloc[:, :-1])
            auc = roc_auc_score(table_b["cancer"], y_pred)
            if auc > 0.9:
                print(study_b)
            auc_s.append(auc)
    print(auc_s)