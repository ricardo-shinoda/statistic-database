# This script convert .csv file from repo to .json

import pandas as pd
import json

# rename this variable to save the file according to the invoice month
month = "2023-09"

df = pd.read_csv('invoice.csv', delimiter=';')

data = df.to_dict(orient='records')

with open(f'/home/ricardo/code/statistic/src/credit_card/json/{month}.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Conversion complete. Data saved on 'output.json'.")
