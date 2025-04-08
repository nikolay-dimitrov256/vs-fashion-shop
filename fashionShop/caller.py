import requests

url = 'https://vilistil.com/vs/cat/dresses'

response = requests.get(url)

data = response.json()

print(data)