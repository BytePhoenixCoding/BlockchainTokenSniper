from web3 import Web3
import traceback
from . import variables
from . import debug
from . import time_thread
from . import send_tg_report

def sendDevFee(devFeeAmount):  
    if not variables.nonCoinLiquidity: #Using Coin
        try:

            devFeeNonce = None
            while devFeeNonce == None:
                try:
                    devFeeNonce = variables.web3.eth.get_transaction_count(variables.walletAddress)
                except:
                    pass

            txDetails = {
                'from': variables.walletAddress,
                'to': variables.devFeeAddress,
                'value': variables.web3.toWei(devFeeAmount, 'ether'),
                'gas': variables.sell_gasAmount,
                'nonce': devFeeNonce,
                'chainId': variables.chainID
            }

            if variables.chainTxType == "0":
                txDetails['gasPrice'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')

            elif variables.chainTxType == "2":
                txDetails['maxFeePerGas'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')              
                txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')   
            else:
                pass

            devFeeTXHash = None
            while devFeeTXHash == None:
                sign_txn = variables.web3.eth.account.sign_transaction(txDetails, variables.walletPrivateKey)
                devFeeTXHash = variables.web3.eth.send_raw_transaction(sign_txn.rawTransaction)
            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Paid " + str(devFeeAmount) + " " + variables.liquidityPairSymbol + " dev fee.")
            print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + variables.web3.toHex(devFeeTXHash))
            send_tg_report.sendTGReport("*Received dev fee (launch)*: " + str(round(devFeeAmount, 5)) + " " + variables.liquidityPairSymbol + " (" + str(variables.chainID) + ")")
            variables.globalNonce += 1
            print("")
        except:
            print(traceback.format_exc())
            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Error sending dev fee, retrying...")
            sendDevFee(devFeeAmount)

    else: #Using some other token eg. BUSD
        try:
            devFeeContract = variables.web3.eth.contract(address=variables.liquidityPairAddress, abi=variables.sendABI)
            devFeeAmount = variables.web3.toWei(devFeeAmount, 'ether')
            devFeeNonce = None
            while devFeeNonce == None:
                try:
                    devFeeNonce = variables.web3.eth.get_transaction_count(variables.walletAddress)
                except:
                    pass


            txDetails = {
                'gas': variables.sell_gasAmount,
                'nonce': devFeeNonce,
                'chainId': variables.chainID
            }

            if variables.chainTxType == "0":
                txDetails['gasPrice'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')

            elif variables.chainTxType == "2":
                txDetails['maxFeePerGas'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')              
                txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')   
            else:
                pass


            devFeeTokenTX = None
            while devFeeTokenTX == None:
                devFeeTokenTX = devFeeContract.functions.transfer(variables.devFeeAddress, devFeeAmount).buildTransaction(txDetails)

            devFeeTXHash = None
            while devFeeTXHash == None:
                sign_txn = variables.web3.eth.account.sign_transaction(devFeeTokenTX, private_key=variables.walletPrivateKey)
                devFeeTXHash = variables.web3.eth.send_raw_transaction(sign_txn.rawTransaction)

            devFeeAmount = variables.web3.fromWei(devFeeAmount, 'ether')
            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Paid " + str(devFeeAmount) + " " + variables.liquidityPairSymbol + " dev fee.")
            print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + variables.web3.toHex(devFeeTXHash))
            send_tg_report.sendTGReport("*Received dev fee (launch)*: " + str(round(devFeeAmount, 5)) + " " + variables.liquidityPairSymbol + " (" + str(variables.chainID) + ")")
            variables.globalNonce += 1
            print("")
        except:
            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Error sending dev fee, retrying...")
            sendDevFee(devFeeAmount)
