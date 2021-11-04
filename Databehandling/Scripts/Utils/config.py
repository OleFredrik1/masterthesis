import pathlib

studies = ["Asakura2020", "Bianchi2011", "Boeri2011", "Chen2019", "Duan2021",
           "Fehlmann2020", "Halvorsen2016", "Jin2017", "Keller2009",
           "Keller2014", "Keller2020", "Kryczka2021", "Leidinger2011", "Leidinger2014",
           "Leidinger2015", "Leidinger2016", "Li2017", "Marzi2016", "Nigita2018",
           "Patnaik2012", "Patnaik2017", "Qu2017", "Reis2020", "Wozniak2015",
           "Yao2020", "Zaporozhchenko2018"]

common_regulated = ["hsa-miR-21", "hsa-miR-205", "hsa-miR-210", "hsa-miR-155", "hsa-miR-182", "hsa-miR-200b",
                    "hsa-miR-17", "hsa-miR-223", "hsa-miR-486"]


def get_project_path() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent.parent.resolve()
