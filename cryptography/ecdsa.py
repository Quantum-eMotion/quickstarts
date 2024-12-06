import requests
import base64
from ecdsa import SigningKey
import os
from dotenv import load_dotenv
load_dotenv()


token = "your-access-token"
size = "entropy-size-required"
url = f'https://api-qxeaas.quantumemotion.com/entropy'

#### Define and submit the request

headers = { 'Authorization': f'Bearer {token}' }
querystring = { 'size': size }
response = requests.get( url, headers=headers, params=querystring)

#### Process the response

priv_key = ''
s = str(response.json()['random_number'])
priv_key = int(''.join(filter(str.isdigit, s)))
priv_key = priv_key % 10**64

#### Generate ECDSA key pair

sk = SigningKey.from_secret_exponent(priv_key)
public_key = sk.get_verifying_key()

#### Sign a message

message = input("Enter a message to encrypt: ")
signature = sk.sign(message)

#### Verify the signature

assert public_key.verify(signature, message), "Signature verification failed"
