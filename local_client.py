import requests

print(requests.get('http://3.101.13.147:8080/similar_users?', params={'user_id': 1, 'user_num': 1}).text)
