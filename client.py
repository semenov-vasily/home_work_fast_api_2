import requests

"""-----Запросы для записи, получения, изменения и удаления юзера в бд-----"""

"""-----Запись нового юзера-------------------------------------------------"""
# response = requests.post('http://127.0.0.1:8000/v1/user/',
#                          json={
#                              "name": "user_3",
#                              "password": "12345",
#                          })
# print(response.json())
# print(response.status_code)

"""-----Запись юзеру токена---------------------------------------------"""
# response = requests.post('http://127.0.0.1:8000/v1/login/',
#                          json={
#                              "name": "user_3",
#                              "password": "12345",
#                          })
# print(response.json())
# print(response.status_code)
# token = response.json()["token"]


"""-----Изменение юзера  по его id---------------------------------"""
# response = requests.patch('http://127.0.0.1:8000/v1/user/4/',
#                           headers={"xtoken": token},
#                           json={
#                               'name': "user_2a",
#                               'password': '11223',
#                           })
# print(response.json())
# print(response.status_code)


"""-----Удаление юзера по его id-----------------------------------"""
# response = requests.delete('http://127.0.0.1:8000/v1/user/2/', headers={"xtoken": token})
# print(response.json())
# print(response.status_code)


"""-----Получение юзера по его id-----------------------------------"""
# response = requests.get('http://127.0.0.1:8000/v1/user/4/', headers={"xtoken": token},)
# print(response.json())
# print(response.status_code)



# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
"""-----Запросы для записи, получения, изменения и удаления объявления в бд-----"""

"""-----Запись нового объявления нужен токен юзера ----------------------------------"""
# response = requests.post('http://127.0.0.1:8000/v1/advertisement/',
#                          headers={"xtoken": token},
#                          json={
#                              'title': "advertisement_1",
#                              'description': 'text of description 1',
#                              'price': 100})
# print(response.json())
# print(response.status_code)


"""-----Изменение объявления  по его id нужен токен юзера------------------------------"""
# response = requests.patch('http://127.0.0.1:8000/v1/advertisement/10/',
#                           headers={"xtoken": token},
#                           json={
#                               'title': "advertisement_12333",
#                               'description': 'text of description aaaaaaccccasdafa',
#                               'price': 200,
#                           })
# print(response.json())
# print(response.status_code)


"""-----Удаление объявления по его id  нужен токен юзера-------------------------------"""
# response = requests.delete('http://127.0.0.1:8000/v1/advertisement/2/',
#                            headers={"xtoken": token})
# print(response.json())
# print(response.status_code)


"""-----Получение объявления по его id токен юзера не нужен (юзер может быть не авторизован)---"""
# response = requests.get('http://127.0.0.1:8000/v1/advertisement/1/', )
# print(response.json())
# print(response.status_code)


"""-----Получение объявления по полю id токен юзера не нужен (юзер может быть не авторизован)---"""
# response = requests.get('http://127.0.0.1:8000/v1/advertisement_id?advertisement_id=1', )
# print(response.json())
# print(response.status_code)


"""-----Получение объявления по полю title токен юзера не нужен (юзер может быть не авторизован)---"""
# response = requests.get('http://127.0.0.1:8000/v1/advertisement_title?title=advertisement_1')
# print(response.json())
# print(response.status_code)


"""-----Получение объявления по полю title токен юзера не нужен (юзер может быть не авторизован)---"""
response = requests.get('http://127.0.0.1:8000/v1/advertisement_title_2?title=advertisement_1')
print(response.json())
print(response.status_code)
