import os.path

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(result)


def test_get_api_key_for_upper_valid_user(email='MALYMAKS91@GMAIL.COM', password=valid_password):

    """Пробуем ввести валидный email в верхнем регистре и валидный пароль"""
    """ОР: status == 200 и ключа API должен быть в результате (регистронезависимость email)"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_actual_filter(filter='my_pets'):
    """Проверка работы вывода списка моих питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    print(result)


def test_post_add_a_new_pet_without_a_photo(name='Bas', animal_type='bird', age='3'):
    """Проверяем добавляется ли питомец без фото"""

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_a_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    print(result)


def test_put_update_pet(pet_id='a1d3a86e-c74d-4d42-a440-a61f3a47dc78',
                        name='Big_sister', animal_type='обезьяна', age='16'):
    """Проверка обновления данных существующего питомца"""

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.put_update_pet(auth_key, pet_id, name, animal_type, age)
    assert status == 200
    print(result)


def test_post_add_a_new_pet_with_a_photo(name='Buk', animal_type='Dog', age='10', pet_photo='image\Dog_cool.jpg'):
    """Проверяем добавляется ли питомец с фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_a_new_pet_with_a_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_photo_to_pet(pet_id='beb7e683-f5db-49d7-af49-1f379e1a72b8', pet_photo='image/Dog_cool.jpg'):
    """Проверяем что фото добавилось существующему уже питомцу, status == 200"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 200

def test_delete_pet(pet_id='7a37a5d1-191d-45f3-9d51-7de0e6b080f1'):
    """Проверка удаления питомца из database"""

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.delete_pet_from_database(auth_key, pet_id)

    assert status == 200
    assert pet_id not in result

def test_post_add_a_new_pet_with_a_photo_empty_str(name='', animal_type='', age='7', pet_photo='image\Dog_cool.jpg'):
    """Добавляется ли питомец только с одним фото без других заполненных атрибутов?"""
    """Если status == 200 -> это баг. Такого быть не должно"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_a_new_pet_with_a_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_photo_to_pet_text(pet_id='ec9fab80-bc53-4d10-9bf8-62483473c49a', pet_photo='image/File_text.txt'):
    """Проверка, что при добавлении .txt файла вместо фото .jpg существующему уже питомцу status == 500 -> баг"""
    """status == 400 или 403 должен быть"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 500


def test_post_add_a_new_pet_with_a_photo_not_valid(name='Milka', animal_type='Dog', age='10',
                                                   pet_photo='image\File_text.txt'):
    """Проверяем добавляется ли питомец НОВЫЙ если формат фото в .txt"""
    """Если status == 200 -> баг. По идее питомец вообще не должен добавиться. Должна появляться ошибка 400"""
    """Ведь это тест добавления питомца с ФОТО правильного формата!"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_a_new_pet_with_a_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_post_add_a_new_pet_with_a_photo_empty_str_all(name='', animal_type='', age='', pet_photo='image\File_text.txt'):
    """Добавляется ли питомец без заполненных атрибутов кроме фото в формате .txt?"""
    """Если status == 200 -> это баг. Такого быть не должно"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем авторизационный ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_a_new_pet_with_a_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_get_api_key_for_not_valid_user(email='MALYMAKS9@GMAIL.COM', password=valid_password):

    """Пробуем ввести невалидный email в верхнем регистре и валидный пароль"""
    """ОР: status == 400 or 403 и ключ API не должен быть в результате"""

    status, result = pf.get_api_key(email, password)
    assert status == 403 or status == 400
    assert 'key' not in result