import argparse
import csv
import os
import shutil
import zipfile


def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def clean_tmp_dir(tmp_dir):
    shutil.rmtree(tmp_dir)


def validate_input_file(input_file_path):
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file {input_file_path} does not exist")

    if not input_file_path.endswith(".zip"):
        raise ValueError(f"Input file {input_file_path} is not a zip file")

    if not zipfile.is_zipfile(input_file_path):
        raise ValueError(f"Input file {input_file_path} is not a valid zip file")


def validate_output_file(output_file_path):
    if os.path.exists(output_file_path):
        raise FileExistsError(f"Output file {output_file_path} already exists")

    if not output_file_path.endswith(".zip"):
        raise ValueError(f"Output file {output_file_path} is not a zip file")


def read_csv_with_dict_reader(csv_file_path):
    with open(csv_file_path, "r") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def write_csv_with_dict_writer(csv_file_path, data):
    with open(csv_file_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def merge_csv_files(csv_files):
    data = []
    for csv_file in csv_files:
        data.extend(read_csv_with_dict_reader(csv_file))
    return data


def do_merge_csv_files_per_folder(folder_path):
    csv_files = [
        f"{folder_path}/{file}"
        for file in os.listdir(folder_path)
        if file.endswith(".csv")
    ]
    data = merge_csv_files(csv_files)
    write_csv_with_dict_writer(f"{folder_path}/all_merged.csv", data)


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, "w") as zipf:
        for root, _dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)


def extract_zip_file(zip_file_path, output_dir):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)


def write_zip_file(zip_file_path, file_path):
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        zipf.write(file_path, os.path.basename(file_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-I", "--input", required=True, help="Input Datasaur exported zip file path"
    )
    parser.add_argument("-O", "--output", required=True, help="Output zip file path")
    args = parser.parse_args()

    INPUT_ZIP_FILE = args.input
    OUTPUT_ZIP_FILE = args.output

    validate_input_file(INPUT_ZIP_FILE)
    validate_output_file(OUTPUT_ZIP_FILE)

    TMP_DIR = "tmp"
    create_dirs(TMP_DIR)

    extract_zip_file(INPUT_ZIP_FILE, TMP_DIR)

    BASE_EXTRACTED_PATH = "tmp/{name}".format(name=os.listdir("tmp")[0])

    folders = [
        f"{BASE_EXTRACTED_PATH}/{folder}"
        for folder in os.listdir(BASE_EXTRACTED_PATH)
        if os.path.isdir(os.path.join(BASE_EXTRACTED_PATH, folder))
    ]

    for folder in folders:
        do_merge_csv_files_per_folder(folder)

    zip_folder(BASE_EXTRACTED_PATH, OUTPUT_ZIP_FILE)

    clean_tmp_dir(TMP_DIR)
