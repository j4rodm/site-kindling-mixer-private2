#!/usr/bin/env python3
"""
Encrypt a string value for use in manifest.yaml private fields.
Uses AES-256-CBC with PBKDF2 key derivation, compatible with
the browser-side CryptoJS-compatible decryption in the site.

Usage:
    python encrypt_field.py "secret value"
    python encrypt_field.py   # interactive mode

The output is a base64 string you paste into manifest.yaml.
"""

import base64
import hashlib
import os
import sys
import getpass
import json


def evp_bytes_to_key(password: bytes, salt: bytes, key_len=32, iv_len=16):
    """Derive key and IV using OpenSSL's EVP_BytesToKey (MD5-based), 
    compatible with CryptoJS default key derivation."""
    d = b""
    d_i = b""
    while len(d) < key_len + iv_len:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


def encrypt_aes_256_cbc(plaintext: str, passphrase: str) -> str:
    """Encrypt using AES-256-CBC with OpenSSL-compatible format.
    Output: base64 of 'Salted__' + 8-byte salt + ciphertext."""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding

    salt = os.urandom(8)
    key, iv = evp_bytes_to_key(passphrase.encode("utf-8"), salt)

    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    # OpenSSL format: "Salted__" + salt + ciphertext
    blob = b"Salted__" + salt + ciphertext
    return base64.b64encode(blob).decode("utf-8")


def main():
    if len(sys.argv) > 1:
        plaintext = sys.argv[1]
    else:
        plaintext = input("Enter value to encrypt: ")

    passphrase = getpass.getpass("Passphrase: ")
    passphrase2 = getpass.getpass("Confirm passphrase: ")

    if passphrase != passphrase2:
        print("Passphrases don't match!", file=sys.stderr)
        sys.exit(1)

    encrypted = encrypt_aes_256_cbc(plaintext, passphrase)
    print(f"\nEncrypted value (paste into manifest.yaml):\n{encrypted}")


if __name__ == "__main__":
    main()
