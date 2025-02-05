
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
