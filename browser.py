from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import random
import logging
import os

class BrowserController():
    browser = None
    wait = None

    def __init__(self, url):
        # Инициализация объекта логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Определение обработчика логирования для записи в файл
        handler = logging.FileHandler('logs.txt', mode='w')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Инициализация браузера
        self.logger.info('Initializing BrowserController')
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-extensions-file-access-check")
        options.add_argument("--disable-extensions-http-throttling")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-web-security")

        script_dir = os.path.dirname(__file__)
        profile_dir = os.path.join(script_dir, 'Profile')
        options.add_argument(f"user-data-dir={profile_dir}")
        options.add_argument("profile-directory=Default")

        binary_yandex_driver_file = 'yandexdriver.exe'

        service = webdriver.ChromeService(executable_path=binary_yandex_driver_file)

        self.browser = webdriver.Chrome(service=service, options=options)

        # Максимизация окна браузера и переход по указанному URL
        self.browser.maximize_window()
        self.browser.get(url)

        # Инициализация объекта ожидания элементов
        self.wait = WebDriverWait(self.browser, 60)

        # Добавление cookie
        self.add_cookie()

    def add_cookie(self):
        # Загрузка cookie из файла JSON
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
        try:
            # Добавление каждого cookie в браузер
            for cookie in cookies:
                self.browser.add_cookie({"name": cookie["name"], "value": cookie["value"]})
            self.logger.info('Adding cookies')
            self.browser.refresh()
        except Exception as ex:
            self.logger.error('Error adding cookies: %s', ex)

    def get_gift(self):
        try:
            # Попытка получить подарок
            but_get_map = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="battle"]/div[6]/div[2]/div[2]/div[3]/div[1]/span')))
            but_get_map.click()
            print('Получена бесплатная попытка!')
            self.logger.info('Getting gift')
        except Exception as ex:
            print('Получение бесплатной попытки недоступно. Ждем 1 минуту.')
            self.logger.error('Error getting gift: %s', ex)

    def game_actions(self):
        try:
            # Получение количества доступных игр
            total_map = self.browser.find_element(By.XPATH, '//*[@id="startGameBtn"]/div[2]/span')
            if int(total_map.text) >= 1:
                # Проведение указанного числа игр
                for _ in range(int(total_map.text)):
                    self.logger.info('Starting game')
                    # Запуск игры
                    but_game = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="startGameBtn"]')))
                    but_game.click()

                    self.logger.info('Choosing side')
                    # Выбор стороны, за которую будет играть
                    but_cm = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="battle"]/div[6]/div[3]/div[2]/div[2]')))
                    but_cm.click()

                    self.logger.info('Choosing line')
                    # Выбор линии для движения
                    for _ in range(3):
                        for i in range(3):
                            wait_move = self.wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="battle"]/div[6]/div[7]/div[2]/div/div[1]'), 'Выбери путь!'))
                            box = self.browser.find_element(By.XPATH, f'//*[@id="battle"]/div[6]/div[7]/div[3]/div[4]/div/div[{i+1}]/div[{random.randint(1, 3)}]')
                            box.click()
                            time.sleep(1.5)

                    self.logger.info('Clicking next')
                    # Нажатие на кнопку "Продолжить"
                    but_next = self.wait.until(EC.any_of(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="battle"]/div[4]/div[4]/button')),
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="battle"]/div[5]/div[5]/button[1]'))
                    ))
                    but_next.click()
        except Exception as ex:
            self.logger.error('Error during game: %s', ex)
            print('Во время игры произошла ошибка:')
            print(ex)

    def br_exit(self):
        # Закрытие браузера
        self.browser.close()
        self.browser.quit()