import secrets
import random
import sys, os
import bitcoin_keygen
import base64
import hashlib


# Private key generator
bits = secrets.randbits(256)
bitsHex = hex(bits)
privateKey = bitsHex[2:]
publicKey = bitcoin_keygen.private2public(privateKey)
address = bitcoin_keygen.public2address(publicKey)
print(bits)
print(bitsHex)
print("Private Key: ", privateKey)
print("Public Key: ", publicKey)
print("Address: ", address)

