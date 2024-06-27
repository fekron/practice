import requests
import json

'''Не смог получить 100-ые и 500-ые статусы, так как 100-ые очень редкие и обычно не используются,
   а 500-ые указывают на ошибку со стороны сервера и также редко встречаются'''

url_reqres = "https://reqres.in/api"

request_ok = requests.request("GET",f'{url_reqres}/users?page=2')
request_create = requests.request("POST",f'{url_reqres}/posts',
                                    data = json.dumps({"title": "title", "body": "hand", "userId": 1}),
                                    headers = {'Content-Type': 'application/json'})
request_moved = requests.request('GET', url='http://github.com', allow_redirects=False)
request_bad = requests.request('POST', f'{url_reqres}/register',
                                        data=json.dumps({"email": "avangard@docs"}),
                                        headers = {'Content-Type': 'application/json'})
request_not_found = requests.request('GET', f'{url_reqres}/users/0')

print(f'Successful Response - {request_ok.status_code}\n',
      f'Successful Response - {request_create.status_code}\n',
      f'Redirect Response - {request_moved.status_code}\n',
      f'ErrorClient Response - {request_bad.status_code}\n',
      f'ErrorClient Response - {request_not_found.status_code}\n'
      )

