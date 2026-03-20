import pandas as pd
from pathlib import Path
import operations.save_as_csv as save_as_csv
import utils.cli_input_utils as cli_input
from utils.cli_output_utils import print_plain, print_good, print_bad, print_warning

OPTION_ANY_COLUMN_HAS_NULL = "Save rows where any column has a null value in a separate file"
OPTION_USER_SELECTED_COLUMNS_HAS_NULL = "Save rows where null exists in selected columns only in a separate file"

def apply(df: pd.DataFrame, output_dir: Path, step_count: int) -> pd.DataFrame:
    print_plain("Separate Null Values:")
    option = cli_input.ask_option(
        "Select null separation option",
        [
            OPTION_ANY_COLUMN_HAS_NULL,
            OPTION_USER_SELECTED_COLUMNS_HAS_NULL,
        ],
    )

    if option == OPTION_ANY_COLUMN_HAS_NULL:
        null_mask = df.isnull().any(axis=1)
        file_name = f"step_{step_count}_null_rows_any_column.csv"
    elif option == OPTION_USER_SELECTED_COLUMNS_HAS_NULL:
        columns_with_nulls = [column for column in df.columns if df[column].isnull().any()]
        selected_columns = cli_input.ask_multi_options(
            "Select columns to filter out null values from",
            columns_with_nulls,
        )
        null_mask = df[selected_columns].isnull().any(axis=1)
        file_name = f"step_{step_count}_null_rows_selected_columns.csv"
    else:
        print_warning("Invalid option. No changes applied.")
        return df

    null_rows_df = df[null_mask]
    output_path = save_as_csv.apply(
        null_rows_df,
        output_dir,
        step_count,
        file_name=file_name,
    )
    print_good(f"Saved {null_rows_df.shape[0]} rows with null values to: {output_path}")

    proceed_with_remaining = cli_input.ask_yes_no(
        "Proceed with remaining rows only? Enter 'no' to continue with original dataset including null rows",
        default=True,
    )

    if not proceed_with_remaining:
        print_plain("Continuing with original dataset.")
        return df

    index_to_drop = null_rows_df.index
    filtered_df = df.drop(index=index_to_drop)
    print_plain(f"Continuing with filtered dataset. Remaining rows: {filtered_df.shape[0]}")
    return filtered_df
