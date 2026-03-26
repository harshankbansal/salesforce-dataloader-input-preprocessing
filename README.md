# Salesforce Dataloader Input Preprocessing CLI

`dataloader-prep` is an interactive command-line utility for preparing CSV and Excel files before Salesforce dataloader imports. It loads your input file into a dataframe, lets you run preprocessing steps interactively, and writes generated files to an output directory for the current run.

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

The tool validates the input file, loads the selected data, shows a summary, and then lets you apply operations interactively until you exit. Generated files are saved under `_dataloader-prep-output/`.

### Excel Files

Excel input is supported.

- If Microsoft Excel is available on the machine, the CLI can use it for better workbook compatibility.
- If Excel is not available, the tool falls back to Python-based reading.
- For complex workbooks with formulas or formatting-dependent values, using a machine with Excel installed usually gives the best results.

## Supported Operations

- `Save as CSV`: save the current dataset as CSV
- `Show Summary`: review high-level dataset and column information
- `Add Lookup Column`: enrich the current dataset using a lookup file
- `Separate Null Values`: isolate rows with null values for cleanup
- `Split CSV Files and Exit`: split the current dataset into smaller CSV files
- `Exit`: end the session

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

Each run creates a new folder under `_dataloader-prep-output/`, and generated files from that run are saved there.

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

