import pandas as pd
from utils.cli_output_utils import print_plain, print_good, print_bad, print_warning
from tabulate import tabulate

def apply(df: pd.DataFrame) -> None:
    show_df_overview(df)
    show_df_columns(df)

def show_df_overview(df: pd.DataFrame) -> None:
    print_plain('DataFrame Overview:')
    overview = pd.DataFrame({
        'Total rows': [df.shape[0]],
        'Total columns': [df.shape[1]],
        'Rows with at least one null value': [df.isnull().any(axis=1).sum()]
    })
    print(tabulate(overview, tablefmt = 'psql', headers = overview.columns))


def show_df_columns(df: pd.DataFrame) -> None:
    print_plain('Column breakdown:')
    summary = df.describe().T
    summary['null_count'] = df[summary.index].isnull().sum()
    cols_order = ['count', 'unique', 'null_count', 'top', 'freq']
    print(tabulate(summary[cols_order], tablefmt = 'grid', headers = cols_order, maxcolwidths=75))