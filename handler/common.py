#
# Common tools for torrent file download, rename
#

import os
import time
import re
import tempfile

###################################################
# wait until chrome finishes the download and renames the file
def wait_for_download(torrent_file: str, timeout=30):
    seconds = 0
    while seconds < timeout:
        files = os.listdir(tempfile.gettempdir())
        for f in files:
            if torrent_file in f:
                if f.endswith(".crdownload"):
                    print("    waiting ", f)
                    time.sleep(1)
                elif f.endswith(".torrent"):
                    print("    download finished ", f)
                    return True
    return False

###################################################
# delete old torrent file before download
def cleanup_download(torrent_file: str):
    for f in os.listdir(tempfile.gettempdir()):
        if torrent_file in f and f.endswith(".torrent"):
            print("    delete torrent:", f)
            os.remove(os.path.join(tempfile.gettempdir(),f))

###################################################
# delete leading [] from file name
def rename_download(torrent_file: str):
    for f in os.listdir(tempfile.gettempdir()):
        if torrent_file in f and f.endswith(".torrent"):
            new_name = re.sub(r'^(\[[^\]]+\])+', '', f)
            print("    renamed torrent:", new_name)
            os.rename(
                os.path.join(tempfile.gettempdir(), f),
                os.path.join(tempfile.gettempdir(), new_name)
            )

###################################################
# increases episode counter in file name like S01E01 -> S01E02
def step_episode(filename: str) -> str:
    pattern = r"(S(\d{2})E(\d{2}))"

    match = re.search(pattern, filename)
    if not match:
        raise ValueError("    Can not find SxxEyy in name")

    full, season, episode = match.groups()
    season_num = int(season)
    episode_num = int(episode) + 1

    new_ep = f"S{season_num:02d}E{episode_num:02d}"
    return filename.replace(full, new_ep, 1)
