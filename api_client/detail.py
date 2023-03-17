import requests 

endpoint = "http://localhost:8000/api/allergnes/"

get_reponse = requests.get(endpoint)
print(get_reponse.json())