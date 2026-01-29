#
# module to handle nCore website
#

import os   # add selenium chromedriver to PATH
import time # yep, we must wait. There is no good way to check if AJAX has finished populating the torrent table
import re   # re.search is used to find SxxEyy pattern in torrent file name

from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .common import rename_download
from .common import wait_for_download
from .common import cleanup_download


###################################################
# Login to ncore web server
#
def nCoreLogin(ncore_driver: WebDriver) -> None:
    print(f"  Login as : {os.environ["tracker_uid"]}")

    name = ncore_driver.find_element(By.ID, "nev")
    name.send_keys(os.environ["tracker_uid"])

    pwd = ncore_driver.find_element(By.NAME, "pass")
    pwd.send_keys(os.environ["tracker_pwd"])

    submit = ncore_driver.find_element(By.CLASS_NAME, "submit_btn")
    submit.click()

    WebDriverWait(ncore_driver, 5).until(EC.presence_of_element_located((By.ID, "footer_bg")))

###################################################
# get torrent for next episode from nCore web page
def nCoreGetFile(ncore_driver: WebDriver, torrent: str) -> bool:
    print(f"  search in ncore for: {torrent}")

    wait = WebDriverWait(ncore_driver, 5)
    name = ncore_driver.find_element(By.ID, "mire")
    name.clear()
    name.send_keys(torrent)

    submit = ncore_driver.find_element(By.CLASS_NAME, "g_mehet")
    submit.click()

    try:
        wait.until(
            lambda d: (
                    d.find_elements(By.CSS_SELECTOR, "a[href*='torrents.php?action=details']")
                    or
                    d.find_elements(By.CSS_SELECTOR, ".lista_mini_error")
            )
        )
        if ncore_driver.find_elements(By.CSS_SELECTOR, ".lista_mini_error"):
            print("    not found")
            time.sleep(5)
            return False

    except TimeoutException as ex:
        print("    none found")
        return False

    # click to expand
    torrent_link = ncore_driver.find_element(By.XPATH, "//a[contains(@href,'torrents.php?action=details')]")
    torrent_link.click()

    download_link = WebDriverWait(ncore_driver, 5).until(
        EC.element_to_be_clickable(
            (
                By.LINK_TEXT,
                "Letöltés"
            )
        )
    )
    # download torrent
    cleanup_download(torrent)
    download_link.click()
    wait_for_download(torrent)
    rename_download(torrent)
    return True