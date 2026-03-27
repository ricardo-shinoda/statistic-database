from decouple import config
import PyPDF2
import json
import re
import pandas as pd
import os
import shutil

pdf_password = config('PDF_PASSWORD')

source_directory = "/home/ricardo/Downloads/invoice"

month = "2023-10"

target_extension = ".pdf"

destination_directory = "/home/ricardo/code/statistic/src"

for root, dirs, files in os.walk(source_directory):
    for file in files:
        if file.endswith(target_extension):
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_directory, file)
            shutil.move(source_file_path, destination_file_path)
            break

pdf_file = open(destination_file_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
pdf_reader.decrypt(pdf_password)

movements = []
date_pattern = r"^\d{2}/\d{2}/\d{4}"  # Matches lines starting with a date

for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text = page.extract_text()
    lines = text.split('\n')

    current_transaction = None

    for line in lines:
        if re.search(date_pattern, line):
            if current_transaction:
                if "SALDO" not in current_transaction["Transaction"]:
                    movements.append(current_transaction)

            parts = line.strip().split()
            current_date = parts[0]
            description = " ".join(parts[1:-2])
            montante = parts[-2]
            natureza = parts[-1]
            current_transaction = {
                "Date": current_date,
                "Transaction": description,
                "Montante": montante,
                "Natureza": natureza,
            }
        else:
            if current_transaction:
                current_transaction["Transaction"] += "\n" + line.strip()

    if current_transaction:
        if "SALDO" not in current_transaction["Transaction"] and "TOTAL" not in current_transaction["Transaction"]:
            movements.append(current_transaction)

pdf_file.close()

df = pd.DataFrame(movements)

df.to_excel(f'/home/ricardo/code/statistic/src/account_mvt/xlsx/{month}.xlsx', index=False)

data_as_list = df.to_dict(orient='records')

# Define an outer dictionary
data_to_save = {
    "Date": month,
    "Transaction": "Your Main Transaction Description",
    "Montante": "Total Montante",
    "Natureza": "Total Natureza",
    "Transactions": data_as_list  # Add the list of transactions here
}

# Save the structured data to a JSON file
json_file_path = f'/home/ricardo/code/statistic/src/account_mvt/json/{month}.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_to_save, json_file, indent=4, ensure_ascii=False)


print(f'Data saved to {month}.xlsx')
