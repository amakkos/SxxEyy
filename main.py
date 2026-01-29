# python + selenium script to download torrent of next episode
#
# Supported torrent client:
#  - qBit torrent
#  - µTorrent
# Supported torrent tracker site:
#  - ncore (php - single run HTML build)

import os   # add selenium chromedriver to PATH

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from handler.common import step_episode
from selenium.webdriver.support.ui import WebDriverWait
import tempfile

# TODO cp config.examle.py config.py - and edit the file

# load modules
from handler.qBitTorrent import qBitLogin, qBitListEpisodes, qBitAdd
from handler.nCore import nCoreLogin, nCoreGetFile
from handler.utorrent import utorrent_list_episodes, utorrent_add
# torrent client handler functions, suppress IDE warning by pre-setting values
client_list = qBitListEpisodes
client_add = qBitAdd
# torrent server handler functions
tracker_get_file = nCoreGetFile

# service = Service(executable_path="chromedriver")
import config


###################################################
# opens URL, identifies SW
def login_torrent_client() -> WebDriver | None:
    global client_list
    global client_add

    print(f"login to torrent client site: {os.environ["client_url"]}")
    options = Options()
    options.add_argument("--headless=new")  # kötelező
    options.add_argument("--no-sandbox")  # kötelező Dockerben
    options.add_argument("--disable-dev-shm-usage")  # kötelező Dockerben
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    torrent_driver = webdriver.Chrome(options=options)
    # TODO exit if login failed
    torrent_driver.get(os.environ["client_url"])
    wait = WebDriverWait(torrent_driver, 5)

    try:
        wait.until(
            lambda d: (
                    d.find_elements(By.XPATH, "//meta[@name='description']")
                    or
                    d.find_elements(By.XPATH, "//img[@id='dlgAbout-logo']")
            )
        )
        # try to figure out what WebUI it is - qBit uses <meta name="description" content="qBittorrent WebUI">
        if torrent_driver.find_elements(By.XPATH, "//meta[@name='description']"):
            meta = torrent_driver.find_element(By.XPATH, "//meta[@name='description']")
            app_name = meta.get_attribute("content")
            print("  client:", app_name)
            if "qBittorrent" in app_name:
                client_list = qBitListEpisodes
                client_add = qBitAdd
                qBitLogin(torrent_driver)
                return torrent_driver

        if torrent_driver.find_elements(By.XPATH, "//img[@alt='uTorrent']"):
            print("  client: uTorrent")
            client_list = utorrent_list_episodes
            client_add = utorrent_add
            return torrent_driver

    except torrent_driver as ex:
        print("  can not identify torrent client")
        return None

    print("  can not identify torrent client")
    return None

###################################################
# opens URL, identifies SW
def login_torrent_tracker() -> WebDriver | None:
    global tracker_get_file

    print(f"login to torrent tracker site: {os.environ["tracker_url"]}")
    # set chrome for unattended download
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": tempfile.gettempdir(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
        },
    )
    tracker_driver: WebDriver = webdriver.Chrome(options=chrome_options)
    tracker_driver.get(os.environ["tracker_url"])
    meta = tracker_driver.find_element(By.XPATH, "//meta[@name='description']")
    app_name = meta.get_attribute("content")
    print("  tracker:",app_name)
    if app_name == "nCore":
        tracker_get_file = nCoreGetFile
        nCoreLogin(tracker_driver)

    return tracker_driver

###################################################
# start here
if __name__=="__main__":
    client_driver = login_torrent_client()          # login qBit/uTorrent torrent via WEB
    tracker_driver = login_torrent_tracker()        # logint to nCore

    thislist = client_list(client_driver)           # list the series episodes from active torrent view
    for torrent in thislist:
        next_episode: str = step_episode(torrent)
        if next_episode in thislist:
            print("already have ", next_episode)
        else:
            if tracker_get_file(tracker_driver, next_episode):
                client_add(client_driver, next_episode)