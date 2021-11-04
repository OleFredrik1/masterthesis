import pandas as pd

from .config import studies, get_project_path


def get_dataset(study: str, standardized: bool=False) -> pd.DataFrame:
    path = get_project_path() / "TransformedData" / (study + ".csv")
    table = pd.read_csv(path)
    if standardized:
        values = table.iloc[:, :-1]
        cancer = table.iloc[:, -1]
        values = values.loc[:, values.std() > 0]
        values /= values.std()
        table = pd.concat([values, cancer], axis=1)
    else:
        table = table.loc[:, table.std() > 0]
        controls, cancer = table[table["cancer"] == 0].iloc[:, :-1], table[table["cancer"] == 1].iloc[:, :-1]
        table.iloc[:, :-1] -= 0.5 * controls.mean() + 0.5 * cancer.mean()
        table.iloc[:, :-1] /= (0.5 * controls.var() + 0.5 * cancer.var()).pow(1/2)
    return table


def get_datasets_intersections(studies: list[str], standardized: bool=False) -> list[pd.DataFrame]:
    tables = [get_dataset(study, standardized) for study in studies]
    sequences = [set(table.columns[:-1]) for table in tables]
    intersection = list(set.intersection(*sequences)) + ["cancer"]
    return [table.loc[:, intersection] for table in tables]
