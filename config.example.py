
import os

# config for qBittorrent
os.environ['client_url']="http://IP:PORT/"
os.environ['client_uid']="USERNAME"
os.environ['client_pwd']="PASSWORD"
os.environ['client_pth']="/Series"

# config for utorrent running on docker host
#os.environ['client_url']="http://USER:PWD@host.docker.internal:8081/gui/"


# config for nCore
os.environ['tracker_uid']="USERNAME"
os.environ['tracker_pwd']="PASSWORD"
os.environ['tracker_url']="https://ncore.pro/torrents.php"