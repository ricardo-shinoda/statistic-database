import mysql.connector
import os
from decouple import config

# Retrieve MySQL credentials from environment variables
db_config = {
    "host": config('MYSQL_HOST'),
    "user": config('MYSQL_USER'),
    # Set a default value or leave it empty
    "password": config('MYSQL_PASSWORD'),
    "database": config('MYSQL_DATABASE')
}

# Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Create a table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS invoice_data (
    Column1 VARCHAR(255),
    Column2 VARCHAR(255),
    Column3 VARCHAR(255),
    Column4 VARCHAR(255),
    Column5 VARCHAR(255),
    Column6 VARCHAR(255),
    Column7 VARCHAR(255),
    Column8 VARCHAR(255),
    Column9 VARCHAR(255),
    Column10 VARCHAR(255)
)
"""
cursor.execute(create_table_query)

# Insert data into the MySQL table
insert_query = "INSERT INTO invoice_data (Column1, Column2, ...) VALUES (%s, %s, ...)"
data_to_insert = [(row['Column1'], row['Column2'], ...)
                  for _, row in df.iterrows()]
cursor.executemany(insert_query, data_to_insert)


print("Connecting to host:", db_config['host'])
print("Using database:", db_config['database'])


# Commit the changes and close the connection
connection.commit()
connection.close()
