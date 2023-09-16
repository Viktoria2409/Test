from time import sleep
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base import AuthForm, CodeForm
from settings import valid_email, valid_password, valid_number, valid_login, valid_account


# TC-002 (открываем страницу авторизации, создаем скриншот страницы)
def test_scr_page_auth_form(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('01.jpg')


# TC-005 (проверяем что по умолчанию страница авторизации открывается на вкладке "Телефон")
def test_phone_by_default(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


# TC-006 (проверяем что вкладки на странице авторизации переключаются автоматически при указании
# телефона/почты/логина/лицевого счета)
def test_automatic_change_tub(selenium):
    form = AuthForm(selenium)

    # вводим номер телефона
    form.username.send_keys('+79174586955')
    form.password.send_keys('hgfjgfjhmghg')
    sleep(5)

    assert form.placeholder.text == 'Мобильный телефон'

    # очищаем поле логин
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим почту
    form.username.send_keys('hkgkhgh@mail.ru')
    form.password.send_keys('jhjhvjfjgfjhghg')
    sleep(5)

    assert form.placeholder.text == 'Электронная почта'

    # очищаем поле логин
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим логин
    form.username.send_keys('Ziliboba')
    form.password.send_keys('chxjchdd')
    sleep(5)

    assert form.placeholder.text == 'Логин'

    # очищаем поле логин
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим номер лицевого счета
    form.username.send_keys('012345678910')
    form.password.send_keys('hbdsjvbdjfbv')
    sleep(5)

    assert form.placeholder.text == 'Лицевой счёт'


# TC-007 (авторизация по зарегистрированным номеру телефона и паролю)
def test_auth_reg_phone(selenium):
    form = AuthForm(selenium)

    # вводим номер телефона и пароль
    form.username.send_keys(valid_number)
    form.password.send_keys(valid_password)
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# TC-008 (авторизация по незарегистрированным телефону и паролю)
def test_auth_fake_phone(selenium):
    form = AuthForm(selenium)

    # вводим телефон и пароль
    form.username.send_keys('+79175862568')
    form.password.send_keys('fkvbkdjghbfj')
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TC-009 (авторизация по зарегистриванным почте и паролю)
def test_auth_reg_email(selenium):
    form = AuthForm(selenium)

    # вводим почту и пароль
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_password)
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# TC-010 (авторизация по незарегистрированным почте и паролю)
def test_auth_fake_email(selenium):
    form = AuthForm(selenium)

    # вводим почту и пароль
    form.username.send_keys('ljdneljwdvn@mail.ru')
    form.password.send_keys('ljfshjvelhfvfjhvjff')
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TC-011 (авторизация по зарегистриванным логину и паролю)
def test_auth_reg_login(selenium):
    form = AuthForm(selenium)

    # вводим логин и пароль
    form.username.send_keys(valid_login)
    form.password.send_keys(valid_password)
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    # связка Логин + Пароль считается некорректной из-за
    # использования пароля в этом тесте к номеру телефона,
    # который так же подходит и к почте, к тому же логин не
    # привязан ни к телефону, ни к почте, ни к лицевому счёту,
    #  поэтому этот тест - негативный
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TC-012 (авторизация по некорректному логину и корректному паролю)
def test_auth_fake_login(selenium):
    form = AuthForm(selenium)

    # вводим логин и пароль
    form.username.send_keys('abrakadabra')
    form.password.send_keys(valid_password)
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TC-013 (авторизация по корректному номеру лицевого счёта и корректному паролю)
def test_auth_reg_account(selenium):
    form = AuthForm(selenium)

    # вводим номер лицевого счёта и пароль
    form.username.send_keys(valid_account)
    form.password.send_keys(valid_password)
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    # связка Лицевой счёт + Пароль считается не корректной из-за
    # использования пароля в этом тесте к номеру телефона,
    # который так же подходит и к почте, к тому же лицевой счёт не
    # привязан ни к телефону, ни к почте, ни к логину,
    # поэтому этот тест - негативный
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TC-014 (авторизация по незарегистриванному лицевому счёту и незарегистрированному паролю)
def test_auth_fake_account(selenium):
    form = AuthForm(selenium)

    # вводим номер лицевого счёта и пароль
    form.username.send_keys('12345678')
    form.password.send_keys('оаоаоаоо')
    sleep(25) # на случай появления Captcha, вводим вручную
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TC-015 (открываем страницу авторизации по коду, создаем скриншот страницы)
def test_scr_page_code_form(selenium):
    form = CodeForm(selenium)
    form.driver.save_screenshot('02.jpg')


# TC-016 (авторизация по одноразовому паролю на номер телефона)
def test_auth_code(selenium):
    form = CodeForm(selenium)

    # ввод номера телефона
    form.address.send_keys(valid_number)

    sleep(25) # на случай появления Captcha, вводим вручную
    form.get_click()

    otc = form.driver.find_element(By.ID, 'rt-code-0')
    assert otc


# TC-020 (проверяем форму восстановления доступа)
def test_recovery(selenium):
    form = AuthForm(selenium)

    # нажимаем на кнопку "Забыл пароль"
    form.forgot.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


# TC-021 (проверяем форму регистрации)
def test_reg_form(selenium):
    form = AuthForm(selenium)

    # нажимаем на кнопку "Зарегистрироваться"
    form.register.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'


# TC-022 (проверяем доступность пользовательского соглашения)
def test_user_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # нажимаем на кнопку "Пользовательским соглашением" в футере страницы
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    title_page = form.driver.execute_script("return window.document.title")

    assert title_page == 'User agreement'


# TC-023 (проверяем возможность авторизации через социальную сеть Вконтакте)
def test_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(5)

    assert form.get_base_url() == 'id.vk.com'


# TC-024 (проверяем возможность авторизации через социальную сеть Одноклассники)
def test_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.ok.ru'


# TC-025 (проверяем возможность авторизации через портал mail.ru)
def test_auth_mail_ru(selenium):
    form = AuthForm(selenium)
    form.mail_ru_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.mail.ru'


# TC-026 (проверяем возможность авторизации через яндекс)
@pytest.mark.xfail(reason='Кнопка авторизации через яндекс в данном '
                          'автотесте не отрабатывает с первого раза')
def test_auth_yandex(selenium):
    form = AuthForm(selenium)
    form.yandex_btn.click()
    sleep(5)

    assert form.get_base_url() == 'passport.yandex.ru'
