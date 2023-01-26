import requests

print(requests.get('http://127.0.0.1:5000/similar_users?', params={'user_id': 1, 'user_num': 1}).text)
