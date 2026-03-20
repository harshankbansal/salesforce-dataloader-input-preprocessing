import pandas as pd
from pathlib import Path    
import csv
import utils.cli_input_utils as cli_input

def apply(df: pd.DataFrame, output_dir: Path, step_count: int, file_name: str = None) -> Path:
    default_file_name = f"step_{step_count}_save_as_csv.csv"
    print(f"Saving DataFrame to UTF-8 CSV file: {output_dir}")

    if file_name is None:
        file_name = cli_input.ask_text(
            "Enter the name of the CSV file",
            default=default_file_name,
        )
        
    if file_name == '':
        file_name = default_file_name
    elif not file_name.lower().endswith(".csv"):
        file_name = file_name + '.csv'

    output_path = output_dir / file_name

    df.to_csv(
        output_path, 
        index=False,
        sep=',',
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        doublequote=True,
        encoding='utf-8',
    )

    print(f"Data saved to CSV file: {output_path}")
    return output_path