import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Your Piñata API endpoint
url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'

# Replace these with your actual API key, API secret, and JWT
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
jwt = os.getenv('JWT')

# Prepare the headers for the request
headers = {
    'Authorization': f'Bearer {jwt}',
    'pinata_api_key': api_key,
    'pinata_secret_api_key': api_secret,
}

# Path to the file you want to upload
file_path = 'sample.json'

# Open the file in binary mode
with open(file_path, 'rb') as file:
    files = {
        'file': (file.name, file)
    }
    
    # Make the request to Piñata
    response = requests.post(url, files=files, headers=headers)

    # Print the response
    print(response.text)

# Error handling
if response.status_code != 200:
    print(f'Error: {response.status_code}')
    print(response.text)
