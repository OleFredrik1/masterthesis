import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm
mpl.use("pgf")

from Utils.config import studies, get_project_path
from Utils.datasets import get_datasets_intersections

test = np.array([2,3,5,3,2,3,4,3,2,3,4,3,2,3,2,3,3,4,3])
sm.qqplot(test, line="s")
plt.savefig(get_project_path() / "Outdata" / "auc_qqplot_cv.pdf", bbox_inches="tight")

