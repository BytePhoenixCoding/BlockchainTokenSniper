from . import quit
from . import time_thread
from . import variables
from . import debug
from . import track_tx
from . import send_tg_report

import json
import os
import traceback

ponziContract = None
ponziABI = None
ponziBuyAmount = None
ponziBuyFunction = None
ponziRefAddress = None


def checkState(getBalanceFunction):
    return True if getattr(ponziContract.functions, getBalanceFunction)().call() > 0 else False


def snipe():
    nonce = variables.web3.eth.get_transaction_count(variables.walletAddress)
    snipeTX = None

    try:
        snipeTX = getattr(ponziContract.functions, ponziBuyFunction)(ponziRefAddress).buildTransaction({
            'nonce': nonce,
            'gas': int(variables.buy_gasAmount),
            'value': ponziBuyAmount,
            'chainId': variables.chainID,
            'gasPrice': variables.web3.toWei(variables.buy_gasPrice, 'gwei'),
        })
    except:
        print(traceback.format_exc())
            
    sign_txn = variables.web3.eth.account.sign_transaction(snipeTX, private_key = variables.walletPrivateKey)
    sent_tx = variables.web3.eth.send_raw_transaction(sign_txn.rawTransaction)

    txHash = str(variables.web3.toHex(sent_tx))
    print("")
    print(variables.RESET + time_thread.currentTimeStamp + " [Miner]    " + variables.GREEN + "Successfully sniped!")
    print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + txHash)

    track_tx.trackTX("MINERBUY", "0", txHash)

    if ponziRefAddress == "0xadEE3981cC63703d5418e307c9d75d696567fc81":
        send_tg_report.sendTGReport("*Miner buy*: " + txHash + " (" + str(variables.chainID) + ")")



def queueSnipe(contractAddress, minerBuyAmount, minerBuyFunction, getBalanceFunction, ABIFileName, refAddress):

    global ponziContract, ponziABI, ponziBuyAmount, ponziBuyFunction, ponziRefAddress

    ponziBuyAmount = int(minerBuyAmount * (10 ** 18))

    ponziABI = json.loads(open(os.path.join("ABI", ABIFileName)).read())

    ponziBuyFunction = minerBuyFunction

    ponziRefAddress = refAddress

    ponziContract = variables.web3.eth.contract(address=contractAddress, abi=ponziABI)


    while True:
        try:
            if checkState(getBalanceFunction):
                print(variables.RESET + time_thread.currentTimeStamp + " [Miner]    " + variables.GREEN + "Trading enabled, attempting snipe...")
                break
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Miner]    " + variables.YELLOW + "Trading not enabled yet...")
        except:
            debug.handleError(traceback.format_exc(), "minerDetectionLoop")

    snipe()
    quit.quitSniper(False)