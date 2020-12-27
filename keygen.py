import codecs
import hashlib
import ecdsa
import secrets
import bitcoin_keygen
from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5








def generate_compressed_address(private_key):
    public_key = __private_to_compressed_public(private_key)
    address = __public_to_address(public_key)
    return address

def private_to_public(private_key):
    private_key_bytes = codecs.decode(private_key, 'hex')
    # Get ECDSA public key
    key = ecdsa.SigningKey.from_string(
        private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')
    # Add bitcoin byte
    bitcoin_byte = b'04'
    public_key = bitcoin_byte + key_hex
    return public_key


def __private_to_compressed_public(private_key):
    private_hex = codecs.decode(private_key, 'hex')
    # Get ECDSA public key
    key = ecdsa.SigningKey.from_string(
        private_hex, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')
    # Get X from the key (first half)
    key_string = key_hex.decode('utf-8')
    half_len = len(key_hex) // 2
    key_half = key_hex[:half_len]
    # Add bitcoin byte: 0x02 if the last digit is even, 0x03 if the last digit is odd
    last_byte = int(key_string[-1], 16)
    bitcoin_byte = b'02' if last_byte % 2 == 0 else b'03'
    public_key = bitcoin_byte + key_half
    return public_key


def public_to_address(public_key):
    public_key_bytes = codecs.decode(public_key, 'hex')
    # Run SHA256 for the public key
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()
    # Run ripemd160 for the SHA256
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
    # Add network byte
    network_byte = b'00'
    network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
    network_bitcoin_public_key_bytes = codecs.decode(
        network_bitcoin_public_key, 'hex')
    # Double SHA256 to get checksum
    sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
    sha256_nbpk_digest = sha256_nbpk.digest()
    sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
    sha256_2_nbpk_digest = sha256_2_nbpk.digest()
    sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
    checksum = sha256_2_hex[:8]
    # Concatenate public key and checksum to get the address
    address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
    wallet = base58(address_hex)
    return wallet


def base58(address_hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    b58_string = ''
    # Get the number of leading zeros and convert hex to decimal
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    # Convert hex to decimal
    address_int = int(address_hex, 16)
    # Append digits to the start of string
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    # Add '1' for each 2 leading zeros
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = '1' + b58_string
    return b58_string


def to_dict(sender_address="Joshgun", recipient_address="Ece", value=1000):
    return OrderedDict({'sender_address': sender_address,
                        'recipient_address': recipient_address,
                        'value': value})


def sign_transaction(privateKey):
    private_key = RSA.importKey(
        binascii.unhexlify(privateKey))
    signer = PKCS1_v1_5.new(private_key)
    h = SHA.new(str(to_dict()).encode('utf8'))
    return binascii.hexlify(signer.sign(h)).decode('ascii')

# Private key generator
bits = secrets.randbits(256)
bitsHex = hex(bits)
privateKey = bitsHex[2:]
print(bits)
print(bitsHex)
print(privateKey)
publicKey = private_to_public(privateKey)
address = public_to_address(publicKey)
print(publicKey)
publick2 = bitcoin_keygen.private2public(privateKey)
print(publick2)
print(bitcoin_keygen.public2address(publick2))
print(address)

print("signedd: ", sign_transaction(privateKey) )


