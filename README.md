# SxxEyy
The name stands for series/epizode mapping in torrent names.  
This is a python+selenium tool to automate getting new episodes
  
<u>Supported clients:</u>
- qBittorrent - tested by v5.1.2 (64 bit)
- µTorrent - tested by 3.6 (build 47224) 
  
<u>Supported tracker site:</u>
- nCore

## Features
- Lists episodes from your torrent client 
- Looks for next episode in tracker web site
- Downloads and adds them if any was found

## Hint
- Keep the last episode in your client, so the script can find it. Older episodes can be deleted of course.
- Activate WebUI in torrent client


## How to configure
When using docker, just update URL, user and password in docker compose yaml file. I think you can copy those from your browser.  
Note: uTorrent still uses old basic http auth, so use `http://{USER}:{PASSWD}@{IP}:{PORT}/gui/` as URL.   
Note: If you use utorrent/qBittorent on your machine and want to run that in container, `127.0.0.1` will not work. Use host.docker.internal to access your docker host.   
When running python instead, just set those variables in environment. In this case you can use `127.0.0.1` in URL. 

## Setup and run docker
```
[adamm@DESKTOP-C6MFFLN:/g/src/SxxEyy]$ cp config.example.py config.py
```
Update config.py: add your IP/host, user and password
```
[adamm@DESKTOP-C6MFFLN:/g/src/SxxEyy]$ docker build --no-cache -t selenium-app .
...
[adamm@DESKTOP-C6MFFLN:/g/src/SxxEyy]$ docker compose up --build 
...
 Container sxxeyy-selenium-app-1  Recreate
 Container sxxeyy-selenium-app-1  Recreated
Attaching to selenium-app-1
selenium-app-1  | login to torrent client site: http://192.168.1.91:8081/
selenium-app-1  |   client: qBittorrent WebUI
selenium-app-1  | login to torrent tracker site: https://ncore.pro/torrents.php
selenium-app-1  |   tracker: nCore
selenium-app-1  |   Login as : xxxxxx
selenium-app-1  | Fallout.S02E06.720p.AMZN.WEB-DL.DDP5.1.Atmos.H.264.HUN.ENG-PTHD
selenium-app-1  | Star.Trek.Starfleet.Academy.S01E03.1080p.WEB.h264-ETHEL
selenium-app-1  |   search in ncore for: Fallout.S02E07.720p.AMZN.WEB-DL.DDP5.1.Atmos.H.264.HUN.ENG-PTHD
selenium-app-1  |     download finished  [nCore][hdser_hun]Fallout.S02E07.720p.AMZN.WEB-DL.DDP5.1.Atmos.H.264.HUN.ENG-PTHD.torrent
selenium-app-1  |     renamed torrent: Fallout.S02E07.720p.AMZN.WEB-DL.DDP5.1.Atmos.H.264.HUN.ENG-PTHD.torrent
selenium-app-1  |   search in ncore for: Star.Trek.Starfleet.Academy.S01E04.1080p.WEB.h264-ETHEL
selenium-app-1  |     waiting  [nCore][hdser]Star.Trek.Starfleet.Academy.S01E04.1080p.WEB.h264-ETHEL.torrent.crdownload
selenium-app-1  |     download finished  [nCore][hdser]Star.Trek.Starfleet.Academy.S01E04.1080p.WEB.h264-ETHEL.torrent
selenium-app-1  |     renamed torrent: Star.Trek.Starfleet.Academy.S01E04.1080p.WEB.h264-ETHEL.torrent
selenium-app-1 exited with code 0

[adamm@DESKTOP-C6MFFLN:/g/src/SxxEyy]$ 
```

## Schedule
On windows use Task Scheduler (taskschd.msc) on linux use crontab. Make sure you entered that directory so docker-compose can find the yaml file.  
Also Kubernetes can be used if already have. 

## Debug
Check console if having problem. 

## License
2026-amakkos

SxxEyy is licensed under a 2-clause BSD license.  
You can use, alter and re-distribute.  
Please show this original git URL when distribute.  
