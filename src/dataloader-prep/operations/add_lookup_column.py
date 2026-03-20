from pathlib import Path
import pandas as pd
import operations.load_file as load_file
import operations.save_as_csv as save_as_csv
import utils.cli_input_utils as cli_input
from utils.cli_output_utils import print_plain, print_good, print_bad, print_warning

LOOKUP_DIR = Path("lookup")

def apply(df: pd.DataFrame, output_dir: Path, step_count: int) -> pd.DataFrame:
    print_plain("Add Lookup Column:")
    new_column_name = cli_input.ask_text("Enter name for the new column")
    if not new_column_name:
        print_warning("Column name cannot be empty. No changes applied.")
        return df

    if new_column_name in df.columns:
        replace_existing = cli_input.ask_yes_no(
            f"Column '{new_column_name}' already exists. Replace it?",
            default=False,
        )
        if not replace_existing:
            print_warning("No changes applied.")
            return df

    target_key_column = _read_column_name(
        df.columns,
        "Select the column from current dataset used for lookup key: ",
    )

    source_file = _select_lookup_file()
    if source_file is None:
        return df

    source_df = load_file.apply(str(source_file), output_dir)
    if source_df.empty:
        print_warning("Lookup source file is empty. No changes applied.")
        return df

    source_key_column = _read_column_name(
        source_df.columns,
        "Select lookup key column from source: ",
    )
    source_value_column = _read_column_name(
        source_df.columns,
        "Select lookup value column from source: ",
    )

    lookup_series = (
        source_df[[source_key_column, source_value_column]]
        .drop_duplicates(subset=[source_key_column], keep="first")
        .set_index(source_key_column)[source_value_column]
    )

    df[new_column_name] = df[target_key_column].map(lookup_series)
    print_good(f"Lookup column '{new_column_name}' added to dataset")
    null_count = df[new_column_name].isnull().sum()
    total_count = df[new_column_name].size
    print_warning(
        f"** Null values in '{new_column_name}': {null_count} out of {total_count} rows"
    )

    save_as_csv.apply(
        df,
        output_dir,
        step_count,
        file_name=f"step_{step_count}_add_lookup_column_{new_column_name}.csv",
    )
    return df


def _read_column_name(columns: pd.Index, prompt: str) -> str:
    return cli_input.ask_option(prompt, list(columns))


def _select_lookup_file() -> Path | None:
    if not LOOKUP_DIR.exists() or not LOOKUP_DIR.is_dir():
        print_bad(
            f"Lookup directory '{LOOKUP_DIR}' does not exist. "
            "Create it and add lookup files."
        )
        return None

    lookup_files = sorted(
        [
            file.name for file in LOOKUP_DIR.iterdir() if file.is_file()
        ],
    )

    if not lookup_files:
        print_bad(
            f"No lookup files found in '{LOOKUP_DIR}'. "
            "Add .csv or .xlsx files and try again."
        )
        return None

    selected_file_name = cli_input.ask_option(
        "Select lookup source file from lookup folder",
        lookup_files,
    )
    return LOOKUP_DIR / selected_file_name
