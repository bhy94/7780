
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import hashlib 
from fastapi import Request, HTTPException
from models import RESPONSE
from copy import deepcopy

def aes_encryption(plaintext: bytes, secret: bytes) -> bytes:
    _h = hashlib.sha512(secret).digest()
    key, iv = _h[:32], _h[32:48]
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # encrypt
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext


def aes_decryption(ciphertext: bytes, secret: bytes) -> bytes:
    _h = hashlib.sha512(secret).digest()
    key, iv = _h[:32], _h[32:48]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    # decrypt
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    # delete padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

async def authentication(request: Request):
    pool = request.app.state.pool
    try:
        cookie_str = request.cookies.get("token")
        role = request.cookies.get("role")
        assert role in ["admin", "vendor", "user"]
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT {role}_id FROM login_status_{role} WHERE token = %s", (cookie_str,))
                rid = await cur.fetchone()
                if rid is None:
                    raise Exception("No user found")
                return {
                    "success": 1,
                    "rid": rid[0],
                    "sid": cookie_str, 
                    "role": role
                }
    except Exception as e:
        return {
            "success": 0,
            "rid": 0,
            "sid": "", 
            "role": "None"
        }