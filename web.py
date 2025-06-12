#!/usr/bin/python
from src.web import Webserver
from src.screenControls import ScreenControls
import main



Server = Webserver(ScreenControls.clearScreen, lambda: main.main(debug=True))

Server.start_server(80, 24, 80, 24)