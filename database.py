# Database Management Banking

import os
import mysql.connector as sql
from dotenv import load_dotenv

load_dotenv()

mydb = sql.connect(
            host="localhost",
            user="root",
            passwd=os.getenv("DB_PASSWORD"),
            database="bank"
)

cursor = mydb.cursor()

def db_query(str):
    cursor.execute(str)
    result = cursor.fetchall()
    return result

def createcustomertable():
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers
                (username VARCHAR(20) NOT NULL,
                password VARCHAR(20) NOT NULL,
                name varchar(20) NOT NULL,
                age INTEGER NOT NULL,
                city VARCHAR(20) NOT NULL,
                balance INTEGER NOT NULL,
                account_number INTEGER NOT NULL,
                status BOOLEAN NOT NULL)
    ''')

mydb.commit()

if __name__ == "__main__":
    createcustomertable()