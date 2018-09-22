import os
import logging
import sys
from flask import Flask
app = Flask(__name__)

import codeitsuisse.routes.square
import codeitsuisse.routes.primenumbers
<<<<<<< HEAD
import codeitsuisse.routes.tallyexpenses
=======
import codeitsuisse.routes.ATC
import codeitsuisse.routes.photogps
>>>>>>> c013081f9371b69206239442fd8fb8067aa21127

if 'DYNO' in os.environ:
    logFormatter = logging.Formatter("%(asctime)s [%(filename)s] [%(funcName)s] [%(lineno)d] [%(levelname)-5.5s]  %(message)s")
    specialHandler = logging.StreamHandler(sys.stdout)
    specialHandler.setFormatter(logFormatter)
    app.logger.addHandler(specialHandler)
    # app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)
