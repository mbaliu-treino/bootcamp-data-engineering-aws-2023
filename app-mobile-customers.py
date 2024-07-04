# app-mobile-customers.py
import json
import os
import time
import boto3  # STK AWS - biblioteca de manipulação da AWS usando código
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal

# Instância do Faker com dialeto em português
fake = Faker(locale='pt_BR')

# Carregas as variáveis do ambiente do arquivo .env - torna o código multiplataforma
load_dotenv()

# Número de venetos a serem criados
number_of_events = int( os.environ.get('NUM_EVENTS') )

# Define classe de codificação personalizada
# Validação para o json.dumps - faz a codificação personalizada do JSON para o formatação ideal
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomEncoder, self).default(obj)

# Configuração das credenciais da AWS a partir das variáveis de ambiente
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Configura as credenciais de acesso à conta da AWS
s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Define o nome do bucket S3
# 'raw_bootcamp_<id-conta>' por usar o id 
bucket_name = os.environ.get('BUCKET_RAW')

# SIMULAÇÂO DO AMBIENTE MOBILE
#   - Acesso de várias páginas
#   - Realização de uma compra
# Definição da lista de páginas do aplicativo
pages = [
    'home',
    'products',
    'cart',
    'checkout',
    'profile'
]

# Definição da lista de ações do usuário
actions = [
    'view_page',
    'click_link',
    'add_to_cart',
    'remove_from_cart',
    'checkout',
    'purchase'
]

# Gera eventos aleatórios do usuário
for i in range(number_of_events):
    # Define dados do usuário
    user_data = {
        'id': fake.random_int(min=1, max=100),
        'name': fake.name(),
        'email': fake.email(),
        'sex': fake.random_element(elements=('Male', 'Female')),
        'age': fake.random_int(min=18, max=65),
        'ip': fake.ipv4(),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'state': fake.state(),
        'longitude': fake.longitude(),
        'latitude': fake.latitude()
        }
    
    # Define dados do evento
    event_data = {
        # 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # int(time.time())
        'timestamp': int(time.time()),
        'page': fake.random_element(elements=pages),
        'action': fake.random_element(elements=actions),
        'product_id': fake.random_int(min=1, max=100),
        'quantity': fake.random_int(min=1, max=5),
        'stock_id': fake.random_int(min=1, max=100),
        'price': Decimal( str( round( fake.pyfloat(left_digits=2, right_digits=2, positive=True ), 2 ) ) ),
        'stock_id_number': fake.random_int(min=1, max=100)
    }

    # Combina dados do usuário e do evento em um único evento
    data = {
        'user': user_data,
        'event': event_data
    }

    # Persistência dos dados
    frt_date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    
    # Salva os dados em arquivo JSON localmente (opcional para analisar localmente)
    if not os.path.exists('./data'):
        os.makedirs('./data')
        print('Diretório de dados criado: ./data')
    if not os.path.exists('./data/raw'):
        os.makedirs('./data/raw')
        print('Diretório de dados criado: ./data/raw')

    with open(f'event_customers_mobile{i}_{frt_date}.json', 'w') as file:
        time.sleep(1)
        json.dump(data, file, cls=CustomEncoder)

    # Salva os dados em arquivo JSON no bucket S3 diretamente no Bucket
    time.sleep(3)
    (s3.Object(
        bucket_name=bucket_name, 
        key=f'event_customers_mobile{i}_{frt_date}.json')
    .put(
        Body=json.dumps(data, cls=CustomEncoder)
        ))
    
    print(f'Evento {i} criado com sucesso!')

print('=' * 50)
print('Fim do script!\n')