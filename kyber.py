from kyber import Kyber512
from aes256_ctr_drbg import AES256_CTR_DRBG
import requests
import os
from dotenv import load_dotenv
load_dotenv()

#### Retrieve Access Token and Entropy Size

token = "your-access-token"
size = "entropy-size-required"

# Define the endpoint
url = f'https://qum-backend.azurewebsites.net/t32/quentom-entropy'
entropy = ''

# Define and submit the request
headers = { 'Authorization': f'Bearer {token}' }
querystring = { 'size': size }
response = requests.get( url, headers=headers, params=querystring)
s = str(response.json()['random_number'])

entropy = s[:48]
entropy = bytes(entropy, 'utf-8')

#### Initialize DRBG

rng = AES256_CTR_DRBG(entropy)


#### Perform key exchange

print("Starting Kyber512 key exchange:")
message = input("Enter a message to sign/encrypt: ")

Kyber512.set_drbg_seed(rng.random_bytes(48))
public_key, private_key = Kyber512.keygen()
ciphertext, shared_secret = Kyber512.enc(public_key, message)
decrypted = Kyber512.dec(ciphertext, private_key)

#### Verify decryption worked

print("Public key:", public_key.hex())
print("Private key:", private_key.hex())
print("Ciphertext:", ciphertext.hex())
print("Shared secret:", shared_secret.hex())
print("Decrypted shared secret:", decrypted.hex())

# Verify decryption worked
assert shared_secret == decrypted

print("\nKey exchange completed successfully!")