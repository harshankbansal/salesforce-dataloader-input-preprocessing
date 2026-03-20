import math
from pathlib import Path
import pandas as pd
import operations.save_as_csv as save_as_csv
import utils.cli_input_utils as cli_input


def apply(df: pd.DataFrame, output_dir: Path, step_count: int) -> None:

    total_rows = len(df)

    records_per_file = cli_input.ask_int(
        f"Enter number of records per split file. Total rows: {total_rows}",
        min_value=1,
    )
    total_files = math.ceil(total_rows / records_per_file)

    print(f"Splitting {total_rows} rows into {total_files} file(s)")

    for part_index in range(total_files):
        start_index = part_index * records_per_file
        end_index = start_index + records_per_file
        chunk_df = df.iloc[start_index:end_index]
        file_name = f"step_{step_count}_split_part_{part_index + 1}_of_{total_files}.csv"
        save_as_csv.apply(
            chunk_df,
            output_dir,
            step_count,
            file_name=file_name,
        )

    print(f"Split complete. Files saved to: {output_dir}")