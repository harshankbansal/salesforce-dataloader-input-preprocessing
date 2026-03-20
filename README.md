# Salesforce Dataloader Input Preprocessing CLI

Interactive CLI utilities for preparing CSV/XLSX files before Salesforce dataloader operations.

## What This Tool Does

This CLI helps data engineers and developers clean and prepare files before loading into Salesforce.  
It loads a CSV/XLSX into a dataframe, lets you apply interactive preprocessing operations, and writes results to timestamped output folders.

## Supported Operations

The CLI currently supports:

1. **Save as CSV**
   - Saves the current in-memory dataframe to a CSV file in output folder.

2. **Show Summary**
   - Displays row/column count.
   - Shows null count, unique count, and most frequent value by column.

3. **Add Lookup Column**
   - Adds a new column to the current dataframe using a lookup source file.
   - Lookup files are picked from the `lookup/` folder.
   - You choose:
     - target key column in current dataset
     - key column in lookup file
     - value column in lookup file
   - The tool reports nulls in the newly created lookup column.

4. **Separate Null Values**
   - Saves rows with nulls to a separate file.
   - Supports:
     - rows where any column is null
     - rows where selected columns are null
   - You can continue with:
     - original dataset, or
     - filtered dataset (remaining rows only)

5. **Split CSV Files and Exit**
   - Splits current dataset into multiple CSV files by records-per-file.
   - Saves split files to output folder.
   - Exits after split operation.

## Install (Recommended: pipx)

Install directly from GitHub:

```bash
pipx install "git+https://github.com/harshankbansal/salesforce-dataloader-input-preprocessing.git"
```

After installation, run:

```bash
dataloader-prep /path/to/input/file
```

## Upgrade

```bash
pipx upgrade salesforce-dataloader-preprocess-cli
```

## Reinstall (if command is not refreshed after changes)

```bash
pipx reinstall salesforce-dataloader-preprocess-cli
```

## Uninstall

```bash
pipx uninstall salesforce-dataloader-preprocess-cli
```

## Notes

- Python 3.10+ is required.
- Lookup files should be placed in a `lookup` folder (relative to where you run the command) for the lookup-column operation.
- Output files are written to `output/<execution_id>/`.
