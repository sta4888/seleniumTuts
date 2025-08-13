# Импорт модуля webdriver из библиотеки Selenium для управления браузером
from selenium import webdriver

# Импорт модуля time для работы с задержками
import time

# Создание экземпляра webdriver браузера Chrome
browser = webdriver.Chrome()

# Открытие сайта "stepik.org" в браузере
browser.get("http://stepik.org/104774")

# Пауза на 5 секунд, чтобы страница успела загрузиться
time.sleep(5)

# Закрытие браузера
browser.quit()