import requests

url = 'https://vilistil.com/vs/item/10003'

response = requests.get(url)

data = response.json()

print(response.status_code)