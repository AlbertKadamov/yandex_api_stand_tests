import sender_stand_request
import data

def get_user_body(firts_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = firts_name
    return current_body

# Функция для позитивной проверки
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

# Функци для негативной проверки
# В ответе ошибка: "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"


# Функция для негативной проверки
# В ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 1. В параметре firstName допустимое кол-во символов (2)
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2. В параметре firstName Допустимое кол-во символов (15)
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Тест 3. В параметре firstName кол-во символов меньше допустимого
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Тест 4. В параметре firstName кол-во символов больше допустимого
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

# Тест 5. В параметре firstName разрешены английские символы
def test_create_user_english_letter_in_first_name_get_succes_response():
    positive_assert("QWErty")

# Тест 6. В параметре firstName разрешены русские символы
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 7. В параметре firstName запрещены пробелы
def test_create_user_has_space_in_first_name_get_response():
    negative_assert_symbol("Человек и Ко")

# Тест 8. В firstName запрещены Спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

# Тест 9. В firstName запрещены цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Тест 10. Параметр firstName не передан
def test_create_user_no_first_name_get_error_response():
       user_body = data.user_body.copy()
       user_body.pop("firstName")
       negative_assert_no_firstname(user_body)

# Тест 11. Передано пустое значение параметра firstName
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

#Тест 12. Передан другой тип параметра firstName: число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
