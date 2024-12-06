import os
from dotenv import load_dotenv
token = os.environ.get("ACCESS_TOKEN")
size = "required-size-for-your-application"

# Define the endpoint
url = f'https://api-qxeaas.quantumemotion.com/entropy'

# Define and submit the request
headers = { 'Authorization': f'Bearer {token}'}
querystring = { 'size': size }
response = requests.get( url, headers=headers, params=querystring)

response = response.json()
print('response =>', response)