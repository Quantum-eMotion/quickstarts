import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

#### Request random number
token = "your-access-token"
size = "entropy-size-required"

url = f'https://qum-backend.azurewebsites.net/t32/quentom-entropy'
headers = { 'Authorization': f'Bearer {token}' }
querystring = { 'size': size }

def get_random_int():
    
    response = requests.get(url, headers=headers, params=querystring)
    random_num = int(''.join(filter(str.isdigit, response.json()['random_number'][:-19])))
    # truncate the timestamp from the random_numbers, which is the last 19 characters.
    return random_num % 10**2

#### Main function

def main():
    
    # Get CSV file path and num samples
    csv_file = input("Enter CSV file path: ") 
    num_samples = int(input("Enter number of samples: "))

    import chardet

    with open(csv_file, "rb") as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']

    # Read CSV into DataFrame using Pandas
    df = pd.read_csv(csv_file, encoding=encoding)

    # Get total rows
    total_rows = len(df)  

    # Get random indices
    indices = []
    for i in range(num_samples):
        random_index = get_random_int() % total_rows
        indices.append(random_index)
        
    # Print random samples    
    for i in indices:
        print(df.loc[i])
        
if __name__ == "__main__":
    main()