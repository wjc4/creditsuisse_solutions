import os
import logging
import sys
from flask import Flask
app = Flask(__name__)

import codeitsuisse.routes.square
import codeitsuisse.routes.primenumbers
import codeitsuisse.routes.tally
import codeitsuisse.routes.ATC
import codeitsuisse.routes.photogps
import codeitsuisse.routes.hotel
import codeitsuisse.routes.puzzle
import codeitsuisse.routes.broadcastmessage
import codeitsuisse.routes.broadcastconnected

if 'DYNO' in os.environ:
    logFormatter = logging.Formatter("%(asctime)s [%(filename)s] [%(funcName)s] [%(lineno)d] [%(levelname)-5.5s]  %(message)s")
    specialHandler = logging.StreamHandler(sys.stdout)
    specialHandler.setFormatter(logFormatter)
    app.logger.addHandler(specialHandler)
    # app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)
