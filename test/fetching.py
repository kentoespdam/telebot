import requests

url="https://prometheus.perumdamts.id/api/v1/targets"
response = requests.get(url)
print(response.json())