# Merge Export File Script

This script is designed to merge CSV files from a Datasaur exported ZIP file and output a new ZIP file containing the merged CSVs.

## Prerequisites

- Python 3.x
- Ensure you have the necessary permissions to read/write files in the directories you are working with.

## Installation

- Clone the repository or download the script to your local machine.
-Ensure Python is installed on your system. You can download it from python.org.

## Usage

To run the script, use the following command in your terminal or command prompt:

```bash
python merge.py -I <input_file_path> -O <output_file_path>
```

### Arguments

-I, --input: Required. The path to the input Datasaur exported ZIP file.
-O, --output: Required. The path where the output ZIP file will be saved.

### Example

```bash
python merge.py -I /path/to/input.zip -O /path/to/output.zip
```

This command will:

- Validate the input ZIP file to ensure it exists and is a valid ZIP file.
- Extract the contents of the input ZIP file to a temporary directory.
- Merge all CSV files found in each folder within the extracted contents.
- Create a new ZIP file containing the merged CSV files at the specified output path.
- Clean up the temporary directory used during the process.

## Notes

- Ensure the input file is a valid ZIP file containing CSV files to be merged.
- The output file path should not already exist, as the script will not overwrite existing files.
- The script will create a temporary directory named tmp in the current working directory. Ensure you have write permissions in this directory.

## Troubleshooting

- If you encounter a `FileNotFoundError`, ensure the input file path is correct.
- If you encounter a `FileExistsError`, ensure the output file path does not already exist.
- For any other issues, ensure you have the necessary permissions and that your Python environment is correctly set up.
