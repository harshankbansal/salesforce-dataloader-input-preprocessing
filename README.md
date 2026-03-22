# Salesforce Dataloader Input Preprocessing CLI

`dataloader-prep` is an interactive command-line utility for preparing CSV files before Salesforce dataloader imports. It loads your input file into a pandas dataframe, lets you run preprocessing steps interactively, and writes generated files to a timestamped output directory.

## What It Does

This utility is helpful when you need to:

- inspect an incoming CSV or XLSX before upload
- save normalized output as UTF-8 CSV
- add a lookup-derived column from a secondary file
- separate rows with null values for cleanup
- split a large file into smaller CSV files for loading

## Prerequisites

You need the following installed on your machine:

- `Python 3.10+`
- `pipx`

Check whether they are already available:

```bash
python --version
pipx --version
```

**NOTE:** If your system does not have these installed, refer to the [Prepare your system](#prepare-your-system) section at the end.

## Install This CLI With pipx

Install directly from GitHub:

```bash
pipx install "git+https://github.com/harshankbansal/salesforce-dataloader-input-preprocessing.git"
```

You can verify the installation with:

```bash
pipx list
```

You can also confirm the command is wired correctly by running it without arguments:

```bash
dataloader-prep
```

## Usage

Run the CLI with a CSV or XLSX file:

```bash
dataloader-prep /path/to/input-file.csv
```

Examples:

```bash
dataloader-prep ./data/accounts.csv
dataloader-prep ./data/contacts.xlsx
```

### Interactive Workflow

When the tool starts, it:

1. validates that the input file exists and is not empty
2. asks for an output directory suffix
3. creates an output folder under `dataloader-prep-output/`
4. loads the file into memory
5. shows a summary of the dataset
6. lets you keep applying operations until you exit

For CSV files, the tool also:

- detects file encoding
- lets you confirm or override the detected encoding
- optionally shows the first few lines
- lets you keep the default CSV parsing settings or override separator, quote character, quoting mode, and double-quote handling

If malformed CSV lines are encountered while loading, they are appended to:

```text
dataloader-prep-output/<your-run-folder>/lines_unable_to_load.csv
```

## Supported Operations

### Save as CSV

Saves the current in-memory dataframe to a CSV file in the current run's output directory.

### Show Summary

Displays summary of data, like number of rows, columns and separate summary for each column

### Add Lookup Column

Adds a new column by matching values from a lookup source file.

How it works:

1. you enter the new column name
2. you choose the key column from the current dataset
3. you choose a source file from the `lookup/` directory
4. you choose the lookup key column and value column from the source file
5. the tool maps values and reports unmatched keys

Generated outputs:

- a results CSV with the updated dataset
- an unmatched-keys CSV when lookup values are missing

### Separate Null Values

Saves rows with null values to a separate CSV file.

You can choose:

- rows where any column has a null value
- rows where selected columns have null values

After saving the null rows, you can continue with either:

- the original dataset
- only the remaining non-null rows

### Split CSV Files and Exit

Splits the current dataframe into multiple CSV files based on the number of records per file, saves them to the output directory, and then exits the CLI.

### Exit

Ends the interactive session without further processing.

## Lookup Files

For the `Add Lookup Column` operation, place lookup source files in a `lookup` directory relative to where you run the command.

Example:

```text
project-folder/
├── lookup/
│   ├── users.csv
│   └── accounts.xlsx
└── input.csv
```

## Output Location

Each run creates a folder like:

```text
dataloader-prep-output/<suffix>_<MMDD_HHMMSS>/
```

Generated CSV files from each step are saved there.

## Upgrade

```bash
pipx upgrade dataloader-prep
```

## Reinstall

If the command needs to be refreshed:

```bash
pipx reinstall dataloader-prep
```

## Uninstall

```bash
pipx uninstall dataloader-prep
```

## Prepare your system

### Install Python (Skip if already installed)

#### Windows

1. Download Python 3.10 or later from [python.org](https://www.python.org/downloads/windows/).
2. Run the installer.
3. Make sure you enable `Add python.exe to PATH`.
4. Verify the install:

#### macOS

Install Python using the official installer or Homebrew:

```bash
brew install python
python3 --version
```

#### Linux

Use your distribution package manager. Example for Ubuntu or Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Install pipx (Skip if already installed)

#### Windows

Install `pipx` using Python:

```bash
py -m pip install --user pipx
py -m pipx ensurepath
```

Close and reopen your terminal, then verify:

```bash
pipx --version
```

#### macOS and Linux

Install `pipx` with Python:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your terminal, then verify:

```bash
pipx --version
```
