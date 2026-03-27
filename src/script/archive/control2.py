import pandas as pd
import json
import openpyxl

# Define file paths
csv_file_path = "/home/ricardo/Downloads/invoice/invoice.csv"  # Path to the CSV file
month = "20240708ultimo"  # You can update this dynamically as needed

json_file_path = f"/home/ricardo/code/statistic/src/credit_card/json/{month}.json"
xlsx_file_path = f"/home/ricardo/code/statistic/src/credit_card/xlsx/{month}.xlsx"

# Read the CSV file with the specified delimiter
df = pd.read_csv(csv_file_path, delimiter=';')

# Exclude rows with "Inclusao de Pagamento" in the "Descrição" column
df = df[df['Descrição'] != 'Inclusao de Pagamento    ']

# Load the description mapping from the JSON file
with open('/home/ricardo/code/statistic/src/description.json') as f:
    description_list = json.load(f)

# Convert the list of dictionaries to a dictionary for mapping
description_mapping = {item['original']: item['new']
                       for item in description_list}

# Apply the mapping and fill in categories
df['Mapped_Categoria'] = df['Descrição'].map(description_mapping)
df['Categoria'] = df['Mapped_Categoria'].combine_first(df['Categoria'])
df = df.drop(columns=['Mapped_Categoria'])
df.columns = df.columns.str.strip()

# Save the data to Excel
with pd.ExcelWriter(xlsx_file_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)

# Save the data to JSON
df.to_json(json_file_path, orient='records', indent=4, force_ascii=False)

print(f"CSV converted and saved as JSON and Excel in the credit_card path.")
