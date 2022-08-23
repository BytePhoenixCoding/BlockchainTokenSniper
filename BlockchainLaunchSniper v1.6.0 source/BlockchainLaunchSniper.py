import os
import sys
import ctypes

versionNumber = "v1.6.0"
backendFolder = "backend"

#os.system("mode con: lines=32766")
os.system("")

print("Loading...")

try:
    from web3 import Web3
except:
    print("[Error] Web3 not installed or incorrectly configured. Please resolve the issue and restart bot.")
    input()
    quit()
    exit()

import datetime
import threading
import json
import asyncio
import requests
import time
import traceback
import webbrowser
import warnings
import ssl
import urllib3
from web3.auto import w3
from eth_account.messages import encode_defunct

from modules import variables
from modules import connect_to_node
from modules import debug
from modules import init_nonce
from modules import quit
from modules import setup_hotkeys
from modules import time_thread
from modules import buy_token
from modules import token_details
from modules import resume_snipe
from modules import trading_check
from modules import monitor_price
from modules import snipe_miner
from modules import check_authorisation

variables.init()

urllib3.disable_warnings()

timeStampThread = threading.Thread(target=time_thread.getTimestamp, )
timeStampThread.start()  
connect_to_node.initNode(True)

sys.setrecursionlimit(10**6)

if(sys.platform == "win32"): #if os is windows
    ctypes.windll.kernel32.SetConsoleTitleW((variables.chainName + "LaunchSniper " + versionNumber))
    os.system("mode con: lines=32766")
    os.system("")
else: #if OS is not windows eg. mac, linux
    #sys.stdout.write(("BlockchainLaunchSniper " + versionNumber))
    sys.stdout.flush()

COLOUR = variables.chainLogoColour
RESET = variables.RESET


print(variables.RESET + ''' 
                                                .||||.  
                                                .||||.                                               
                                                .||||.                                               
                                                .||||.                                               
                                               .-||||-.                                              
                                      ..-:+||||--||||--||||+:-..                                     
                                  .-+|-||||||||||||||||||||||||-|+-.                                 
                  -|+.        ..+|||||||||-|||+.::::::.+|||-|||||||||+..        .+|-                 
                .||||-..    .+-||||||||:-.                  .-:||||||||-+.    ..-||||.               
                 -|||||-..  ..|||-|:.                            .:|-|||..  ..-|||||-                
                   -|||||-:   ..-                                    -..   :-|||||-                  
                     -|||||-:                     ''' + COLOUR + '''..''' + RESET + '''                     :-|||||-                    
                       :-|||||-                ''' + COLOUR + '''..||||..''' + RESET + '''                -|||||-:                      
                   .+.   :-|||||.           ''' + COLOUR + '''-+-||||||||-+-''' + RESET + '''           .|||||-:   .+.                  
                  ||||.   ..-|||:       ''' + COLOUR + '''.:|||||||-||-|||||||:.''' + RESET + '''       :|||-..   .||||                 
                .|||||:     .---.    ''' + COLOUR + '''..||||||||+..  ..+||||||||..''' + RESET + '''    .---.     :|||||.               
                |||||-           ''' + COLOUR + '''.-+-|||||||...        ...|||||||-+-.''' + RESET + '''           -|||||               
               |||||-        ''' + COLOUR + ''' .:|-|||||-|:.                .:|-|||||-|:.''' + RESET + '''         -|||||              
              :||||.         ''' + COLOUR + '''||||||||+-.                      .-+||||||||''' + RESET + '''         .||||:             
              -||||          ''' + COLOUR + '''||||||||:.                        .:||||||||''' + RESET + '''          ||||-             
             .||||.          ''' + COLOUR + '''|||||||||||+..                ..+|||||||||||''' + RESET + '''          .||||.            
             |||||           ''' + COLOUR + '''||||+:|||||||-|-.          .-|-|||||||:+||||''' + RESET + '''           |||||            
            .||||:           ''' + COLOUR + '''||||.  .:|-|||||||:.    .:|||||||-|:.  .||||''' + RESET + '''           :||||.           
 ...........:||||.           ''' + COLOUR + '''||||.      .+||||||||++||||||||+.      .||||''' + RESET + '''           .||||:...........
 ||||||||||||||||            ''' + COLOUR + '''||||.         .:||||||||||||:.         .||||''' + RESET + '''            ||||||||||||||||
 ||||||||||||||||            ''' + COLOUR + '''||||.             -||||||-             .||||''' + RESET + '''            ||||||||||||||||
 ...........:||||.           ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''           .||||:...........
            .||||:           ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''           :||||.           
             |||||           ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''           |||||            
             .||||.          ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''          .||||.            
              -||||          ''' + COLOUR + '''|||||..            .||||.            ..|||||''' + RESET + '''          ||||-             
              :||||.         ''' + COLOUR + '''||||||||+-.        .||||.        .-+||||||||''' + RESET + '''         .||||:             
               |||||-         ''' + COLOUR + '''.:|-|||||-|:.     .||||.     .:|-|||||-|:.''' + RESET + '''         -|||||              
                |||||-           ''' + COLOUR + '''.-+-|||||||... .||||. ...|||||||-+-.''' + RESET + '''           -|||||               
                .|||||:     .---.    ''' + COLOUR + '''..||||||||+:||||:+||||||||..''' + RESET + '''    .---.     :|||||.               
                  ||||.   ..-|||:       ''' + COLOUR + '''.:||||||||||||||||||:.''' + RESET + '''       :|||-..   .||||                 
                   .+.   :-|||||.           ''' + COLOUR + '''-+-||||||||-+-''' + RESET + '''           .|||||-:   .+.                  
                       :-|||||-                ''' + COLOUR + '''..||||..''' + RESET + '''                -|||||-:                      
                     -|||||-:                     ''' + COLOUR + '''..''' + RESET + '''                     :-|||||-                    
                   -|||||-:   ..-                                    -..   :-|||||-                  
                 -|||||-..  ..|||-|:.                            .:|-|||..  ..-|||||-                
                .||||-..    .+-||||||||:-.                  .-:||||||||-+.    ..-||||.               
                  -|+.        ..+|||||||||-|||+.::::::.+|||-|||||||||+..        .+|-                 
                                  .-+|-||||||||||||||||||||||||-|+-.                                 
                                      ..-:+||||--||||--||||+:-..                                     
                                               .-||||-.                                              
                                                .||||.                                               
                                                .||||.                                               
                                                .||||.                                               
                                                .||||.
    
''')

print("BlockchainLaunchSniper", versionNumber)

print(variables.WHITE)     

variables.liquidityPairSymbol = token_details.getTokenSymbol(variables.liquidityPairAddress)

if(variables.chainCurrencySymbol in variables.liquidityPairSymbol):
    variables.liquidityPairSymbol = variables.chainCurrencySymbol
    variables.nonCoinLiquidity = False

#authenticate status

signed_message = w3.eth.account.sign_message(encode_defunct(text="BlockchainTokenSniper"), private_key=Web3.toBytes(hexstr=variables.walletPrivateKey))
signedWalletAddress = variables.web3.eth.account.recover_message(encode_defunct(text="BlockchainTokenSniper"), signature=signed_message.signature)

if signedWalletAddress != variables.walletAddress:
     print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Primary wallet address does not match private key.")
     quit.quitSniper(False)

variables.versionNumber = versionNumber
variables.backendFolder = backendFolder

#authenticate

connect_to_node.initAuthNode()
check_authorisation.checkAuth()

if variables.activeWalletAddress != None:
    variables.walletAddress = variables.activeWalletAddress
    variables.walletPrivateKey = variables.activeWalletPrivateKey


print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + "Using wallet address: " + variables.GREEN + variables.walletAddress)
print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + "Using " + variables.GREEN + str(variables.liquidityPairSymbol) + variables.RESET + " as liquidity pair.")
print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.RED + "Do not snipe any tokens you currently have in your wallet.")
print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.RED + "Do not make any other transactions involving your sniping wallet while bot is running.")
print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + "Current tier: " + variables.GREEN + variables.userTier)
print("")

init_nonce.initNonce()

if variables.chainCurrencySymbol not in variables.liquidityPairSymbol: #check if approved for liquidity pair
    contract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.exchangeRouterABI)
    sellTokenContract = variables.web3.eth.contract(address=variables.liquidityPairAddress, abi=variables.sellABI)
    tokenContract = variables.web3.eth.contract(address=variables.liquidityPairAddress, abi=variables.exchangeFunctionsABI)
    tokenAllowance = tokenContract.functions.allowance(variables.walletAddress, variables.exchangeRouterAddress).call()

    approveBalance = int((2 ** 256) - 1)
    if int(tokenAllowance) < (approveBalance * 0.5):
        print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + variables.YELLOW + "Auto-approving liquidity pair...")

        approveSentTX = None
        while approveSentTX == None:
            try:
                txDetails = {
                    'from': variables.walletAddress,
                    'nonce': variables.globalNonce
                }

                if variables.chainTxType == "0":
                    txDetails['gasPrice'] = variables.web3.toWei(int(variables.approve_gasPrice), 'gwei')

                elif variables.chainTxType == "2":
                    txDetails['maxFeePerGas'] = variables.web3.toWei(int(variables.approve_gasPrice), 'gwei')                  
                    txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(int(variables.approve_gasPrice), 'gwei')   
                else:
                    pass

                approveTX = sellTokenContract.functions.approve(variables.exchangeRouterAddress, approveBalance).buildTransaction(txDetails)

                approveSignedTX = variables.web3.eth.account.sign_transaction(approveTX, variables.walletPrivateKey)

                approveSentTX = variables.web3.eth.send_raw_transaction(approveSignedTX.rawTransaction)
                txHash = str(variables.web3.toHex(approveSentTX))
                variables.globalNonce += 1
                print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + variables.GREEN + "Approved liquidity pair.")
                print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + txHash)
                print("")
            except:
                debug.handleError(str(traceback.format_exc()), "liquidityPair_Approval")
                init_nonce.initNonce()

trading_check.initHoneypotContract()

def getInitialBalance():
    if variables.nonCoinLiquidity == True:
        sellTokenContract = variables.web3.eth.contract(address=variables.liquidityPairAddress, abi=variables.sellABI)
        variables.initialBalance = float(variables.web3.fromWei(sellTokenContract.functions.balanceOf(variables.walletAddress).call(), 'ether'))
    else:
        variables.initialBalance = float(variables.web3.fromWei(variables.web3.eth.getBalance(variables.walletAddress), 'ether'))
getInitialBalance()


def monitor_pending_tx():
    while not variables.snipeCompleted:
        try:
            pending_transaction_filter = variables.web3.eth.filter('pending')       
            for pending in pending_transaction_filter.get_new_entries():
                tx_hash = str(Web3.toHex(pending))
                tx_details = None
                gotTXDetails = False
                try:
                    tx_details = variables.web3.eth.get_transaction(tx_hash)
                    gotTXDetails = True
                except:
                    pass

                if gotTXDetails:
                    function_hash = tx_details['input'][:10].lower()
                    if function_hash in variables.addLiquidityFunctionHashes:
                       if (variables.snipeTokenAddress[2:].lower() in tx_details['input'].lower() or 
                          (tx_details['from'].lower() == variables.snipeTokenAddress.lower()) or
                          (tx_details['to'].lower() == variables.snipeTokenAddress.lower())):

                           print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + tx_hash)
                           print(variables.RESET + time_thread.currentTimeStamp + " [Mempool]  " + variables.YELLOW + "Detected liquidity TX, attempting to buy...")
                           buy_token.buyToken(variables.snipeTokenAddress)
        except:
            debug.handleError(traceback.format_exc(), "monitorPendingTXMain")


def sell_monitor_pending_tx(): 
    while not variables.snipeCompleted:
        try:
            pending_transaction_filter = variables.web3.eth.filter("pending")
            for pending in pending_transaction_filter.get_new_entries():
                tx_hash = str(Web3.toHex(pending))
                tx_details = None
                gotTXDetails = False
                try:
                    tx_details = variables.web3.eth.get_transaction(tx_hash)
                    gotTXDetails = True
                except:
                    pass

                if gotTXDetails:
                    function_hash = tx_details['input'][:10].lower()              
                    if function_hash in variables.addLiquidityFunctionHashes:
                       if (variables.snipeTokenAddress[2:].lower() in tx_details['input'].lower() or 
                          (tx_details['from'].lower() == variables.snipeTokenAddress.lower()) or
                          (tx_details['to'].lower() == variables.snipeTokenAddress.lower())):
                           print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + tx_hash)
                           print(variables.RESET + time_thread.currentTimeStamp + " [Mempool]  " + variables.YELLOW + "Detected liquidity TX, attempting to sell...")
                           if variables.antiBotDelay > 0:
                               time.sleep(variables.antiBotDelay)
                               trading_check.repeatHoneypotCheck(variables.snipeTokenAddress)
                
                               if(variables.enableHotkeys):
                                   setup_hotkeys.setup_hotkeys()                                    

                               monitor_price.manualMonitorAndSell()
                          
        except:
            pass

def setupInterface():
    try:
        print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + "Please choose from one of the following options:")
        print("")
        print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.CYAN + "1 - Snipe tokens when token address is provided.")
        print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.CYAN + "2 - Snipe tokens when liquidity is added.")
        print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.CYAN + "3 - Snipe tokens at certain time.")
        print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.CYAN + "4 - Monitor / sell tokens when token address is provided.")
        print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.CYAN + "5 - Monitor / sell tokens when liquidity is added.")
        print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.CYAN + "6 - Snipe miner contract when trading is enabled.")
        print(variables.RESET + "")

        snipeMode = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "Please enter option (1-6) then press ENTER: ")

        if snipeMode == "1":
            variables.tokenSnipeAmount = float(input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(2/6): Please enter amount to buy in " + variables.liquidityPairSymbol + ": "))
            
            autoSellValue = None
            if not variables.enableTrailingStopLoss:
                if variables.enableHotkeys:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x) - to sell manually press ENTER: ")
                else:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x): ")
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): N/A (using trailing stop loss)")

            honeypotCheckAnswer = None
            if variables.honeypotCheckerAddress != "":
                honeypotCheckAnswer = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): Enable honeypot/antibot checker? (Y/N): ")
            else:
                honeypotCheckAnswer = "N"
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): N/A")
            
            if(honeypotCheckAnswer.upper() == "Y"):
                variables.honeypotCheck = True
            else:
                variables.honeypotCheck = False

            if honeypotCheckAnswer.upper() != "Y" and honeypotCheckAnswer.upper() != "N":
                raise Exception()

            variables.antiBotDelay = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(5/6): Please enter anti-bot buy delay in seconds - for no delay press ENTER: ")
            
            if(variables.antiBotDelay == None or variables.antiBotDelay == "" or variables.antiBotDelay == 0):
                variables.antiBotDelay = 0
            else:
                variables.antiBotDelay = float(variables.antiBotDelay)

            if variables.antiBotDelay < 0:
                raise Exception()

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.GREEN + "(6/6): Please input the contract address of the token you would like to snipe then press ENTER to immediately snipe: ")
            variables.snipeTokenAddress = str(input("                                 ").lower()).split("0x", 1)[1][:40]
            variables.snipeTokenAddress = "0x" + variables.snipeTokenAddress
            variables.snipeTokenAddress = Web3.toChecksumAddress(variables.snipeTokenAddress)
            print("")

            variables.initialTokenPrice = variables.tokenSnipeAmount
            buy_token.preSign(variables.snipeTokenAddress)
            buy_token.buyToken(variables.snipeTokenAddress)

        elif snipeMode == "2":
            variables.tokenSnipeAmount = float(input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(2/6): Please enter amount to buy in " + variables.liquidityPairSymbol + ": "))
           
            autoSellValue = None

            if not variables.enableTrailingStopLoss:
                if variables.enableHotkeys:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x) - to sell manually press ENTER: ")
                else:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x): ")
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): N/A")

            if autoSellValue != "" and autoSellValue != None:
                variables.autoSellMultiplier = float(autoSellValue)
            else:
                variables.autoSellMultiplier = None

            if variables.autoSellMultiplier != None and variables.autoSellMultiplier <= 1:
                raise Exception()

            honeypotCheckAnswer = None
            if variables.honeypotCheckerAddress != "":
                honeypotCheckAnswer = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): Enable honeypot/antibot checker? (Y/N): ")
            else:
                honeypotCheckAnswer = "N"
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): N/A")
            
            if(honeypotCheckAnswer.upper() == "Y"):
                variables.honeypotCheck = True
            else:
                variables.honeypotCheck = False

            if honeypotCheckAnswer.upper() != "Y" and honeypotCheckAnswer.upper() != "N":
                raise Exception()

            variables.antiBotDelay = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(5/6): Please enter anti-bot buy delay in seconds - for no delay press ENTER: ")
            
            if(variables.antiBotDelay == None or variables.antiBotDelay == "" or variables.antiBotDelay == 0):
                variables.antiBotDelay = 0
            else:
                variables.antiBotDelay = float(variables.antiBotDelay) #convert to float

            if variables.antiBotDelay < 0:
                raise Exception()

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.GREEN + "(6/6): Please input the contract address of the token you would like to snipe then press ENTER to queue snipe: ")
            variables.snipeTokenAddress = str(input("                                 ").lower()).split("0x", 1)[1][:40]
            variables.snipeTokenAddress = "0x" + variables.snipeTokenAddress
            variables.snipeTokenAddress = Web3.toChecksumAddress(variables.snipeTokenAddress)

            variables.initialTokenPrice = variables.tokenSnipeAmount

            print("")
            buy_token.preSign(variables.snipeTokenAddress)
            print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Waiting for liquidity to be added to token...")
            print("")

            monitor_pending_tx()
   
        elif snipeMode == "3":
            variables.tokenSnipeAmount = float(input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(2/6): Please enter amount to buy in " + variables.liquidityPairSymbol + ": "))
            
            if variables.tokenSnipeAmount != None and variables.tokenSnipeAmount < 0:
                raise Exception()

            autoSellValue = None
            if not variables.enableTrailingStopLoss:
                if variables.enableHotkeys:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x) - to sell manually press ENTER: ")
                else:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x): ")
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): N/A")

            if autoSellValue != "" and autoSellValue != None:
                variables.autoSellMultiplier = float(autoSellValue)
            else:
                variables.autoSellMultiplier = None

            if variables.autoSellMultiplier != None and variables.autoSellMultiplier <= 1:
                raise Exception()

            honeypotCheckAnswer = None
            if variables.honeypotCheckerAddress != "":
                honeypotCheckAnswer = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): Enable honeypot/antibot checker? (Y/N): ")
            else:
                honeypotCheckAnswer = "N"
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): N/A")
            
            if(honeypotCheckAnswer.upper() == "Y"):
                variables.honeypotCheck = True
            else:
                variables.honeypotCheck = False

            if honeypotCheckAnswer.upper() != "Y" and honeypotCheckAnswer.upper() != "N":
                raise Exception()

            variables.antiBotDelay = 0

            waitTimeStamp = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.GREEN + "(5/6): Please input the exact time when you would like to snipe (HH:MM:SS): ")

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.GREEN + "(6/6): Please input the contract address of the token you would like to snipe then press ENTER to queue snipe: ")
            variables.snipeTokenAddress = str(input("                                 ").lower()).split("0x", 1)[1][:40]
            variables.snipeTokenAddress = "0x" + variables.snipeTokenAddress
            variables.snipeTokenAddress = Web3.toChecksumAddress(variables.snipeTokenAddress)

            variables.initialTokenPrice = variables.tokenSnipeAmount

            print("")
            buy_token.preSign(variables.snipeTokenAddress)
            print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Waiting until time has been reached...")
            
            while waitTimeStamp not in time_thread.currentTimeStamp:
                pass

            buy_token.buyToken(variables.snipeTokenAddress)

        elif snipeMode == "4":
            variables.initialTokenPrice = float(input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(2/6): Please enter amount spent on buying tokens in " + variables.liquidityPairSymbol + ": "))
            if variables.tokenSnipeAmount != None and variables.tokenSnipeAmount < 0:
                raise Exception()

            autoSellValue = None
            if not variables.enableTrailingStopLoss:
                if variables.enableHotkeys:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x) - to sell manually press ENTER: ")
                else:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x): ")
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): N/A")

            if autoSellValue != "" and autoSellValue != None:
                variables.autoSellMultiplier = float(autoSellValue)
            else:
                variables.autoSellMultiplier = None

            if variables.autoSellMultiplier != None and variables.autoSellMultiplier <= 1:
                raise Exception()

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): N/A")          
            variables.honeypotCheck = False

            variables.antiBotDelay = 0

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(5/6): N/A")
            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.GREEN + "(6/6): Please input the contract address of the token you would like to sell then press ENTER to queue sell: ")
            variables.snipeTokenAddress = str(input("                                 ").lower()).split("0x", 1)[1][:40]
            variables.snipeTokenAddress = "0x" + variables.snipeTokenAddress
            variables.snipeTokenAddress = Web3.toChecksumAddress(variables.snipeTokenAddress)

            print("")

            if(variables.enableHotkeys):
                setup_hotkeys.setup_hotkeys()                           

            monitor_price.manualMonitorAndSell()

        elif snipeMode == "5":
            variables.initialTokenPrice = float(input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(2/6): Please enter amount spent on buying tokens in " + variables.liquidityPairSymbol + ": "))
            if variables.tokenSnipeAmount != None and variables.tokenSnipeAmount < 0:
                raise Exception()

            autoSellValue = None
            if not variables.enableTrailingStopLoss:
                if variables.enableHotkeys:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x) - to sell manually press ENTER: ")
                else:
                    autoSellValue = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): Please enter autosell multiplier to sell at (eg. 2 for 2x): ")
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/6): N/A")

            if autoSellValue != "" and autoSellValue != None:
                variables.autoSellMultiplier = float(autoSellValue)
            else:
                variables.autoSellMultiplier = None

            if variables.autoSellMultiplier != None and variables.autoSellMultiplier <= 1 and (snipeMode != "4" or snipeMode != "5"):
                raise Exception()

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/6): N/A")          
            variables.honeypotCheck = False

            variables.antiBotDelay = 0

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(5/6): N/A")
            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.GREEN + "(6/6): Please input the contract address of the token you would like to sell then press ENTER to queue sell: ")
            variables.snipeTokenAddress = str(input("                                 ").lower()).split("0x", 1)[1][:40]
            variables.snipeTokenAddress = "0x" + variables.snipeTokenAddress
            variables.snipeTokenAddress = Web3.toChecksumAddress(variables.snipeTokenAddress)

            print("")                                           
            print(variables.RESET + time_thread.currentTimeStamp + " [Mempool]  " + variables.GREEN + "Waiting for liquidity to be added to token...")
            
            sell_monitor_pending_tx()

        elif snipeMode == "6":
            print("")
            print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Please be aware that these miner contracts are probably Ponzi schemes.")
            print("                          " + variables.YELLOW + "Although sniping them can be very profitable, do not invest more than you can afford to lose and DYOR to make sure it isn't a scam.")
            print("                          " + variables.YELLOW + "This bot should work with all Baked Beans forked miner contracts, however some ones may not work.")

            print("")

            ABIFileName = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(2/7): Please enter file name of miner contract JSON ABI in ABI folder (eg. minerABI.json): ")
            
            if ".json" not in ABIFileName:
                raise Exception()

            minerBuyAmount = float(input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(3/7): Please enter amount to spend on snipe in " + variables.liquidityPairSymbol + ": "))

            minerBuyFunction = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(4/7): Please enter name of miner buy function (eg. buyEggs): ")
            
            getBalanceFunction = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(5/7): If getBalance function is non-standard then enter here, otherwise press ENTER: ")

            if getBalanceFunction == "":
                getBalanceFunction = "getBalance"
            else:
                pass

            refAddress = None
            if variables.userTier == "Gold" or variables.userTier == "Diamond":
                refAddress = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(6/7): If preferred, enter a custom referral wallet address, or to use dev address press ENTER: ")
                if refAddress == "":
                    refAddress = variables.devFeeAddress
                else:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.ORANGE + "(6/7): N/A")
                    refAddress = Web3.toChecksumAddress(refAddress)

            else:
                refAddress = variables.devFeeAddress

            print(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.GREEN + "(7/7): Please enter contract address of miner and press ENTER to queue snipe: ")
            contractAddress = str(input("                                 ").lower()).split("0x", 1)[1][:40]
            contractAddress = "0x" + contractAddress
            contractAddress = Web3.toChecksumAddress(contractAddress)

            try:
                snipe_miner.queueSnipe(contractAddress, minerBuyAmount, minerBuyFunction, getBalanceFunction, ABIFileName, refAddress)
            except:
                debug.handleError(traceback.format_exc(), "queueMinerSnipeFunction")
        else:
            raise Exception()

    except:
        print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.RED + "Illegal input! Input is not valid.")
        quit.quitSniper(True)


if resume_snipe.initSnipeState():
    setupInterface()

else:
    resumeSnipe = input(variables.RESET + time_thread.currentTimeStamp + " [Setup]    " + variables.YELLOW + "Previous snipe was unfinished. Resume? (Y/N): ")
    if resumeSnipe.upper() == "Y":
        setup_hotkeys.setup_hotkeys()
        print("")
        resume_snipe.completePreviousSnipe()
    else:       
        resume_snipe.delSnipeState()
        getInitialBalance()
        setupInterface() #setup new snipe