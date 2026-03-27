import json
from datetime import datetime

# Função para calcular estatísticas de soma e média
def calculate_statistics(transactions):
    total_sum = sum(transaction["Valor (em R$)"] for transaction in transactions)
    total_count = len(transactions)
    if total_count > 0:
        average = total_sum / total_count
    else:
        average = 0
    return total_sum, average

# Lê o arquivo JSON
with open('/home/ricardo/code/statistic/src/credit_card/json/2023-09.json', 'r') as json_file:
    data = json.load(json_file)

# Cria um dicionário para armazenar transações por mês
data_by_month = {}

for transaction in data:
    date_str = transaction["Data de Compra"]
    date = datetime.strptime(date_str, "%d/%m/%Y")
    month = date.strftime("%Y-%m")
    
    if month not in data_by_month:
        data_by_month[month] = []
    
    data_by_month[month].append(transaction)

# Calcula e imprime as estatísticas para cada mês
for month, transactions in data_by_month.items():
    total_sum, average = calculate_statistics(transactions)
    print(f"Month: {month}")
    print(f"Total Sum: {total_sum}")
    print(f"Average: {average}\n")
