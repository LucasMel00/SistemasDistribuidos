
# API de Criptografia AES-256 com FastAPI

Este projeto é uma API simples para criptografar e descriptografar textos usando o algoritmo AES-256 em modo CBC com padding PKCS7. A aplicação foi desenvolvida utilizando [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://pydantic-docs.helpmanual.io/) e a biblioteca [cryptography](https://cryptography.io/en/latest/).

## Funcionalidades

- **Criptografia**: Envia um texto e uma chave (opcional) e recebe o texto criptografado, o vetor de inicialização (IV) e a chave em base64.
- **Descriptografia**: Envia o texto criptografado, a chave e o IV (todos em base64) e recebe o texto original.

## Pré-requisitos

- Python 3.8 ou superior
- [Pip](https://pip.pypa.io/en/stable/)

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

Instale as dependências:

bash
Copiar
pip install -r requirements.txt
Caso o arquivo requirements.txt não exista, você pode instalar as dependências manualmente:

bash
Copiar
pip install fastapi uvicorn cryptography
Executando a API
Para iniciar o servidor da API, execute o comando:

bash
Copiar
uvicorn main:app --host 0.0.0.0 --port 8000
Observação: O comando acima assume que o arquivo principal se chama main.py. Caso o nome seja outro, ajuste o comando (<nome_do_arquivo>:app).

Endpoints
1. Criptografia
URL: /encrypt

Método: POST

Payload de Exemplo:

json
Copiar
{
  "text": "Olá, mundo!",
  "key": null
}
Caso queira usar uma chave específica, ela deve ser enviada em base64 e ter exatamente 32 bytes (256 bits).

Resposta de Sucesso:

json
Copiar
{
  "encrypted_text": "texto_em_base64",
  "iv": "vetor_de_inicializacao_em_base64",
  "key": "chave_em_base64"
}
2. Descriptografia
URL: /decrypt

Método: POST

Payload de Exemplo:

json
Copiar
{
  "encrypted_text": "texto_em_base64",
  "key": "chave_em_base64",
  "iv": "vetor_de_inicializacao_em_base64"
}
Resposta de Sucesso:

json
Copiar
{
  "decrypted_text": "Olá, mundo!"
}
