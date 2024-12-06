from dilithium import Dilithium2, Dilithium3, Dilithium5
import requests
import os
from dotenv import load_dotenv
load_dotenv()

#### Define Function to sign and verify

def sign_and_verify(dilithium_variant, message):
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
  entropy = s[:16]
  entropy = bytes(entropy, 'utf-8')
  message = message + entropy
  # Generate keypair
  pk, sk = dilithium_variant.keygen()

  # Sign the message
  signature = dilithium_variant.sign(sk, message)

  # Verify the signature
  verification_result = dilithium_variant.verify(pk, message, signature)

  # Print results
  print(f"Public Key (hex): {pk.hex()}")
  print(f"Signature (hex): {signature.hex()}")
  print(f"Verification Result: {'Success' if verification_result else 'Failed'}")

#### Prompts the user for a message

def main():
  """
  Prompts the user for a message to sign and allows choosing a Dilithium variant.
  """
  while True:
    message = input("Enter message to sign (or 'q' to quit): ")
    if message == 'q':
      break

    print("Choose Dilithium variant:")
    print("1. Dilithium2")
    print("2. Dilithium3")
    print("3. Dilithium5")

    choice = input("Enter your choice (1-3): ")
    if choice not in ('1', '2', '3'):
      print("Invalid choice. Please try again.")
      continue

    variant_map = {
      '1': Dilithium2,
      '2': Dilithium3,
      '3': Dilithium5
    }
    dilithium_variant = variant_map[choice]

    sign_and_verify(dilithium_variant, message.encode())  # Encode message to bytes

if __name__ == "__main__":
  main()