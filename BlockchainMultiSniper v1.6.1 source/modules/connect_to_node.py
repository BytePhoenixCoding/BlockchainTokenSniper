from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
import json
from . import variables
from . import time_thread
from . import quit

authNodeURL = "https://bsc-dataseed.binance.org"

def connect():
    tries = 0
    nodeConnected = False

    while not nodeConnected:
        if tries >= 10:
            print(variables.RED + "FATAL ERROR: Cannot connect to blockchain node. This could be because your internet "
                    "connection is unavailable, the blockchain node has connectivity issues or a firewall is "
                    "blocking the bot's access.")
            print(variables.RED + "Please fix the error and restart the bot.")
            quit.quitSniper(True)

        try:
            if "WS://" in variables.blockchainNode.upper() or "WSS://" in variables.blockchainNode.upper():  
                variables.web3 = Web3(Web3.WebsocketProvider(variables.blockchainNode))#, websocket_kwargs={'verify': False}))             

            elif "HTTP://" in variables.blockchainNode.upper() or "HTTPS://" in variables.blockchainNode.upper():
                variables.web3 = Web3(Web3.HTTPProvider(variables.blockchainNode, request_kwargs={'verify': False}))

            elif "FILE://" in variables.blockchainNode.upper():
                variables.web3 = Web3(Web3.IPCProvider(variables.blockchainNode))

            else:
                raise Exception()


            if variables.web3 == None:
                raise Exception("1")

            if not variables.web3.isConnected():
                raise Exception("2")
                
            variables.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

            try:
                blockTest = variables.web3.eth.get_block('latest')
            except:
                raise Exception("3")

            nodeConnected = True
        except:
            tries += 1
            print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Cannot connect to node, retrying... (attempt " + str(tries) + "/10)")
    if nodeConnected:


        #get chain ID

        variables.chainID = variables.web3.eth.chain_id

        #connect to chains.json
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
            quit.quitSniper(True)

def initAuthNode():
    try:
        tries = 0
        nodeConnected = False
        while time_thread.currentTimeStamp == None:
            pass

        while nodeConnected == False:
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
                tries += 1
                print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Cannot connect to authentication node, retrying... (attempt " + str(tries) + "/10)")

    except:
        print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Possible authentication node timeout, retrying...")
        initAuthNode()