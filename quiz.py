import requests

response = requests.get("https://opentdb.com/api.php?amount=10&category=28&type=multiple")
data = response.json()['results']
