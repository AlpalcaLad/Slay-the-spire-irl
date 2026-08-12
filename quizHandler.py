#auto pub quiz
import json
import requests
API_URL = "https://opentdb.com/api.php?amount=50&category=22"

response = requests.get(API_URL)
data = json.loads(response.text)["results"]

def question():
    if len(data)<=0:
        response = requests.get(API_URL)
        data = json.loads(response.text)["results"]
    return data.pop(0)