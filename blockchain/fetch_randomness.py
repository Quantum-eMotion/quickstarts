import os
import requests

def get_random_bits_from_qrng_api():
    token = "your-access-token"
    size = "entropy-size-required"
    url = f'https://api-qxeaas.quantumemotion.com/entropy'
    headers = { 'Authorization': f'Bearer {token}' }
    querystring = { 'size': size }

    response = requests.get(url, headers=headers, params=querystring)
    random_num = int(''.join(filter(str.isdigit, response.json()['random_number'])))
    random_num = random_num % 10**64

    return random_num

def send_random_bits_to_smart_contract(random_bits):
    # Connect to the Ethereum network (e.g., Ganache, Infura, etc.)
    w3 = Web3(Web3.HTTPProvider('https://your-ethereum-node-url'))

    # Set the contract address and ABI (Application Binary Interface)
    contract_address = '0x5B38Da6a701c568545dCfcB03FcB875f56beddC4'
    contract_abi = [
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_randomNumber",
                    "type": "uint256"
                }
            ],
            "name": "setRandomNumber",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]

    # Create a contract instance
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Call the setRandomNumber() function
    tx = contract.functions.setRandomNumber(random_bits).transact()
    w3.eth.waitForTransactionReceipt(tx)

    print(f"Random bits sent to the smart contract: {random_bits}")
random_bits= get_random_bits_from_qrng_api()
send_random_bits_to_smart_contract(random_bits)