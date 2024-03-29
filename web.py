#!/usr/bin/python
from src.web import Webserver
from src.screenControls import ScreenControls

Server = Webserver(ScreenControls.clearScreen)

Server.start_server(80, 24, 80, 24)