import zipfile
import shutil
import subprocess
import os
import glob
from decouple import config

# Path to the downloaded zip file
# Replace with the actual file path
zip_file_path = "/home/ricardo/Downloads/Fatura-CPF.zip"

# Password for the zip file
# zip_password = "218843" SEE if below will work
zip_password = config('ZIP_PASSWORD')

# Extract the contents of the zip file
# Replace with the desired extraction folder
extracted_folder = "/home/ricardo/Downloads/invoice"
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder, pwd=bytes(zip_password, 'utf-8'))

# Find the path of the CSV file inside the extracted folder
csv_files = glob.glob(os.path.join(extracted_folder, '*.csv'))

if csv_files:
    # Use the first CSV file found (you may want to implement specific logic if there are multiple CSV files)
    extracted_text_file = csv_files[0]

    # Path to the Text Editor app in Pop OS
    # Replace with the actual path to the Text Editor app
    text_editor_path = "/usr/bin/gedit"

    # Make a copy of the file before moving it to the desktop folder
    # This ensures that the original file is still available for further operations
    # copied_text_file = os.path.join(
    #     extracted_folder, 'copied_' + os.path.basename(extracted_text_file))
    # shutil.copy(extracted_text_file, copied_text_file)

    # # Open the text file with the Text Editor app
    # subprocess.run([text_editor_path, copied_text_file])

    # Move the copied text file to the desktop folder
    # Replace with the desired desktop folder
    # desktop_folder = "/home/ricardo/Desktop/test"
    # shutil.move(copied_text_file, desktop_folder)

    # Copy the original text file to the second folder
    # Replace with the desired second folder
    # second_folder = "/home/ricardo/Downloads/invoice"
    # shutil.copy(extracted_text_file, second_folder)

# Clean up: remove only the zip file
# Uncomment this part of the code if you want to delete the .zip file
# os.remove(zip_file_path)
