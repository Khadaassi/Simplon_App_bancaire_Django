from sqlmodel import SQLModel, Session, create_engine, select
import sqlite3
import os
import pandas as pd

from dotenv import load_dotenv

# 📌 Charger les variables d'environnemen

load_dotenv()

# 📌 Définir la connexion SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
cursor=sqlite_conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# 📌 Connexion à Azure SQL
server = os.getenv("AZURE_SERVER")
database = os.getenv("AZURE_DATABASE")
username = os.getenv("AZURE_USERNAME")
password = os.getenv("AZURE_PASSWORD")


azure_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server"
azure_engine = create_engine(azure_url)


# 📌 Migrer les données
for table in tables:
    table_name = table[0]
    
    # Charger les données avec Pandas
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)
    
    # Insérer dans Azure SQL
    with Session(azure_engine) as session:
        df.to_sql(table_name, azure_engine, if_exists="replace", index=False)
        session.commit()

print("Migration terminée avec SQLModel !")