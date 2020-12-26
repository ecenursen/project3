import secrets
import random
import sys, os
import bitcoin_keygen
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
import hashlib
import secp256k1

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

# create a private key object
private_key_object = secp256k1.PrivateKey(privateKey)

# create a recoverable ECDSA signature
recoverable_signature = private_key_object.ecdsa_sign_recoverable(
    msg_hash, raw=True)

# convert the result from ecdsa_sign_recoverable to a tuple composed of 64 bytes and an integer denominated as recovery id.
signature, recovery_id = private_key_object.ecdsa_recoverable_serialize(
    recoverable_signature)
recoverable_sig = bytes(bytearray(signature) + recovery_id.to_bytes(1, 'big'))

# base64 encode

"""
message = "I want this stream signed"
digest = SHA256.new()
digest.update(message)
signer = PKCS1_v1_5.new(privateKey)
sig = signer.sign(digest)
print(signer)
print(sig)
"""
