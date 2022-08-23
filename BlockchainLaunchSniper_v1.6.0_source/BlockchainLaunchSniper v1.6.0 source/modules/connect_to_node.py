from web3 import Web3
from web3.middleware import geth_poa_middleware
import traceback
import os
import json
from . import variables
from . import quit
from . import time_thread

global tries

authNodeURL = "https://bsc-dataseed.binance.org"

def initNode(showOutput):
    try:
        tries = 0
        nodeConnected = False
        while time_thread.currentTimeStamp == None:
            pass
        while nodeConnected == False:
            #print(tries)
            if tries >= 10:
                print(variables.RED + "FATAL ERROR: Cannot connect to node. This could be because your internet "
                        "connection is unavailable, the node has connectivity issues or a firewall is "
                        "blocking the bot's access.")
                print(variables.RED + "Please fix the error and restart the bot.")
                quit.quitSniper(False)

            try:
                if "WS://" in variables.blockchainNode.upper() or "WSS://" in variables.blockchainNode.upper():  
                    variables.web3 = Web3(Web3.WebsocketProvider(variables.blockchainNode))#, websocket_kwargs={'verify': False}))

                elif "HTTP://" in variables.blockchainNode.upper() or "HTTPS://" in variables.blockchainNode.upper():
                    variables.web3 = Web3(Web3.HTTPProvider(variables.blockchainNode, request_kwargs={'verify': False}))

                else:
                    raise Exception()


                if variables.web3 == None:
                    raise Exception("1")
                     
                variables.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

                nodeConnected = True
            except:
                tries += 1

                if showOutput:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Cannot connect to node, retrying... (attempt " + str(tries) + "/10)")
        if nodeConnected == True:
            variables.chainID = variables.web3.eth.chain_id

            chainsFilePath = os.path.join(os.path.abspath(''), "chains.json")

            chainData = None
            with open(chainsFilePath, 'r', encoding='utf-8-sig') as chaindata:
                chainData = json.loads(chaindata.read())

            try:
                variables.chainName = chainData[str(variables.chainID)]["name"]
                variables.chainCurrencySymbol = chainData[str(variables.chainID)]["currencySymbol"]
                variables.chainLogoColour = "\033[38;5;" + chainData[str(variables.chainID)]["logoColour"] + "m"
                variables.chainTxType = chainData[str(variables.chainID)]["txType"]
            except:
                print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Unrecognised chain. Please add relevant chain in chains.json file.")
                quit.quitSniper(False)

            variables.devFeeGasPrice = variables.web3.fromWei(variables.buy_gasPrice, "gwei")



            if showOutput:
                print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Successfully connected to node.")
    except:
        print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Possible node timeout, retrying...")
        initNode(showOutput)

def initAuthNode():
    try:
        tries = 0
        nodeConnected = False
        while time_thread.currentTimeStamp == None:
            pass

        while nodeConnected == False:
            #print(tries)
            if tries >= 10:
                print(variables.RED + "FATAL ERROR: Cannot connect to authentication node. This could be because your internet "
                        "connection is unavailable, the node has connectivity issues or a firewall is "
                        "blocking the bot's access.")
                print(variables.RED + "Please fix the error and restart the bot.")
                quit.quitSniper(False)

            try:
                variables.web3_auth = Web3(Web3.HTTPProvider(authNodeURL, request_kwargs={'verify': False}))

                if variables.web3_auth == None:
                    raise Exception("1")
            
                variables.web3_auth.middleware_onion.inject(geth_poa_middleware, layer=0)

                nodeConnected = True
            except:
                print(traceback.format_exc())
                tries += 1
                print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Cannot connect to authentication node, retrying... (attempt " + str(tries) + "/10)")

    except:
        print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Possible authentication node timeout, retrying...")
        initAuthNode()