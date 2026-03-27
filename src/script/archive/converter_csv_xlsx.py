# This script convert .csv file from repo to .xlsx

import pandas as pd
import json

# rename this variable to save the file according to the invoice month
month = "2023-99"

# Read the CSV file with the specified delimiter
df = pd.read_csv('invoice.csv', delimiter=',')

# Exclude rows with "Inclusao de Pagamento" in the "Descrição" column
df = df[df['Descrição'] != 'Inclusao de Pagamento    ']

# Load the description mapping from the JSON file
with open('/home/ricardo/code/statistic/src/description.json') as f:
    description_list = json.load(f)

# Convert the list of dictionaries to a dictionary
description_mapping = {item['original']: item['new']
                       for item in description_list}

# Create a new column "Mapped_Categoria" based on the mapping
df['Mapped_Categoria'] = df['Descrição'].map(description_mapping)

# Use the original "Categoria" if there is no mapping, otherwise use the mapped value
df['Categoria'] = df['Mapped_Categoria'].combine_first(df['Categoria'])

# Drop the temporary "Mapped_Categoria" column
df = df.drop(columns=['Mapped_Categoria'])

# Group by "Categoria" and calculate the sum of "Valor (em R$)"
category_sum = df.groupby('Categoria')['Valor (em R$)'].sum().reset_index()

# Save both DataFrames to a single sheet in a new Excel file, with the summary table on the right of the original data
with pd.ExcelWriter(f'/home/ricardo/code/statistic/src/credit_card/xlsx/{month}.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False, startrow=0, startcol=0)
    category_sum.to_excel(writer, sheet_name='Data', index=False,
                          startrow=0, startcol=df.shape[1] + 1, header=True)

print(f'Conversion complete, Data and Summary saved in {month}.xlsx.')
