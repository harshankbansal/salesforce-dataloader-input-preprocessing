import sys
import os
import pandas as pd
from pathlib import Path
import csv
import utils.cli_input_utils as cli_input
from utils.cli_output_utils import print_plain, print_good, print_bad, print_warning, print_info
from charset_normalizer import from_bytes
import xlwings as xw

def apply(file_path: str, output_dir: Path, step: int = 0) -> pd.DataFrame:
    if(file_path.lower().endswith('.xlsx')):
        return load_xlsx(file_path, output_dir, step)
    elif(file_path.lower().endswith('.csv')):
        return load_csv(file_path, output_dir, step)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def load_xlsx(file_path: str, output_dir: Path, step) -> pd.DataFrame:
    print_plain(f"Reading Excel File: {file_path}")
    file = pd.ExcelFile(file_path)
    sheets = file.sheet_names
    if(len(sheets) == 1):
        selected_sheet = sheets[0]
    else:
        selected_sheet = cli_input.ask_option(
            "Please select a sheet",
            sheets,
        )

    if is_excel_available():
        print_plain("Excel application is available. Converting to CSV an reading")
        return load_excel_with_xlwings(file_path, selected_sheet, output_dir, step)
        
    print_plain("Excel application is not available.")
    return load_xlsx_with_pandas(file_path, selected_sheet, output_dir, step)

def load_csv(file_path: str, output_dir: Path, step, encoding: str = None, show_head: bool = None) -> pd.DataFrame:
    SEPARATOR = ','
    QUOTECHAR = '"'
    QUOTING = csv.QUOTE_ALL
    DOUBLEQUOTE = True
    ENCODING = encoding

    if ENCODING is None:
        print_plain('Detecting encoding...')
        with open(file_path, 'rb') as f:
            bytes_to_read = min(10 * 1024 * 1024, os.path.getsize(file_path))
            bytes = f.read(bytes_to_read)
        result = from_bytes(bytes).best()
        if result is None:
            print_bad("Unable to automatically detect encoding. Please specify the encoding.")
            ENCODING = cli_input.ask_text(
                    f"Enter encoding to use to read the file"
            )
        else:
            print_info(f"Detected encoding: {result.encoding}. Encoding also known as: {result.encoding_aliases}.")
            print_warning("!!IMPORTANT!! DETECTED ENCODING MAY NOT BE CORRECT. PLEASE VERIFY THE ENCODING BEFORE USING IT.")
            ENCODING = cli_input.ask_text(
                    f"Enter encoding to use to read the file. Press enter to keep detected encoding or type the encoding you want to use",
                    default=result.encoding,
                )

    print_plain(f"Reading CSV File: {file_path}")

    # if show_head is None:
    #     show_head = cli_input.ask_yes_no("Show head?", default=False)
    # if show_head:
    #     _show_file_head(file_path, n_lines=3, encoding=ENCODING)

    # Show default values and ask if user wants to update
    # keep_default_prompt = f"""
    # The following are the default values for reading the CSV file:
    # Separator: {SEPARATOR}
    # Quotechar: {QUOTECHAR}
    # Quoting: {QUOTING}
    # Doublequote: {DOUBLEQUOTE}
    # Do you want to keep these default values?
    # """
    # keep_default = cli_input.ask_yes_no(
    #     keep_default_prompt.strip(),
    #     default=True,
    # )

    # if not keep_default:
    #     SEPARATOR = cli_input.ask_text(
    #         "Please select the separator",
    #         default=SEPARATOR,
    #     )
    #     QUOTECHAR = cli_input.ask_text(
    #         "Please select the quotechar",
    #         default=QUOTECHAR,
    #     )
    #     quoting_str = cli_input.ask_text(
    #         "Please select the quoting",
    #         default=str(QUOTING),
    #     )
    #     try:
    #         QUOTING = int(quoting_str)
    #     except ValueError:
    #         print(f"Invalid quoting value '{quoting_str}'. Keeping default: {QUOTING}")

    #     doublequote_text = cli_input.ask_yes_no(
    #         "Does CSV use double quotes for quotes within values?",
    #         default=str(DOUBLEQUOTE),
    #     )
    #     DOUBLEQUOTE = doublequote_text.strip().lower() in ("1", "true", "t", "yes", "y")
        
    CSV_FILE_PROPERTIES = {
        'sep': SEPARATOR,
        'quotechar': QUOTECHAR,
        'quoting': QUOTING,
        'doublequote': DOUBLEQUOTE,
    }

    df = pd.read_csv(
        file_path,
        encoding=ENCODING,
        dtype=str,
        engine='python',
        na_values=[''],
        # keep_default_na=False,
        on_bad_lines=lambda bad_line: _read_csv_save_bad_lines(bad_line, output_dir, ENCODING, step),
        **CSV_FILE_PROPERTIES
    )
    print_good(f"File loaded successfully. Total rows: {df.shape[0]}")
    return df

def _read_csv_save_bad_lines(bad_line: list[str], output_dir: Path, encoding: str, step: int) -> None:
    print_bad('Bad line Detected')
    with open(output_dir/f'step_{step}_lines_unable_to_load.csv', 'a', encoding=encoding) as file:
        line = ','.join(bad_line)
        file.write(line + '\n')       

def _show_file_head(file_path: str, n_lines: int = 3, encoding: str = 'utf-8') -> None:
    with open(file_path, 'r', encoding=encoding) as file:
        for i, line in enumerate(file):
            if i >= n_lines:
                break
            print(line, end='')

def load_xlsx_with_pandas(file_path: str, selected_sheet: str, output_dir: Path, step: int) -> pd.DataFrame:
    print_warning(
        "Since the excel app is not available, note that this tool deos not support all functionalities of the excel app."
        "Reading data may loose formating of fields like number / date / etc."
        "Cells with formulas may appear as #REF!, #VALUE! instead of calculated values.\n"
        "If your workbook has formulas: open it in Excel, wait for values to load, then Save.(Skip if already done) "
        "That updates formula cells with their calculated values. You can then use this CLI on the saved file."
        "The best way to avoid this is to save the file as a CSV file using the excel app."
    )
    if not cli_input.ask_yes_no("Would you like to proceed?", default=True):
        print_plain("Load cancelled.")
        sys.exit(0)

    print_plain(f"Reading Excel File: {file_path}")
    file = pd.ExcelFile(file_path)
    sheets = file.sheet_names
    if(len(sheets) == 1):
        selected_sheet = sheets[0]
    else:
        selected_sheet = cli_input.ask_option(
            "Please select a sheet",
            sheets,
        )
    df = pd.read_excel(file_path, sheet_name=selected_sheet, dtype=str)
    print_good(f"File loaded successfully. Total rows: {df.shape[0]}")
    return df


def load_excel_with_xlwings(file_path: str, selected_sheet: str, output_dir: Path, step: int) -> pd.DataFrame:
    print_plain(f"Reading Excel File using xlwings: {file_path}")

    app = xw.App(visible=False)
    csv_file_path = os.path.abspath(output_dir/f"step_{step}_excel_to_csv_{selected_sheet}.csv")
    print_plain(f"Saving Excel File to CSV: {csv_file_path}")
    wb = app.books.open(file_path)
    wb.sheets[selected_sheet].activate()
    #app.api.Calculate()
    df = None
    if sys.platform == "win32":
        wb.api.SaveAs(csv_file_path, FileFormat=62)
        df = load_csv(csv_file_path, output_dir, step, encoding='utf-8-sig', show_head=False)
    else:
        wb.save(csv_file_path)
        df = load_csv(csv_file_path, output_dir, step, encoding='utf-8', show_head=False)
    
    wb.close()
    app.quit()

    return df

def is_excel_available():
    try:
        app = xw.App(visible=False)
        app.quit()
        return True
    except Exception:
        return False