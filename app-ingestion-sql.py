import psycopg2
import os
from dotenv import load_dotenv

import random
from faker import Faker  # serve para criar dados fictícios


def create_tables(cursor, tables_scripts: dict) -> int:
    """ Cria tabelas de um dicionário de scripts SQL no Banco de Dados.
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


def get_create_tables_scripts() -> dict:
    """ Retorna um dicionário de scripts SQL para criar as tabelas Customers, Products e Orders.
    RETURN
        dict: dicionário de scripts SQL
    """

    customers_sql = """
        CREATE TABLE IF NOT EXISTS Customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
        """

    products_sql = """
        CREATE TABLE IF NOT EXISTS Products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
        """

    orders_sql = """
        CREATE TABLE IF NOT EXISTS Orders (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES Customers(id),
            product_id INTEGER REFERENCES Products(id),
            quantity INTEGER NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) NOT NULL
        )
        """

    sql_scripts = {
        'Customers': customers_sql,
        'Products': products_sql,
        'Orders': orders_sql
    }
    return sql_scripts


def insert_random_data(cursor, conn, number_of_customers):
    """ Insere dados aleatórios nas tabelas Customers, Products e Orders.
    ------
    PARAMS
        cursor: cursor do banco de dados
        conn: conexão com o banco de dados
        number_of_customers: número de clientes a serem inseridos
    ------
    RETURN
        int: 0 para sucesso, 1 para falha
    """
    # Insere os clientes na tabela Customers
    try:
        customers_data = []

        for i in range(number_of_customers):
            name = fake.name()
            email = fake.email()

            # Adição do registro na tabela Customers
            cursor.execute(f'INSERT INTO Customers (name, email) VALUES ({name}, {email})')
            customers_data.append(name)

        # Persiste as alterações no BDR
        cursor.commit()
        print('Dados de clientes inseridos com sucesso!')
    except psycopg2.Error as e:
        print(f'Falha ao tentar gerar dados de usuários: {e}')

    # Insere os produtos na tabela Products
    try:
        products_name = ['Notebook Acer Aspire 5', 'Smartphone Samsung Galaxy S21', 'Smart TV LG 55 inches', 'Tablet Apple']
        products_category = ['Eletrônicos', 'Informática', 'Celulares', 'Tablets']

        for i in range(len(products_name)):
            name = products_name[i]
            category = products_category[i]
            price = round( random.uniform(50, 1000), 2 )

            # Adição do registro na tabela Products
            cursor.execute(f'INSERT INTO Products (name, category, price) VALUES ({name}, {category}, {price})')
        
        # Persiste as alterações no BDR
        cursor.commit()
        print('Dados de produtos inseridos com sucesso!')
    except psycopg2.Error as e:
        print(f'Falha ao tentar gerar dados de produtos: {e}')
    
    # Insere os pedidos na tabela Orders
    try:
        for i in range(len(products_name)):
            customer_id = random.randint(1, number_of_customers)
            product_id = random.randint(1, len(products_name))
            quantity = random.randint(1,5)
            # Extrai o preço do produto no banco de dados
            cursor.execute(f'SELECT price FROM Products WHERE id = {product_id}')
            price = cursor.fetchone()[0]  # recupera a próxima linha do resultado, como uma tupla
            price = price or 0
            total = round( price * quantity, 2 )
            status = random.choice(['Em andamento', 'Concluído', 'Cancelado'])

            # Adição do registro na tabela Orders
            cursor.execute('INSERT INTO Orders (customer_id, product_id, quantity, price, total, status) ' + 
                f'VALUES ({customer_id}, {product_id}, {quantity}, {price}, {total}, {status})')
        
        # Persiste as alteraçõe sno BDR
        cursor.commit()
        print('Dados de pedidos inseridos com sucesso!')
    except psycopg2.Error as e:
        print(f'Falaha ao tentar gerar dados de produtos: {e}')

    # Fecha a conexão com o Banco de Dados
    cursor.close()
    conn.close()


# ==== Código básico de instanciação ====
def main():
    # Instância do Faker com dialeto em português
    fake = Faker(locale='pt_BR')

    # Carregas as variáveis do ambiente do arquivo .env - torna o código multiplataforma
    load_dotenv()

    # Conectar o Banco de Dados PostgreSQL
    conn = psycopg2.connect(
        host = os.environ.get('DB_HOST'),
        database = os.envrion.get('DB_NAME'),
        user = os.environ.get('DB_USER'),
        password = os.environ.get('DB_PASSWORD'),
        port = os.environ.get('DB_PORT')
    )

    # Cria um cursor para executar as instruções
    cursor = conn.cursor()

    # Número de clientes
    number_of_customers = int( os.environ.get('NUM_CUSTOMERS') )

    # Executa as tarefas de manipulação do Banco de Dados
    tables_scripts = get_create_tables_scripts()
    create_tables(cursor, tables_scripts)
    insert_random_data(cursor, conn, number_of_customers)


# EXECUTION
if __name__ == '__main__':
    # Executa a função principal
    print('=' * 50)
    print('Iniciando o script...')

    main()
    
    print('=' * 50)
    print('Fim do script!\n')