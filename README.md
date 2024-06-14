Find Duplicate Files with Python
This Python script helps you locate duplicate files within a directory and its subdirectories. It calculates file hashes (MD5 by default) to identify duplicates efficiently and generates a CSV report summarizing the findings.

Features:

Efficient duplicate detection using file hashing.
Human-readable file size representation (KB, MB, GB).
Detailed CSV report including file path, name, size, creation, and modification dates.
Requirements:

Python 3.x
tqdm library (for progress bar, install using pip install tqdm)
Usage:

Clone or download this repository.
Install the required library: pip install tqdm
Run the script: python find_duplicates.py (This will scan the current directory by default)
Output:

The script will generate a CSV file named duplicates_report.csv in the same directory, containing information about the identified duplicate files.

Advanced Usage:

You can modify the script to specify a different directory for scanning by changing the directory_to_scan variable in the main function.
