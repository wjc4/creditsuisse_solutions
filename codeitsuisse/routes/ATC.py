import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/airtrafficcontroller', methods=['POST'])
def evaluate_ATC():

    # JSON mode
    data = request.get_json();
    app.logger.info("data sent for evaluation {}".format(data))

    # To return a new list, use the sorted() built-in function...
    newlist = sorted(data["Flights"], key=lambda x: (x["Time"],x["PlaneId"]))

    RT = int(int(data["Static"]["ReserveTime"])/60)

    if "Runways" not in data["Static"]:
        for i in range(len(newlist)):
            if(i!=0 and (get_min(newlist[i]["Time"])-get_min(newlist[i-1]["Time"])<=RT)):
                newlist[i]["Time"]=plusRT(newlist[i-1]["Time"],RT)
            i=i+1

        result = {"Flights":newlist}
        app.logger.info("My result :{}".format(result))

        return jsonify(result);

    print(newlist)

    delay = 0
    runway_names = data["Static"]["Runways"]
    runway_names.sort()
    runways = [{"name":"A","occupied":False,"release-time":"0000"}]*len(runway_names)
    for i in range(len(runway_names)):
        runways[i] = {}
        runways[i]["name"] = runway_names[i]
        runways[i]["occupied"] = False
        runways[i]["release-time"] = "0000"

    # by default assign all A runways
    i=0
    n = len(newlist)

    for i in range(n):
        for runway in runways:
            # print(RT)
            print(get_min(newlist[i]["Time"]) - get_min(runway["release-time"]))
            if(runway["occupied"] == True and (get_min(newlist[i]["Time"]) - get_min(runway["release-time"]) >= 0)):
                runway["occupied"] = False
                runway["release-time"] = "0000"
            print(runways)
        # if(i!=0 & getmin(newlist[i]["Time"]) - getmin(newlist[i-1]["Time"]) < ReserveTime):
        #     for

        for runway in runways:
            if(runway["occupied"] == False):
                runway["occupied"] = True
                runway["release-time"] = plusRT(newlist[i]["Time"],RT)
                # print(newlist[i]["Time"],runway["release-time"])
                newlist[i]["Runway"] = runway["name"]
                break

            # newlist[i]["Time"] = plus10(newlist[i-1]["Time"])

    # Args Key Mode
    # data = request.args
    # inputValue = int(data.get('input'))

    result = {"Flights":newlist}
    app.logger.info("My result :{}".format(result))

    return jsonify(result);

def get_min(time_str):
    h = time_str[0:2]
    m = time_str[2:4]
    return int(h) * 60 + int(m)

def gen_timestr(min):
    h = str(int(min/60))
    m = str(min - int(h) * 60)

    print(h,m)
    if(len(h)==1):
        h = "0" + h
    if(len(m)==1):
        m = "0" + m

    return h+m

def plusRT(time_str,RT):
    min = get_min(time_str)
    min = min + RT
    print("plusRT",min,RT)
    return gen_timestr(min)
