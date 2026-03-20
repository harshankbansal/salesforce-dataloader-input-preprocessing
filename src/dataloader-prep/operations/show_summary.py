import pandas as pd

def apply(df: pd.DataFrame) -> None:
    show_df_overview(df)
    show_df_columns(df)

def show_df_overview(df: pd.DataFrame) -> None:
    print('-' * 100)
    print('DataFrame Overview:')
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    print(f"{'Total rows:':<35} {total_rows}")
    print(f"{'Total columns:':<35} {total_columns}")
    print(f"{'Rows with at least one null value:':<35} {df.isnull().any(axis=1).sum()}")
    print('-' * 100)
    

def show_df_columns(df: pd.DataFrame) -> None:
    
    print('Column breakdown:')
    col_width = max(len(col) for col in df.columns) + 2
    header = f"{'Column':<{col_width}} {'Total Values':>15} {'Null Values':>15} {'Unique Values (non null)':>30} {'Most Frequent Value':>25}"
    print(header)
    print('-' * len(header))
    for column in df.columns:
        print(f"{column:<{col_width}} {df[column].size:>15} {df[column].isnull().sum():>15} {df[column].nunique():>30} {df[column].mode(dropna=True)[0]:>25}")
    print('-' * len(header))