from Utils.config import studies
from Utils.datasets import get_dataset
from math import isclose
from tqdm import tqdm


def check_datasets():
    for study in tqdm(studies):
        table = get_dataset(study)
        # Some tolerance here as standardization was done with respect also to the mirnas that were removed
        # due to missing sequence
        assert isclose(table.iloc[:, :-1].var().mean(), 1, rel_tol=0.1), f"Variance not standardized to 1 for study: {study}"
        assert table.columns[-1] == "cancer", f"Last column is not \"cancer\" for study: {study}"
        assert set("".join(table.columns[:-1])).issubset(set("ACGU")), f"Value columns not RNA-sequences for study: {study}"
