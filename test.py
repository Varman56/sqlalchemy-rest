from requests import post, get, delete, put
from pprint import pprint

# # ТЕСТИРОВАНИЕ МОДЕЛИ USER
# # Выводим список пользователей
# pprint(get('http://localhost:8080/api/v2/users').json())
# # Создадим нового пользователя
# pprint(post('http://localhost:8080/api/v2/users', json={
#     'id': 10,
#     'surname': "derckach",
#     'name': 'dmitriy',
#     'age': 16,
#     'position': 'pilot',
#     'city_from': 'Вашингтон',
#     'speciality': "programier",
#     'address': "module_3",
#     'email': "derkach@earth.org",
#     'password': 'qwerty123'}).json())
# # Выводим информацию об одном пользователе
# pprint(get('http://localhost:8080/api/v2/users/10').json())
# # Ошибочный запрос на получение пользователя - стркоа
# pprint(get('http://localhost:8080/api/v2/users/qwerty'))
# # Удаление пользователя
# pprint(delete('http://localhost:8080/api/v2/users/10').json())
# # Ошибочный запрос на удаление несущствующего пользователя
# pprint(delete('http://localhost:8080/api/v2/users/10').json())
# # Ошибочный запрос на получение несущствующего пользователя
# pprint(get('http://localhost:8080/api/v2/users/10').json())
# # Ошибочный запрос на создание пользователя с неполными данными
# pprint(post('http://localhost:8080/api/v2/users', json={
#     'surname': "derckach",
#     'name': 'dmitriy',
#     'position': 'pilot',
#     'speciality': "programier",
#     'address': "module_3",
#     'email': "derkach@earth.org",
#     'password': 'qwerty123'}).json())
# # Создание пользователя
# pprint(post('http://localhost:8080/api/v2/users', json={
#     'id': 10,
#     'surname': "derckach",
#     'name': 'dmitriy',
#     'age': 16,
#     'position': 'pilot',
#     'city_from': 'Вашингтон',
#     'speciality': "programier",
#     'address': "module_3",
#     'email': "derkach@earth.org",
#     'password': 'qwerty123'}).json())
# # Изменяем пользователя
# pprint(put('http://localhost:8080/api/v2/users/10', json={
#     'surname': "derckach",
#     'name': 'dmitriy',
#     'age': 20,
#     'position': 'duty',
#     'city_from': 'Оренбург',
#     'speciality': "programier",
#     'address': "module_15",
#     'email': "derkach@earth.org",
#     'password': 'qwerty123'}).json())
# # Проверяем изменения
# pprint(get('http://localhost:8080/api/v2/users/10').json())
# # Ошибочный запрос на изменение с неполными данными
# pprint(put('http://localhost:8080/api/v2/users/10', json={
#     'surname': "derckach",
#     'name': 'dmitriy',
#     'city_from': 'Оренбург',
#     'speciality': "programier",
#     'address': "module_15",
#     'password': 'qwerty123'}).json())

# ТЕСТИРОВАНИЕ МОДЕЛИ JOBS
# Получение всех работ
pprint(get('http://localhost:8080/api/v2/jobs').json())
# Получение одной работы
pprint(get('http://localhost:8080/api/v2/jobs/1').json())
# Ошибочный запрос на получение несуществующей работы
pprint(get('http://localhost:8080/api/v2/jobs/9999'))
# Ошибочный запрос - строка
pprint(get('http://localhost:8080/api/v2/jobs/strk'))
# Корректный запрос на создание
pprint(post('http://localhost:8080/api/v2/jobs',
            json={'id': 6,
                  'team_leader': 2,
                  'job': 'Работа',
                  'work_size': 13,
                  'collaborators': '1, 3',
                  'is_finished': False,
                  'categories': 5}).json())
# Ошибочный запрос на создание работы с уже существующим id
pprint(post('http://localhost:8080/api/v2/jobs',
            json={'id': 6,
                  'team_leader': 2,
                  'job': 'Работа',
                  'work_size': 13,
                  'collaborators': '1, 3',
                  'is_finished': False,
                  'categories': 5}).json())
# Ошибочный запрос на создание без некоторых обязательных ключей
pprint(post('http://localhost:8080/api/v2/jobs',
            json={'id': 2,
                  'team_leader': 2,
                  'work_size': 13,
                  'collaborators': '1, 3',
                  'is_finished': False,
                  'categories': 5}).json())
# Ошибочный запрос на создание без всех полей
pprint(post('http://localhost:8080/api/v2/jobs').json())
# Проверяем, что работа доабавилась
pprint(get('http://localhost:8080/api/v2/jobs').json())
# Запрос на удаление работы
print(delete('http://localhost:8080/api/v2/jobs/6').json())
# Ошибочный запрос на удаление несуществующей работы
print(delete('http://localhost:8080/api/v2/jobs/6').json())
# Ошибочный запрос - текст
print(delete('http://localhost:8080/api/v2/jobs/qwerty'))
# Проверяем, что работа удалена
pprint(get('http://localhost:8080/api/v2/jobs').json())
# Создание работы
pprint(post('http://localhost:8080/api/v2/jobs',
            json={'id': 6,
                  'team_leader': 2,
                  'job': 'Работа',
                  'work_size': 13,
                  'collaborators': '1, 3',
                  'is_finished': False,
                  'categories': 5}).json())
# Изменяем работу
pprint(put('http://localhost:8080/api/v2/jobs/6',
           json={'team_leader': 1,
                 'job': 'НЕ РАБОТА',
                 'work_size': 24,
                 'collaborators': '3',
                 'is_finished': True,
                 'categories': 2}).json())
# Проверяем, что работа изменилась
pprint(get('http://localhost:8080/api/v2/jobs/6').json())
# Удаляем работу
print(delete('http://localhost:8080/api/v2/jobs/6').json())
# Ошибочный запрос на изменение несуществующей работы
pprint(put('http://localhost:8080/api/v2/jobs/6',
           json={'team_leader': 2,
                 'job': 'Работа',
                 'work_size': 13,
                 'collaborators': '1, 3',
                 'is_finished': False,
                 'categories': 5}).json())
# Создание работы
pprint(post('http://localhost:8080/api/v2/jobs',
            json={'id': 6,
                  'team_leader': 2,
                  'job': 'Работа',
                  'work_size': 13,
                  'collaborators': '1, 3',
                  'is_finished': False,
                  'categories': 5}).json())
# Ошибочный запрос на изменение без всех полей
pprint(put('http://localhost:8080/api/v2/jobs/6').json())
# Ошибочный запрос на изменение без некоторых полей
pprint(put('http://localhost:8080/api/v2/jobs/6',
           json={'team_leader': 2,
                 'job': 'Работа',
                 'work_size': 13}).json())
