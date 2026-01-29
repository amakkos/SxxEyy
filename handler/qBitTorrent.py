#
# module to handle qBittorrent WebUI
#   tested by v5.1.2 (64 bit)
#

import os  # add selenium chromedriver to PATH
import time  # yep, we must wait. There is no good way to check if AJAX has finished populating the torrent table
import re  # re.search is used to find SxxEyy pattern in torrent file name
import tempfile

from typing import Any

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ['PATH'] += "/home/makki/Downloads/chromedriver-linux64"

def qBitLogin(driver: WebDriver):
    name = driver.find_element(By.ID, "username")
    name.clear()
    name.send_keys(os.environ["client_uid"])

    pwd = driver.find_element(By.ID, "password")
    pwd.clear()
    pwd.send_keys(os.environ["client_pwd"])

    submit = driver.find_element(By.ID, "loginButton")
    submit.click()

    # wait for the footer to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "freeSpaceOnDisk")))
    # TODO exit if login failed

    # wait for page is loading REST
    time.sleep(2.5)


###################################################
# List episodes like S01E02 from qBitTorrent web page
# Do not 'yield' here, the caller has to have the full ist to see if 'next' is already downloaded
#
def qBitListEpisodes(driver: WebDriver) -> list[Any]:
    thislist: list[Any] = []  # list of episode of series - having like S02E03 in name

    div_id = driver.find_element(By.ID, 'torrentsTableDiv')

    rows = div_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
    pattern = re.compile("[sS][0-9][0-9][eE][0-9][0-9]")
    for row in rows:
        # Get the columns (all the column 2)
        cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
        for col in cols:
            if pattern.search(col.text):
                print(col.text)  # prints text from the element
                thislist.append(col.text)

    thislist.sort()
    return thislist

###################################################
# upload torrent file to qBitTorrent
def qBitAdd(driver: WebDriver, torrent_file: str) -> None:
    driver.find_element(By.ID, "uploadButton").click()

    iframe = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "uploadPage_iframe")
    )

    driver.switch_to.frame(iframe)
    file_input = WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.querySelector(\"input[type='file']\");"
        )
    )

    file_input.send_keys(os.path.join(tempfile.gettempdir(), torrent_file + ".torrent"))

    if "client_pth" in os.environ:
        savepath = driver.find_element(By.ID, "savepath")
        savepath.clear()
        savepath.send_keys(os.environ["client_pth"])

    driver.find_element(
        By.CSS_SELECTOR,
        "#submitbutton button"
    ).click()
    time.sleep(10)
    driver.switch_to.default_content()