import operations.load_file as load_file
import operations.save_as_csv as save_as_csv
import operations.show_summary as show_summary
import operations.handle_null_values as handle_null_values
import operations.split_csv as split_csv
import operations.add_lookup_column as add_lookup_column
import utils.cli_input_utils as cli_input
from pathlib import Path
import datetime
import os
import sys
from utils.cli_output_utils import print_plain, print_good, print_bad, print_warning, print_info

OPERATION_SAVE_AS_CSV = 'Save as CSV'
OPERATION_SHOW_SUMMARY = 'Show Summary'
OPERATION_SEPARATE_NULL_VALUES = 'Separate Null Values'
OPERATION_SPLIT_CSV_FILES_AND_EXIT = 'Split CSV files and Exit'
OPERATION_ADD_LOOKUP_COLUMN = 'Add Lookup Column'
OPERATION_EXIT = 'Exit'

def main():
    print_plain('Pre-processing data...')

    # Input File
    if len(sys.argv) < 2:
        print_bad("Usage: dataloader-prep <input_file>")
        exit(1)
    input_file_name = sys.argv[1]
    input_file = Path(input_file_name)
    if(not input_file.exists()):
        print_bad(f"File {input_file_name} does not exist")
        exit(1)

    file_size = input_file.stat().st_size
    if(file_size == 0):
        print_bad(f"File {input_file_name} is empty")
        exit(1)

    print_plain(f"File {input_file_name} size: {file_size/1024/1024} MB")

    # Set Ouput Directory
    EXECUTION_ID=datetime.datetime.now().strftime('%m%d_%H%M%S')
    # INSERT_YOUR_CODE
    # OUTPUT_FOLDER_PREFIX = cli_input.ask_text(
    #     "Enter output directory suffix for your reference (e.g. object name, Jira ticket, etc)",
    #     default="task",
    # )
    OUTPUT_FOLDER_PREFIX = "task"
    OUTPUT_DIR = Path('dataloader-prep-output') / f"{OUTPUT_FOLDER_PREFIX}_{EXECUTION_ID}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print_info(f"All the generated files will be saved in: {OUTPUT_DIR}")

    df = load_file.apply(input_file_name, OUTPUT_DIR)
    show_summary.apply(df)

    available_operations = [
        OPERATION_SAVE_AS_CSV,
        OPERATION_SHOW_SUMMARY,
        OPERATION_ADD_LOOKUP_COLUMN,
        OPERATION_SEPARATE_NULL_VALUES,
        OPERATION_SPLIT_CSV_FILES_AND_EXIT,
        OPERATION_EXIT,
    ]
    # Operations Loop
    step_count = 0
    while True:
        try:
            print("\n")
            print('-' * 100)
            step_count += 1

            operation = cli_input.ask_option(
                "Select operation",
                available_operations,
            )
            print(f"Selected operation: {operation}")
            if operation == OPERATION_EXIT:
                break
            elif operation == OPERATION_SAVE_AS_CSV:
                save_as_csv.apply(df, OUTPUT_DIR, step_count)
            elif operation == OPERATION_SHOW_SUMMARY:
                show_summary.apply(df)
            elif operation == OPERATION_SEPARATE_NULL_VALUES:
                df = handle_null_values.apply(df, OUTPUT_DIR, step_count)
            elif operation == OPERATION_SPLIT_CSV_FILES_AND_EXIT:
                split_csv.apply(df, OUTPUT_DIR, step_count)
                break
            elif operation == OPERATION_ADD_LOOKUP_COLUMN:
                df = add_lookup_column.apply(df, OUTPUT_DIR, step_count)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            print("An error occurred. Returning to operation selection.", file=sys.stderr)
            continue

if __name__ == "__main__":
    main()