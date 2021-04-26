from requests import post, get, delete, put
from pprint import pprint

# Выводим список пользователей
pprint(get('http://localhost:8080/api/v2/users').json())
# Создадим нового пользователя
pprint(post('http://localhost:8080/api/v2/users', json={
    'id': 10,
    'surname': "derckach",
    'name': 'dmitriy',
    'age': 16,
    'position': 'pilot',
    'city_from': 'Вашингтон',
    'speciality': "programier",
    'address': "module_3",
    'email': "derkach@earth.org",
    'password': 'qwerty123'}).json())
# Выводим информацию об одном пользователе
pprint(get('http://localhost:8080/api/v2/users/10').json())
# Ошибочный запрос на получение пользователя - стркоа
pprint(get('http://localhost:8080/api/v2/users/qwerty'))
# Удаление пользователя
pprint(delete('http://localhost:8080/api/v2/users/10').json())
# Ошибочный запрос на удаление несущствующего пользователя
pprint(delete('http://localhost:8080/api/v2/users/10').json())
# Ошибочный запрос на получение несущствующего пользователя
pprint(get('http://localhost:8080/api/v2/users/10').json())
# Ошибочный запрос на создание пользователя с неполными данными
pprint(post('http://localhost:8080/api/v2/users', json={
    'surname': "derckach",
    'name': 'dmitriy',
    'position': 'pilot',
    'speciality': "programier",
    'address': "module_3",
    'email': "derkach@earth.org",
    'password': 'qwerty123'}).json())
# Создание пользователя
pprint(post('http://localhost:8080/api/v2/users', json={
    'id': 10,
    'surname': "derckach",
    'name': 'dmitriy',
    'age': 16,
    'position': 'pilot',
    'city_from': 'Вашингтон',
    'speciality': "programier",
    'address': "module_3",
    'email': "derkach@earth.org",
    'password': 'qwerty123'}).json())
# Изменяем пользователя
pprint(put('http://localhost:8080/api/v2/users/10', json={
    'surname': "derckach",
    'name': 'dmitriy',
    'age': 20,
    'position': 'duty',
    'city_from': 'Оренбург',
    'speciality': "programier",
    'address': "module_15",
    'email': "derkach@earth.org",
    'password': 'qwerty123'}).json())
# Проверяем изменения
pprint(get('http://localhost:8080/api/v2/users/10').json())
# Ошибочный запрос на изменение с неполными данными
pprint(put('http://localhost:8080/api/v2/users/10', json={
    'surname': "derckach",
    'name': 'dmitriy',
    'city_from': 'Оренбург',
    'speciality': "programier",
    'address': "module_15",
    'password': 'qwerty123'}).json())
