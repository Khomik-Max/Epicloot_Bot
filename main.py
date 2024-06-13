from browser import BrowserController
import configparser

# Чтение настроек из файла конфигурации
config = configparser.ConfigParser()
config.read('config.ini')

# Получаем информацию о режиме работы
# mode = 0 Режим сбора бесплатных попыток
# mode = 1 Режим сбора и автоматической игры
mode = config['mode']['mode']
url = config['mode']['url']

browser = BrowserController(url)
def main():

    try:
        browser.add_cookie()
        if mode == '0':
            while True:
                browser.get_gift()
        elif mode == '1':
            while True:
                browser.game_actions()
                browser.get_gift()
        else:
            print("Неверный настройки файла config.ini")

    except Exception as e:
        print(e)
    finally:
        browser.br_exit()


if __name__ == '__main__':
    main()
