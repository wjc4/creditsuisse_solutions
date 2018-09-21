import os
import logging
import sys
from flask import Flask
app = Flask(__name__)

import codeitsuisse.routes.square

if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)
