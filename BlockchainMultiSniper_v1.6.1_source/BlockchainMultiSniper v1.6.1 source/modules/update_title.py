import sys
import ctypes
import traceback
import os
from . import debug
from . import variables
#import time


def updateTitle():
    walletBalance = None
    variables.walletBalance = None
    titleString = None

    try:
        extraWalletBalances = ""
        if not variables.useSingleLiquidityPair:
            for i in range(len(variables.liquidityPairs)):
                if variables.liquidityPairs[i]["symbol"] != variables.chainCurrencySymbol:
                    print(variables.liquidityPairs[i]["symbol"] + " | " + variables.chainCurrencySymbol)
                    liquidityPairAddress = variables.liquidityPairs[i]["liquidityPairAddress"]
                    sellTokenContract = variables.web3.eth.contract(address=liquidityPairAddress, abi=variables.sellABI)
                    balance = round(float(variables.web3.fromWei(sellTokenContract.functions.balanceOf(variables.walletAddress).call(), "ether")), 5)

                    extraWalletBalances += " | " + str(balance) + " " + variables.liquidityPairs[i]['symbol']

        walletBalance = variables.web3.eth.get_balance(variables.walletAddress)
        walletBalance = variables.web3.fromWei(walletBalance, 'ether') #There are references to ether in the code but it's set to BNB, its just how Web3 was originally designed
        variables.walletBalance = round(walletBalance, -(int("{:e}".format(walletBalance).split('e')[1]) - 4)) #the number '4' is the wallet balance significant figures + 1, so shows 5 sig figs

        numTokensQueued = sum(1 for line in open((os.path.join("temp", (variables.chainName + 'TokenCache.csv')))))

        titleString = variables.chainName + "MultiSniper " + variables.versionNumber + " | Tokens Detected: " + str(variables.numTokensDetected) + \
                        " | Tokens Bought: " + str(variables.numTokensBought) + " | Tokens Queued: " + str(numTokensQueued) + " | Tokens Sold: " + str(variables.numTokensSold) + \
                        " | Wallet Balance: " + str(variables.walletBalance) + " " + variables.chainCurrencySymbol + extraWalletBalances
        if(sys.platform == "win32"): #if os is windows
            ctypes.windll.kernel32.SetConsoleTitleW(titleString)
        else:
            print(titleString)
    except:
        debug.handleError(traceback.format_exc(), "updateTitleMain")
        updateTitle()
