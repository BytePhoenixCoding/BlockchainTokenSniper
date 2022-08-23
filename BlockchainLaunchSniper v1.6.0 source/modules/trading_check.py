from web3 import Web3
from . import variables
import requests
from . import time_thread
import json
from . import debug
import traceback
import time


checkHoneypotContract = None

def initHoneypotContract():
    global checkHoneypotContract
    try:
        honeypotContractAddress = Web3.toChecksumAddress(variables.honeypotCheckerAddress)
        checkHoneypotContract = variables.web3.eth.contract(address=honeypotContractAddress, abi=variables.tradingABI)
        pass
    except:
        print(traceback.format_exc())
         
def honeypotCheck(tokenAddress):
    tokenAddress = Web3.toChecksumAddress(tokenAddress)
    #print(tokenAddress)
    try:
        global checkHoneypotContract
        tokenInfo = checkHoneypotContract.functions.buy(variables.liquidityPairAddress, tokenAddress).call({"value": Web3.toWei(variables.tokenSnipeAmount, 'ether') })
        buy_tax = round((tokenInfo[0] - tokenInfo[1]) / tokenInfo[0] * 100)
        sell_tax = round((tokenInfo[3] - tokenInfo[4]) / tokenInfo[3] * 100)

        return False, buy_tax, sell_tax
    except:
        del tokenAddress
        return True, 101, 101
    
def repeatHoneypotCheck(tokenAddress):
    honeypotOK = False
    if(variables.honeypotCheck == True):
        print(variables.RESET + time_thread.currentTimeStamp + " [Trading]  " + variables.YELLOW + "Checking honeypot status...")
        isHoneypot, buyFee, sellFee = honeypotCheck(tokenAddress) #first time, so don't display anything
        if isHoneypot or buyFee > variables.honeypot_maxBuyFee or sellFee > variables.honeypot_maxSellFee:
            print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Token is currently a honeypot / antibot enabled, waiting until trading is enabled...")
            while isHoneypot or buyFee > variables.honeypot_maxBuyFee or sellFee > variables.honeypot_maxSellFee:
                isHoneypot, buyFee, sellFee = honeypotCheck(tokenAddress)
                if buyFee < 101 and sellFee < 101:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Trading]  " + variables.YELLOW + "Status: " + str(isHoneypot) + " | Buy Fee: " + str(buyFee) + "% | Sell Fee: " + str(sellFee) + "%")
                else:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Trading]  " + variables.YELLOW + "No liquidity available / trading not enabled yet...") #debug.handleError(traceback.format_exc(), "honeypotCheckMain")       

            honeypotOK = True
            print(variables.RESET + time_thread.currentTimeStamp + " [Trading]  " + variables.GREEN + "Honeypot pass, trading is enabled...")
        print(variables.RESET + time_thread.currentTimeStamp + " [Trading]  " + variables.GREEN + "Honeypot check OK.")
        print("")
    else:
        honeypotOK = True #dont check for honeypot, just set to true
