import psycopg2
import os
# from dotenv import load_dotenv

import random
from faker import Faker  # serve para criar dados fictícios


def create_tables(cursor, tables_scripts: dict) -> int:
    """ Cria as tabelas Customers, Products e Orders no Banco de Dados indicado pelo cursor. 
    ------
    PARAMS
        cursor: cursor do banco de dados
        tables_scripts: dicionário de scripts SQL para criar as tabelas
    ------
    RETURN
        int: 0 para sucesso, 1 para falha
    """
    for table_script in tables_scripts:
        try:
            cursor.execute(table_script)
        except psycopg2.Error as e:
            print('Erro ao criar a tabela:', e)
            return 1

    # Mensagem de conclusão
    print("Tabelas criadas com sucesso no Banco de Dados!")

    return 0


def get_tables_scripts():
    """ Retorna um dicionário de scripts SQL para criar as tabelas Customers, Products e Orders. 
    RETURN
        dict: dicionário de scripts SQL
    """
    
    sql_scripts = {
        'Customers': """
        CREATE TABLE IF NOT EXISTS Customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
        """,
        'Products': """
        CREATE TABLE IF NOT EXISTS Products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
        """,
        'Orders': """
        CREATE TABELE IF NOT EXISTS Orders (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES Customers(id),
            product_id INTEGER REFERENCES Products(id),
            quantity INTEGER NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) NOT NULL
        )
        """
    }
    return sql_scripts


cursor = None
tables_scripts = get_tables_scripts()
create_tables(cursor, tables_scripts)