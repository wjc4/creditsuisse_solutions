import logging
import os
from codeitsuisse import app
# logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def default_route():
    app.logger.info("base url requested. saying hello")
    return "Team XYZ page. Hello"

if __name__ == "__main__":
    if 'DYNO' not in os.environ:   
        logFormatter = logging.Formatter("%(asctime)s [%(filename)s] [%(funcName)s] [%(lineno)d] [%(levelname)-5.5s]  %(message)s")
        rootLogger = logging.getLogger()

        rootLogger.setLevel(logging.INFO)

        fileHandler = logging.FileHandler("team.log")
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

        # logger.info("Starting application ...")
    app.run()
    # app.run(debug=True)

