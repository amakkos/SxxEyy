#
# module to handle µTorrent WebUI
#   tested by 3.6 (build 47224)

import re  # re.search is used to find SxxEyy pattern in torrent file name
import os  # add selenium chromedriver to PATH
import time

from typing import Any
import tempfile

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def utorrent_list_episodes(driver: WebDriver) -> list[Any]:
    torrent_list: list[Any] = []  # list of episode of series - having like S02E03 in name
    pattern = re.compile("[sS][0-9][0-9][eE][0-9][0-9]")

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "tr[id^='stable-mainTorList-row-'][title]"
    )

    for row in rows:
        title = row.get_attribute("title")
        if pattern.search(title):
            torrent_list.append(title)

    torrent_list.sort()
    for item in torrent_list:
        print("  ",item)
    return torrent_list


def utorrent_add(driver: WebDriver, torrent_file: str) -> None:
    add = driver.find_element(By.CSS_SELECTOR,"a[id='add']")
    add.click()

    file_input = driver.find_element(By.ID, "dlgAdd-file")
    file_input.send_keys(os.path.join(tempfile.gettempdir(), torrent_file + ".torrent"))

    driver.find_element(By.ID, "ADD_FILE_OK").click()
    time.sleep(5)


