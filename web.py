#!/usr/bin/python
from src.web import Webserver
import main



Server = Webserver(lambda: main.main(debug=False))

Server.start_server()
