from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import glob
import os
from zipfile import ZipFile
import shutil
import time

# logowanie
login_html = 'mainForm:mainNavPanelTabSet:0:loginUserName'
password_html = 'mainForm:mainNavPanelTabSet:0:loginPassword'
remember_me_button_html = 'mainForm:mainNavPanelTabSet:0:loginRememberMe'
login_button_html = 'mainForm:mainNavPanelTabSet:0:loginLoginButtonText'

# pobieranie
date_from_html = 'mainForm:mainNavPanelTabSet:0:searchesPanelTabSet:0:priceSearchDateFromInput'
date_to_html = 'mainForm:mainNavPanelTabSet:0:searchesPanelTabSet:0:priceSearchDateToInput'

cancel_button_html = 'mainForm:mainNavPanelTabSet:0:searchesPanelTabSet:0:priceSearchProgressBarbar'
search_button_html = 'mainForm:mainNavPanelTabSet:0:searchesPanelTabSet:0:priceSearchSearchButtonText'
search_bar_html = 'mainForm:mainNavPanelTabSet:0:searchesPanelTabSet:0:priceSearchGalleryResultGridPagerAbove'

download_button_html = 'mainForm:j_id96'
download_pdf_html = 'mainForm:j_id1893'


# uniwersalne funkcje


def click_with_wait(driver, wait_time, find_by, button_html, sleep_time=1):
    """
    :param driver selenium webdriver object
    :param wait_time: how many seconds wait for the appearance of the button
    :param find_by: By.ID, By.CLASS_NAME
    :param button_html: place in HTML, imported from the config.py file
    :param sleep_time: seconds to wait after click
    """
    wait = WebDriverWait(driver, wait_time).until(
        ec.presence_of_element_located((find_by, button_html))
    )
    wait.click()
    time.sleep(sleep_time)


def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    number_of_files = len(os.listdir(path_to_downloads))
    # czeka max 10 min. na pobieranie z AFO
    while dl_wait and seconds < 600:
        time.sleep(1)
        dl_wait = False
        current_number_of_files = len(os.listdir(path_to_downloads))
        for fname in os.listdir(path_to_downloads):
            # plik tymczasowy .crdownload nie powstanie zanim strona nie rozpocznie pobierania, dlatego trzeba sprawdzić
            # czy w folderze mamy nowy plik. Jeśli nie mamy nowego pliku czekamy
            if '.crdownload' not in os.listdir(path_to_downloads) and number_of_files == current_number_of_files:
                dl_wait = True
            # czekamy aż plik tymczasowy zostanie pobrany
            if fname.endswith('.crdownload') or fname.endswith('.tmp'):
                dl_wait = True
        seconds += 1
    return seconds


def rename_and_zip(project_directory: str, current_file_name: str, file_extension: str):
    """
    :param project_directory: project directory form the config
    :param current_file_name:  file name form the config
    :param file_extension:  file extension
    :return:
    """
    # znalenienie pobranego pliku
    list_of_files = glob.glob(os.path.join(project_directory, r'*.pdf'))
    latest_file = max(list_of_files, key=os.path.getctime)

    # zmiana nazwy
    latest_file_new_name = os.path.join(project_directory, current_file_name)
    latest_file_new_name_extension = os.path.join(project_directory, current_file_name) + file_extension
    try:
        os.rename(latest_file, latest_file_new_name_extension)
    # jeśli plik o tej samej nazwie isnieje, usuwa go i toworzy nowy
    except FileExistsError:
        os.remove(latest_file_new_name_extension)
        os.rename(latest_file, latest_file_new_name_extension)
        print(f"Zastąpiono plik {latest_file_new_name_extension}")

    # zip
    with ZipFile(latest_file_new_name + ".zip", "w") as new_zip:
        new_zip.write(
            filename=latest_file_new_name_extension,
            arcname=current_file_name + file_extension
        )


def remove_files(project_directory, file_extension, staying_amount):
    """
    :param project_directory: project directory form the config file
    :type project_directory: str
    :param file_extension: file extension which we want to remove, e.g. write '*.zip' to search for all zip files in
    a directory
    :type file_extension: str
    :param staying_amount: how many files is going to stay in a directory
    :type staying_amount: int
    """

    remove = True
    while remove:
        remove = False
        list_of_files = glob.glob(os.path.join(project_directory, file_extension))
        sorted_list_of_files = sorted(list_of_files, key=os.path.getmtime)
        if len(sorted_list_of_files) > staying_amount:
            os.remove(sorted_list_of_files[0])
            remove = True


def copy_to_it(project_directory, current_file_name, it_directory):
    """
    :param project_directory: project directory form the config file
    :type project_directory: str
    :param current_file_name:  file name form the config file
    :type project_directory: str
    :param it_directory: it directory form the config file
    :type project_directory: str
    """
    full_path = os.path.join(project_directory, current_file_name + ".zip")
    shutil.copy(full_path, it_directory)
