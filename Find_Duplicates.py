import os
import hashlib
import csv
import time
from tqdm import tqdm

def calculate_file_hash(file_path, hash_algorithm='md5'):
    """
    Calculates the hash of a file using the specified hash algorithm.
    Args:
        file_path: The path to the file.
        hash_algorithm: The hash algorithm to use (default is 'md5').
    Returns:
        The calculated hash of the file.
    """
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def human_readable_size(size):
    """
    Converts a file size to a human-readable format (KB, MB, GB).
    Args:
        size: File size in bytes.
    Returns:
        Human-readable file size.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def get_file_dates(file_path):
    """
    Gets the creation and last modified dates of a file.
    Args:
        file_path: The path to the file.
    Returns:
        A tuple containing the creation and last modified dates.
    """
    created_date = time.ctime(os.path.getctime(file_path))
    modified_date = time.ctime(os.path.getmtime(file_path))
    return created_date, modified_date

def find_duplicates(directory):
    """
    Finds duplicate files in a directory and its subdirectories.
    Args:
        directory: The directory path to search for duplicates.
    Returns:
        A dictionary where the keys are file hashes and the values are lists of file information (path, name, size, created date, modified date).
    """
    file_hashes = {}
    duplicates = {}

    total_files = sum([len(files) for r, d, files in os.walk(directory)])
    with tqdm(total=total_files, desc="Scanning files", unit="file") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_hash = calculate_file_hash(file_path)
                    file_size = os.path.getsize(file_path)
                    created_date, modified_date = get_file_dates(file_path)

                    if file_hash in file_hashes:
                        if file_hash not in duplicates:
                            duplicates[file_hash] = [file_hashes[file_hash]]
                        duplicates[file_hash].append((file_path, file, file_size, created_date, modified_date))
                    else:
                        file_hashes[file_hash] = (file_path, file, file_size, created_date, modified_date)
                    pbar.update(1)

    return duplicates

def write_duplicates_to_csv(duplicates, output_file):
    """
    Writes duplicate file information to a CSV file.
    Args:
        duplicates: A dictionary of duplicate files.
        output_file: The path to the output CSV file.
    """
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Path', 'File Name', 'File Size', 'Created Date', 'Modified Date'])
        for files in duplicates.values():
            for file_info in files:
                file_path, file_name, file_size, created_date, modified_date = file_info
                writer.writerow([file_path, file_name, human_readable_size(file_size), created_date, modified_date])

def main():
    # Automatically detect the directory where the script is located
    directory_to_scan = os.path.dirname(os.path.realpath(__file__))
    output_file = os.path.join(directory_to_scan, 'duplicates_report.csv')

    duplicates = find_duplicates(directory_to_scan)
    write_duplicates_to_csv(duplicates, output_file)

    print(f"Duplicate file search completed. Report saved to {output_file}.")

if __name__ == "__main__":
    main()
