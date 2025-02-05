import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn")

app = FastAPI()

class EncryptionRequest(BaseModel):
    text: str
    key: str = None

class DecryptionRequest(BaseModel):
    encrypted_text: str
    key: str
    iv: str

def encrypt_aes256(text: str, key: bytes) -> dict:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_text = padder.update(text.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_text) + encryptor.finalize()

    return {
        "encrypted_text": base64.b64encode(encrypted_data).decode(),
        "iv": base64.b64encode(iv).decode()
    }

def decrypt_aes256(encrypted_data: bytes, key: bytes, iv: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted_data.decode('utf-8')

@app.post("/encrypt")
def encrypt(request: EncryptionRequest):
    logger.info(f"Requisição de criptografia recebida: {request.dict()}")

    if not request.key:
        key = os.urandom(32)
    else:
        try:
            key = base64.b64decode(request.key)
        except Exception as e:
            logger.error(f"Erro no decode da chave: {str(e)}")
            raise HTTPException(status_code=400, detail="Chave em base64 inválida")

    if len(key) != 32:
        logger.error("A chave fornecida não tem 256 bits (32 bytes).")
        raise HTTPException(status_code=400, detail="A chave deve ter 256 bits (32 bytes) em base64.")

    try:
        result = encrypt_aes256(request.text, key)
        logger.info(f"Texto criptografado: {result}")

        return {
            "encrypted_text": result["encrypted_text"],
            "iv": result["iv"],
            "key": base64.b64encode(key).decode()
        }
    except Exception as e:
        logger.error(f"Erro durante a criptografia: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decrypt")
def decrypt(request: DecryptionRequest):
    logger.info(f"Requisição de descriptografia recebida: {request.dict()}")

    try:
        key = base64.b64decode(request.key)
        iv = base64.b64decode(request.iv)
        encrypted_data = base64.b64decode(request.encrypted_text)
    except Exception as e:
        logger.error(f"Erro no decode base64: {str(e)}")
        raise HTTPException(status_code=400, detail="Dados em base64 inválidos")

    if len(key) != 32:
        logger.error("Chave inválida: tamanho diferente de 256 bits")
        raise HTTPException(status_code=400, detail="Chave deve ter 256 bits (32 bytes)")
    if len(iv) != 16:
        logger.error("IV inválido: tamanho diferente de 128 bits")
        raise HTTPException(status_code=400, detail="IV deve ter 128 bits (16 bytes)")

    try:
        decrypted_text = decrypt_aes256(encrypted_data, key, iv)
        return {"decrypted_text": decrypted_text}
    except ValueError as e:
        logger.error(f"Erro de padding: {str(e)}")
        raise HTTPException(status_code=400, detail="Dados criptografados corrompidos")
    except Exception as e:
        logger.error(f"Erro na descriptografia: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno na descriptografia")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)