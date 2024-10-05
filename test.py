import requests

r = requests.get('https://htv-project.onrender.com/api/getrecords').json()

print(r)