import pandas as pd

WIKI = "https://en.wikipedia.org/wiki/"


def get_symbols_in_indices(indices: list[str]):
    symbols = []

    if 'CAC40' in indices:
        symbols.extend(
            pd.read_html(WIKI + "CAC_40", flavor="html5lib")[4]["Ticker"].to_list()
        )

    if "S&P500" in indices:
        symbols.extend(
            pd.read_html(WIKI + "List_of_S%26P_500_companies", flavor="html5lib")[0][
                "Symbol"
            ].to_list()
        )

    if "FTSE100" in indices:
        symbols.extend(
            pd.read_html(WIKI + "FTSE_100_Index", flavor="html5lib")[4][
                "EPIC"
            ].to_list()
        )

    if "DAX" in indices:
        symbols.extend(
            pd.read_html(WIKI + "DAX", flavor="html5lib")[4]["Ticker"].to_list()
        )

    return symbols


if __name__ == "__main__":
    print(get_symbols_in_indices(['CAC40']))
