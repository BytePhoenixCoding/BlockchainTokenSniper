import datetime
import time

currentTimeStamp = ""

def getTimestamp():
    global currentTimeStamp

    while True:
        timeStampData = datetime.datetime.now()
        currentTimeStamp = "[" + timeStampData.strftime("%H:%M:%S.%f")[:-3] + "]"
        time.sleep(0.01) #small delay to not throttle CPU

