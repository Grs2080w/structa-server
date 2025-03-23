import jwt

# first import the module
from cryptography.hazmat.primitives import serialization

# envs
from config.settings import config


def token_encode(token):
    """
    Encode a token using a private key loaded from a file.

    Args:
        token (dict): The token to be encoded.

    Returns:
        str: The encoded token.

    """

    private_key = open("ssh/.ssh", "r").read()
    private_key_decode = serialization.load_ssh_private_key(
        private_key.encode(), password=config["PASSWORD_SSH_KEY"].encode()
    )
    return jwt.encode(token, private_key_decode, algorithm="RS256")


def token_decode(token):
    """
    Decode a token using a public key loaded from a file.

    Args:
        token (str): The token to be decoded.

    Returns:
        dict: The decoded token.

    """
    public_key = open("ssh/.ssh.pub", "r").read()
    public_key_decode = serialization.load_ssh_public_key(public_key.encode())
    return jwt.decode(token, public_key_decode, algorithms=["RS256"])
