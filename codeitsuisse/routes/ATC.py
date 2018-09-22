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
    back_count=0

    while (i<n):
        if("Distressed" in newlist[i] and newlist[i]["Distressed"]=="true"):
            #traceback RT, drop and add behind
            print('Trigger distress')
            for j in range(i-1,-1,-1):
                print(newlist[i]["Time"],newlist[j]["Time"])
                if(get_min(newlist[i]["Time"]) - get_min(newlist[j]["Time"]) < RT):
                    newlist[j]["Time"]=plusRT(newlist[i]["Time"],RT)
                    print("RTTTTT",newlist[j]["Time"])
                    tmp = newlist[j]
                    for runway in runways:
                        if(runway["name"]==newlist[j]["Runway"]):
                            runway["occupied"] = False
                            runway["release-time"] = "0000"
                    newlist[j] = newlist[i]
                    newlist[i] = tmp

                    back_count+=1
                    print('isnide')

            i=i-back_count

        print("i=",i)
        print(newlist[i])




        for runway in runways:
            # print(get_min(newlist[i]["Time"]) - get_min(runway["release-time"]))
            if(runway["occupied"] == True and (get_min(newlist[i]["Time"]) - get_min(runway["release-time"]) >= 0)):
                runway["occupied"] = False
                runway["release-time"] = "0000"

        if(not any([runway["occupied"]==False for runway in runways])):
            print("any!")
            min = 0
            for x in range(len(runways)-1):
                if get_min(runways[i]["release-time"]) < get_min(runways[min]["release-time"]):
                    min = x

            print("i=",i)
            newlist[i]["Time"] = runways[min]["release-time"]
            newlist[i]["Runway"] = runways[min]["name"]
            runways[min]["release-time"] = plusRT(runways[min]["release-time"],RT)

        for runway in runways:
            if(runway["occupied"] == False):
                runway["occupied"] = True
                runway["release-time"] = plusRT(newlist[i]["Time"],RT)
                newlist[i]["Runway"] = runway["name"]
                break

        i=i+1
        print(runways)
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
    if(len(h)==1):
        h = "0" + h
    if(len(m)==1):
        m = "0" + m

    return h+m

def plusRT(time_str,RT):
    min = get_min(time_str)
    min = min + RT
    return gen_timestr(min)
