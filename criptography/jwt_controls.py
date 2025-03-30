import jwt

# first import the module
from cryptography.hazmat.primitives import serialization

# envs
from config.settings import config

"""
This module contains all the functions to handle JWT

Functions:

    token_encode: function to encode a token with a private key
    token_decode: function to decode a token with a public key

The functions rely on the cryptography library to handle the encryption and
decryption of the tokens.
"""


def token_encode(token):
    private_key = open("ssh/.ssh", "r").read()
    private_key_decode = serialization.load_ssh_private_key(
        private_key.encode(), password=config["PASSWORD_SSH_KEY"].encode()
    )
    return jwt.encode(token, private_key_decode, algorithm="RS256")


def token_decode(token):
    public_key = open("ssh/.ssh.pub", "r").read()
    public_key_decode = serialization.load_ssh_public_key(public_key.encode())
    return jwt.decode(token, public_key_decode, algorithms=["RS256"])
