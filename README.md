# Bootcamp Data Engineering AWS 2023

Este projeto é uma solução de dados que visa integrar dados provenientes de duas fontes distintas (de um Banco de Dados Relacional - RDBMS e um de Data Lake) para disponibizá-los em um Data Warehouse de forma a permitir análises e insights consistentes. O desafio é a construção de um Data Pipeline utilizando a Cloud AWS.

## ARQUITETURA

### 1. DATA SOURCES (AWS RDB e AWS S3)

Para simular o contexto, primeiro foram criados fontes de dados (_data sources_). Uma delas é uma aplicação de geração de dados fictícios usando Python e ingeridos no Amazon RDS. Uma outra é a uma aplicação Python de geração de dados fictícios para criação de diversos arquivos JSON, os quais foram ingeridos em um Bucket do Amazon S3.

### 2. INGESTÃO NO DATA LAKE (AWS DMS)

### 3. PROCESSAMENTO E MANIPULAÇÃO NA CLOUD

### 4. SERVING

### 5. DATA WAREHOUSE


<!--
Tecnologias:

Python (para processamento e integração de dados)
Bibliotecas como Pandas e IPython para manipulação e visualização de dados.
SQL para interagir com o RDBMS.


Próximos Passos:

Conexão com as fontes de dados: Estabelecer conexões seguras com o RDBMS e o Data Lake.
Extração de dados: Extrair os dados relevantes de ambas as fontes.
Transformação de dados: Limpar, tratar e transformar os dados para garantir consistência e compatibilidade.
Carregamento de dados: Carregar os dados integrados em um destino final (banco de dados, arquivo, etc.).
-->
