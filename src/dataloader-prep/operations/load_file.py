import pandas as pd
from pathlib import Path
import csv
import utils.cli_input_utils as cli_input

def apply(file_path: str, output_dir: Path) -> pd.DataFrame:
    if(file_path.lower().endswith('.xlsx')):
        return load_xlsx(file_path, output_dir)
    elif(file_path.lower().endswith('.csv')):
        return load_csv(file_path, output_dir)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def load_xlsx(file_path: str, output_dir: Path) -> pd.DataFrame:
    file = pd.ExcelFile(file_path)
    sheets = file.sheet_names
    if(len(sheets) == 1):
        return file.parse(sheets[0])
    else:
        selected_sheet = cli_input.ask_option(
            "Please select a sheet",
            sheets,
        )
        return file.parse(selected_sheet)

def load_csv(file_path: str, output_dir: Path) -> pd.DataFrame:
    SEPARATOR = ','
    QUOTECHAR = '"'
    QUOTING = csv.QUOTE_ALL
    DOUBLEQUOTE = True
    ENCODING = 'utf-8'

    print('Reading CSV File...')
    show_head = cli_input.ask_yes_no("Show head", default=False)
    if show_head:
        _show_file_head(file_path, n_lines=3, encoding=ENCODING)

    # Show default values and ask if user wants to update
    keep_default_prompt = f"""
    The following are the default values for reading the CSV file:
    Separator: {SEPARATOR}
    Quotechar: {QUOTECHAR}
    Quoting: {QUOTING}
    Doublequote: {DOUBLEQUOTE}
    Encoding: {ENCODING}
    Do you want to keep these default values? (Y/n)
    """
    keep_default = cli_input.ask_yes_no(
        keep_default_prompt.strip(),
        default=True,
    )

    if not keep_default:
        SEPARATOR = cli_input.ask_text(
            "Please select the separator",
            default=SEPARATOR,
        )
        QUOTECHAR = cli_input.ask_text(
            "Please select the quotechar",
            default=QUOTECHAR,
        )
        quoting_str = cli_input.ask_text(
            "Please select the quoting",
            default=str(QUOTING),
        )
        try:
            QUOTING = int(quoting_str)
        except ValueError:
            print(f"Invalid quoting value '{quoting_str}'. Keeping default: {QUOTING}")

        doublequote_text = cli_input.ask_text(
            "Please select the doublequote (true/false)",
            default=str(DOUBLEQUOTE),
        )
        DOUBLEQUOTE = doublequote_text.strip().lower() in ("1", "true", "t", "yes", "y")
        ENCODING = cli_input.ask_text(
            "Please select the encoding",
            default=ENCODING,
        )

    CSV_FILE_PROPERTIES = {
        'sep': SEPARATOR,
        'quotechar': QUOTECHAR,
        'quoting': QUOTING,
        'doublequote': DOUBLEQUOTE,
    }

    return pd.read_csv(
        file_path,
        encoding=ENCODING,
        dtype=str,
        engine='python',
        # keep_default_na=False,
        on_bad_lines=lambda bad_line: _read_csv_save_bad_lines(bad_line, output_dir, ENCODING),
        **CSV_FILE_PROPERTIES
    )

def _read_csv_save_bad_lines(bad_line: list[str], output_dir: Path, encoding: str) -> None:
    print('Bad line Detected')
    with open(output_dir/'lines_unable_to_load.csv', 'a', encoding=encoding) as file:
        line = ','.join(bad_line)
        file.write(line + '\n')       

def _show_file_head(file_path: str, n_lines: int = 3, encoding: str = 'utf-8') -> None:
    with open(file_path, 'r', encoding=encoding) as file:
        for i, line in enumerate(file):
            if i >= n_lines:
                break
            print(line)