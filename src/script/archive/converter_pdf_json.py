import re
from datetime import datetime
from decouple import config
import PyPDF2
import json

pdf_password = config('PDF_PASSWORD')

pdf_file = open('account_mvt.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
pdf_reader.decrypt(pdf_password)

movements = []

date_pattern = r"\d{2}/\d{2}/\d{4}"

for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text = page.extract_text()
    lines = text.split('\n')
    current_date = None
    movement = None

    for line in lines:
        if re.search(date_pattern, line):
            if movement:
                if movement.get("Date") and movement.get("Transaction"):
                    movements.append(movement)
            parts = line.strip().split()
            current_date = parts[0]
            description = " ".join(parts[1:-2])
            montante = parts[-2]
            natureza = parts[-1]
            if re.match(date_pattern, current_date):
                if "SALDO" in description:
                    movement = None  # Exclude transactions with "SALDO" in description
                elif not natureza.isalpha():
                    movement = None  # Exclude transactions where "Natureza" is not a letter
                else:
                    movement = {"Date": current_date, "Transaction": description, "Montante": montante, "Natureza": natureza, "Transactions": []}
        else:
            if movement is not None:
                if "SALDO" not in line:
                    movement["Transactions"].append({"Transaction": line.strip()})

if movement and movement.get("Date") and movement.get("Transaction"):
    movements.append(movement)

pdf_file.close()

data = {
    'text': '',
    'structure': [],
    'movements': movements
}

movements_data = {
    'movements': movements
}

data.update(movements_data)

# Filter out transactions with "SALDO" in their description and non-letter "Natureza"
filtered_movements = [m for m in movements if all("SALDO" not in t.get("Transaction", "") for t in m.get("Transactions", []))]

data["movements"] = filtered_movements

json_data = json.dumps(data, ensure_ascii=False, indent=4)

with open('output_account.json', 'w') as json_file:
    json_file.write(json_data)

print(json_data)
