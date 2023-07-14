import requests

url = 'https://discord.com/api/oauth2/token'
headers = {
    'Content-Type':"application/x-www-form-urlencoded"
    }
data = {
    "client_id":"1128957735157899274",
    'grant_type': 'authorization_code',
    "client_secret":"P3isfqh76Sucr-bzLVew8FrVeA2jUB3j"
}

token = requests.post(url, data=data, headers=headers)

print(token.text)



