import time
from fileinput import close
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selen_utils import close_modal, login_btn_press, from_sms, take_screenshot_modal

# Создание объекта ChromeOptions для дополнительных настроек браузера
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--no-sandbox')
# options_chrome.add_argument('--headless')
options_chrome.add_argument('--disable-dev-shm-usage')

with webdriver.Chrome(options=options_chrome) as browser:
    # Открытие сайта в браузере
    browser.get("https://openbudget.uz/boards/initiatives/initiative/52/93d0a0c6-95c7-47f9-b8c7-0e0406fe3329")

    element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "vote-wrapper"))).click()

    # if close_modal(browser):
    #     browser.save_screenshot("page.png")
    #
    # if login_btn_press(browser):
    #     browser.save_screenshot("login.png")
    #
    # login_field = browser.find_element(By.ID, "phone-number")
    # login_field.click()
    #
    # login_field.send_keys("934343242")
    from_sms(browser)
    take_screenshot_modal(browser)


    browser.save_screenshot("ins_number.png")

    # # element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "vote-wrapper"))).click()
    # time.sleep(30)
    #
    #
    # # close_modal_window_btn = browser.find_element(By.CSS_SELECTOR, "#app > div.main-view > div.main-container > div > div.mf-modal.show.modal > div.mf-modal-content.md > button")
    # # time.sleep(1)
    # # close_modal_window_btn.click()
    #
    # button_login = browser.find_element(By.CSS_SELECTOR,
    #                                    "#app > div.main-view > div.normal-header.top-header > div.top-header-wrapper > button.mf-button.mf-button-light.sign-in")
    # time.sleep(3)
    # button_login.click()
    #
    # # print(text.text)

    # browser.save_screenshot("page.png")

    # soup = BeautifulSoup(browser.page_source,  'lxml')
    # headings = soup.find('div',  {'class': 'elementor-heading-title'})
    # time.sleep(10)
    # for heading in headings:
    #     print(heading.getText())
