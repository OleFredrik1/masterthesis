import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

from Utils.config import studies, get_project_path
from Utils.datasets import get_dataset

for study in studies:
    table = get_dataset(study)
    data = table.iloc[:, :-1]
    pca = PCA(n_components=2)
    components = pca.fit_transform(data)
    sample_type = np.array(["Cancer" if i else "Control" for i in table["cancer"]])
    out_df = pd.DataFrame(components)
    out_df.columns = ["PCA1", "PCA2"]
    out_df["Type"] = sample_type
    out_df.to_csv(get_project_path() / "Outdata" / "PCA" / f"{study}.csv")
