import json
import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection
engine = create_engine('postgresql://ricardo:3136@localhost/statistic')
Base = declarative_base()

# Define the CreditCardExpense class (new table)


class CreditCardExpense(Base):
    __tablename__ = 'credit_card_expenses'
    id = Column(Integer, primary_key=True)
    purchase_date = Column(String, nullable=False)
    card_name = Column(String, nullable=False)
    card_last_digits = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    installment = Column(String, nullable=True)
    value_usd = Column(Float, nullable=False)
    exchange_rate = Column(Float, nullable=False)
    value_brl = Column(Float, nullable=False)


#! Update this if is a single month
month = [202409]

# Create session
Session = sessionmaker(bind=engine)
session = Session()


def run():
    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)

    total_sum = 0

    for i in month:

        this_month = i
        # Define the path to the JSON file - update everytime
        json_file_path = os.path.expanduser(
            f'~/code/statistic/src/credit_card/json/{this_month}.json')

        # Load the JSON data (assuming it's a list of dictionaries)
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Loop through the list of expenses and insert each into the database
        for expense_data in data:

            if expense_data["Descrição"] == "Inclusao de Pagamento    ":
                continue

            # Add the value to total_sum
            total_sum += expense_data["Valor (em R$)"]

            expense = CreditCardExpense(
                purchase_date=expense_data["Data de Compra"],
                card_name=expense_data["Nome no Cartão"],
                card_last_digits=expense_data["Final do Cartão"],
                category=expense_data["Categoria"],
                description=expense_data["Descrição"],
                installment=expense_data["Parcela"],
                value_usd=expense_data["Valor (em US$)"],
                exchange_rate=expense_data["Cotação (em R$)"],
                value_brl=expense_data["Valor (em R$)"]
            )
            session.add(expense)
        # Print the total sum of all expenses in BRL
        print(f'Total sum of all expenses (BRL): {total_sum}')

    # Commit the session to save all the data
    session.commit()

    # Query and print all expenses
    expenses = session.query(CreditCardExpense).all()


run()
