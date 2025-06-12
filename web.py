#!/usr/bin/python
from src.web import Webserver
import main



Server = Webserver(lambda: main.main(debug=True))

Server.start_server()
