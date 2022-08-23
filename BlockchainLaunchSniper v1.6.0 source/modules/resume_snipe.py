import json
import fileinput
import traceback
import os
from . import variables
from . import monitor_price
from . import token_details
from . import time_thread
from . import quit
from . import variables



def delSnipeState():
    try:
        os.remove(os.path.join("temp", (variables.chainName + "SnipeState.tmp")))
    except:
        pass


def initSnipeState():

    doesExist = os.path.exists(os.path.join("temp", (variables.chainName + "SnipeState.tmp")))

    if not doesExist:
        return True

    with open(os.path.join("temp", (variables.chainName + "SnipeState.tmp")), 'r+') as snipeState: #create file if not exists
        snipeState.seek(0)
        if snipeState.read() == "":
            pass
            snipeState.close()
            delSnipeState()
            return True
        else:
            return False
    

def completePreviousSnipe():
    with open(os.path.join("temp", (variables.chainName + "SnipeState.tmp")), 'r+') as snipeState:
        snipeState.seek(0)
        snipeStateString = snipeState.read()
        if snipeStateString != "":
            try:
                parameters = snipeStateString.split(',')
                variables.snipeTokenAddress = parameters[0]
                variables.liquidityPairAddress = parameters[1]
                variables.initialTokenPrice = float(parameters[2])
                if parameters[3] == "None":
                    variables.autoSellMultiplier = None
                else:
                    variables.autoSellMultiplier = float(parameters[3])

                snipeState.close()
                variables.tokenSymbol = token_details.getTokenSymbol(variables.snipeTokenAddress)
                monitor_price.manualMonitorAndSell()
            except:
                print(traceback.format_exc())
                print(variables.RESET + "[Error]    " + variables.RED + "Snipe state file is either incorrectly formatted or corrupted. Please edit/delete file and restart bot.")
                quit.quitSniper(True)
        

   
        


def writeSnipeState():
    current_directory = os.getcwd()
    temp_directory = os.path.join(current_directory, r'temp')
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

    with open(os.path.join("temp", (variables.chainName + "SnipeState.tmp")), 'w+') as snipeState:
        snipeState.seek(0)
        if snipeState.read() == "":
            if variables.autoSellMultiplier == None:
                pass

            if variables.enableTrailingStopLoss:
                snipeStateString = variables.snipeTokenAddress + "," + variables.liquidityPairAddress + "," + str(variables.initialTokenPrice) + ",1"

            else:
                snipeStateString = variables.snipeTokenAddress + "," + variables.liquidityPairAddress + "," + str(variables.initialTokenPrice) + "," + str(variables.autoSellMultiplier)

            snipeState.write(snipeStateString)
        snipeState.close()
