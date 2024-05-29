
import requests
import os
from dotenv import load_dotenv
load_dotenv()
import math 
import sympy
import gmpy2

token = "your-access-token"
size = "entropy-size-required"

# Define the endpoint
url = f'https://qum-backend.azurewebsites.net/t32/quentom-entropy'

# Define and submit the request
headers = { 'Authorization': f'Bearer {token}' }
querystring = { 'size': size }


#### Get P and Q

p = ''
while True:
    response = requests.get( url, headers=headers, params=querystring)
    
    s = str(response.json()['random_number'])
    priv_key = int(''.join(filter(str.isdigit, s)))

    priv_key = priv_key % 10**32
    if sympy.isprime(p):
        break
    else:
        p=''
        
q = ''
while True:
    response = requests.get( url, headers=headers, params=querystring)
    
    s = str(response.json()['random_number'])

    priv_key = int(''.join(filter(str.isdigit, s)))
    priv_key = priv_key % 10**32
    if sympy.isprime(q):
        break
    else:
        q=''


#### Calculate Variables

n = p*q
phi = (p-1)*(q-1)
e = 2

while(e<phi):
    if (math.gcd(e, phi) == 1):
        break
    else:
        e += 1
 
k = 2
d = ((k*phi)+1)/e

#### Encryption

msg = int(input("Enter a message to encrypt: "))
C = pow(msg, e)
C = math.fmod(C, n)
print(f'Encrypted message: {C}')

#### Decryption

C_mpz = gmpy2.mpz(C)
M = gmpy2.powmod(C_mpz, int(d), n)
print(f'Decrypted message: {M}')  
