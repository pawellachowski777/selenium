from config import *
from AFO_selenium import *
from password import *

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import sys
import time


# ustawienie domyślnnego folderu pobierania
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": directory}
chrome_options.add_experimental_option("prefs", prefs)

# ustawienie pozostawienia przeglądarki otwartej po zakończeniu wyszukiwania
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get('https://online.focusmr.com/ActionFocusOnline/main.iface')

try:
    # logowanie
    login_pass = driver.find_element(by='id', value=login_html)
    login_pass.send_keys(login)

    password_pass = driver.find_element(by='id', value=password_html)
    password_pass.send_keys(password)

    click_with_wait(driver=driver, wait_time=10, find_by=By.ID, button_html=remember_me_button_html)
    click_with_wait(driver=driver, wait_time=10, find_by=By.ID, button_html=login_button_html)

    # pobieranie
    driver.get(link)
    time.sleep(1)

    # podanie daty od i do
    date_from_pass = driver.find_element(by='id', value=date_from_html)
    date_from_pass.clear()
    date_from_pass.send_keys(date_from)

    date_to_pass = driver.find_element(by='id', value=date_to_html)
    date_to_pass.clear()
    date_to_pass.send_keys(date_to)

    # anulowanie starego wyszukiwania
    click_with_wait(driver=driver, wait_time=10, find_by=By.ID, button_html=cancel_button_html)

    click_with_wait(driver=driver, wait_time=10, find_by=By.ID, button_html=search_button_html, sleep_time=3)

    # przed pobraniem trzeba zaczekac na zakonczneie wyszukiwania
    wait_for_bar = WebDriverWait(driver, 60).until(
            ec.presence_of_element_located((By.ID, search_bar_html))
        )
    time.sleep(1)

    # pobranie PDF
    click_with_wait(driver=driver, wait_time=10, find_by=By.ID, button_html=download_button_html)
    click_with_wait(driver=driver, wait_time=10, find_by=By.ID, button_html=download_pdf_html)
    download_wait(directory)

    # zzipowanie, usuniecie starych plikow, wrzucenie na IT
    rename_and_zip(directory, file_name, '.pdf')
    remove_files(directory, '*.zip', 4)
    remove_files(directory, '*.pdf', 1)
    copy_to_it(directory, file_name, directory_it)

    driver.quit()

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(e, "/n", exc_type, exc_tb.tb_lineno)
    driver.quit()
