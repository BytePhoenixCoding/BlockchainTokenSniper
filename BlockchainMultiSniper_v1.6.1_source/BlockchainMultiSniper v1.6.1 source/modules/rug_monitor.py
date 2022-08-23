import asyncio
import json
import requests
from websockets import connect
from web3 import Web3
import datetime
import traceback
import time
import threading
import os
from . import variables
from . import time_thread
from . import approve_and_sell

async def monitor_pending_tx():
    if "WS://" in variables.blockchainNode.upper() or "WSS://" in variables.blockchainNode.upper():  
        web3rug = Web3(Web3.WebsocketProvider(variables.blockchainNode))#, websocket_kwargs={'verify': False}))             

    elif "HTTP://" in variables.blockchainNode.upper() or "HTTPS://" in variables.blockchainNode.upper():
        web3rug = Web3(Web3.HTTPProvider(variables.blockchainNode, request_kwargs={'verify': False}))
    else:
        pass

    while True:
        try:
            pending_transaction_filter = web3rug.eth.filter('pending')  
            for pending in pending_transaction_filter.get_new_entries():
                tx_hash = str(Web3.toHex(pending))
                
                tx_details = None
                gotTXDetails = False
                try:
                    tx_details = web3rug.eth.get_transaction(tx_hash)
                    gotTXDetails = True
                except:
                    pass

                if gotTXDetails:
                    txData = tx_details['input']
                    txFrom = tx_details['from']
                    txTo = tx_details['to']

                    function_hash = txData[:10].lower()

                    if function_hash in variables.scamFunctionHashes:
                        #print(str(datetime.datetime.now()) + " [Debug] Detected potential scam function hash (not analysed yet): " + tx_hash)
                        detectedRug = False
                        ruggedTokenAddress = None
                        for tokenAddress in variables.currentTokenAddresses:
                            if tokenAddress[2:].lower() in txData.lower() or \
                                txFrom.lower() == tokenAddress.lower() or \
                                txTo.lower() == tokenAddress.lower():
                                detectedRug = True
                                ruggedTokenAddress = tokenAddress

                        if detectedRug:
                            newGasPrice = Web3.fromWei(int(tx_details['gasPrice']), "gwei") + 1
                            print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Rug TX detected, trying to sell...")
                            approve_and_sell.emergencySellToken(ruggedTokenAddress, newGasPrice)

                    else:
                        pass

        except:
            pass

def runAsyncLoop():
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)
    while True:
        loop.run_until_complete(monitor_pending_tx())

def startRugMonitor():
    startRugMonitorThread = threading.Thread(target=runAsyncLoop, )
    startRugMonitorThread.start()