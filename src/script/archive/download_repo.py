# This script search for a file .csv on downloads/invoice folder and brin to the repo renaming to invoice.csv

import os
import shutil
import pandas as pd
import json

source_directory = "/home/ricardo/Downloads/invoice"

# Rename it as needed
file_name = "invoice"

target_extension = ".csv"

destination_directory = "/home/ricardo/code/statistic/src"

destination_file_path = None  # Initialize the variable outside the loop

for root, dirs, files in os.walk(source_directory):
    for file in files:
        if file.endswith(target_extension):
            source_file_path = os.path.join(root, file)
            destination_file_name = f'{file_name}{target_extension}'
            destination_file_path = os.path.join(
                destination_directory, destination_file_name)
            shutil.move(source_file_path, destination_file_path)
            break

if destination_file_path:
    df = pd.read_csv(destination_file_path, delimiter=';')

    data = df.to_dict(orient='records')
