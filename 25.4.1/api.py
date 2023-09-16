import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        """Метод позволяет получить ключ API, который нужно использовать для других методов API"""

        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):

        """Метод позволяет получить список домашних питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_a_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: float) -> json:

        """Метод отправляет запрос на сервер для создания нового питомца без фото на сайте"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'Content-Type': data.content_type, 'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_a_new_pet_with_a_photo(self, auth_key: json, name: str, animal_type: str, age: float, pet_photo: str) -> json:

        """Метод отправляет запрос на сервер для создания нового питомца с фото на сайте"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def add_photo_to_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:

        """Метод отправляет на сервер фото к добавленному ранее питомцу. Возвращает статус
        запроса  и данные питомца в JSON"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def put_update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: float) -> json:

        """Метод обновления информации о существущем питомце"""

        data = MultipartEncoder(
            fields={
            'name': name,
            'animal_type': animal_type,
            'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str) -> json:

        """Метод удаления питомца из database по pet_id."""
        """В (Swagger) документации API список питомцев конкретного пользователя или всех на сайте"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

