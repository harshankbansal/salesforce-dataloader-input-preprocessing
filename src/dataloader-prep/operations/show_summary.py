import pandas as pd
from utils.cli_output_utils import print_plain, print_good, print_bad, print_warning

def apply(df: pd.DataFrame) -> None:
    show_df_overview(df)
    show_df_columns(df)

def show_df_overview(df: pd.DataFrame) -> None:
    print_plain('-' * 100)
    print_plain('DataFrame Overview:')
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    print_plain(f"{'Total rows:':<35} {total_rows}")
    print_plain(f"{'Total columns:':<35} {total_columns}")
    print_plain(f"{'Rows with at least one null value:':<35} {df.isnull().any(axis=1).sum()}")
    print_plain('-' * 100)
    

def show_df_columns(df: pd.DataFrame) -> None:
    
    print_plain('Column breakdown:')
    col_width = max(len(col) for col in df.columns) + 2
    header = f"{'Column':<{col_width}} {'Total Values':>13} {'Null Values':>12} {'Non-null Unique':>17} {'Most Frequent Value':>25}"
    print_plain(header)
    print_plain('-' * len(header))
    for column in df.columns:
        mode = df[column].mode(dropna=True)
        if mode.empty:
            mode = '<All values are null>'
        else:
            mode = mode[0]
        print_plain(f"{column:<{col_width}} {df[column].size:>13} {df[column].isnull().sum():>12} {df[column].nunique():>17} {mode:>25}")
    print_plain('-' * len(header))