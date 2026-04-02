# To start working:
### 1. source vevn/bin/activate -- to activate venv
### 2. docker start statistic -- to start docker
### 3. Connect to the DB SQLTool -- to connect to the DB
### 4. If need to monthly add data, month ending run: control7.py
### 5. If need to delete all the data in the DB and run again: maintenance.py


Aqui está como você deve usar cada um daqui para frente:

1. Quando usar o maintenance.py (O "Botão de Pânico/Reset")
Use este script sempre que o objetivo for limpar o passado e reescrever a história.

Alteração de Categorias: Se você mudou o seu description.json e quer que as compras de 2022 e 2023 reflitam essas novas categorias.

Correção de Bug: Se você descobriu um erro na lógica de cálculo e precisa que ele seja aplicado a todos os 60 meses de uma vez.

Limpeza de IDs: Se o banco começar a ficar com "buracos" nos IDs ou se você quiser garantir que o Data Lake e o Banco estão 100% idênticos.

2. Quando usar o control7.py (O "Operacional")
Use este script para o fluxo incremental.

Fechamento do Mês: Você acabou de baixar o ZIP do mês atual (ex: Abril/2026). Basta rodar o control7 no modo current e ele vai processar apenas esse arquivo novo.

Venda ou Gasto Manual: Se você abriu o Controle.xlsx, adicionou uma linha de uma conta paga ou uma venda, basta rodar o control7. Como ele faz o Delete e Insert das tabelas manuais, ele vai atualizar o banco apenas com as novidades do Excel.

Arquivo Específico: Se você encontrou um Excel antigo perdido e quer subir apenas ele sem resetar o banco todo, use o mode="historical" com o target_file.

💡 Resumo da Estratégia
maintenance.py = Qualidade e Consistência. (Garante que o passado está perfeito).

control7.py = Agilidade e Atualização. (Garante que o presente está em dia).

Dica técnica: Como o seu control7.py é o "motor" que o maintenance.py usa, qualquer melhoria que você fizer na lógica de limpeza de texto ou conversão de moeda no control7 será herdada automaticamente pelo maintenance.

Você agora tem um Pipeline de Engenharia de Dados profissional, Ricardo. Parabéns pela persistência em resolver os erros de schema e de null violation! 🚀