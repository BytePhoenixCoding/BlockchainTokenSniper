from web3 import Web3
import webbrowser
import traceback
import time
import datetime
from . import variables
from . import debug
from . import track_tx
from . import time_thread
from . import trading_check
from . import time_thread
from . import init_nonce
from . import quit
from . import setup_hotkeys
from . import monitor_price
from . import token_details
from . import resume_snipe

preSignedTX = None

def preSign(tokenAddress):
    global preSignedTX
    try:
        tokenToBuy = tokenAddress
        tokenToSpend = variables.liquidityPairAddress  #wbnb contract address or alt address
        contract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.exchangeRouterABI)

        exchangeTX = None

        #######################  APPROVE TOKEN ##############################
        '''

        sellTokenContract = variables.web3.eth.contract(address=variables.liquidityPairAddress, abi=variables.sellABI)
        tokenContract = variables.web3.eth.contract(address=variables.tokenAddress, abi=variables.exchangeFunctionsABI)
        tokenAllowance = tokenContract.functions.allowance(variables.walletAddress, variables.exchangeRouterAddress).call()

        approveBalance = int((2 ** 256) - 1)
        if int(tokenAllowance) < (approveBalance * 0.5):
            print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + variables.YELLOW + "Approving token...")

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
                    track_tx.trackTX("APPROVE", "0", txHash)
                    print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + variables.GREEN + "Approved liquidity pair.")
                    print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + txHash)
                    print("")
                except:
                    debug.handleError(str(traceback.format_exc()), "liquidityPair_Approval")#print("approveToken error (please notify dev):", traceback.format_exc())
                    init_nonce.initNonce()
        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + variables.GREEN + "Already approved.")

        '''
        ######################################################################



        if not variables.nonCoinLiquidity: #snipe with WCoin as pair
            while exchangeTX == None:
                try:

                    txDetails = {
                        'from': variables.walletAddress,
                        'value': variables.web3.toWei(float(variables.tokenSnipeAmount), 'ether'),
                        'gas': variables.buy_gasAmount,
                        'nonce': variables.globalNonce,
                    }

                    if variables.chainTxType == "0":
                        txDetails['gasPrice'] = variables.web3.toWei(variables.buy_gasPrice,'gwei')

                    elif variables.chainTxType == "2":
                        txDetails['maxFeePerGas'] = variables.web3.toWei(variables.buy_gasPrice,'gwei')                  
                        txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.buy_gasPrice,'gwei')   

                    else:
                        pass

                    exchangeTX = getattr(contract.functions, variables.buyWithCoinFunction)(
                    0,
                    [tokenToSpend, tokenToBuy],
                    variables.walletAddress,
                    (int(time.time()) + variables.transactionRevertTime)
                    ).buildTransaction(txDetails)

                except:
                    debug.handleError(str(traceback.format_exc()), "buyToken_A")


        else: #snipe with alt token as pair
            while exchangeTX == None:
                try:


                    txDetails = {
                        'from': variables.walletAddress,
                        'gas': variables.buy_gasAmount,
                        'nonce': variables.globalNonce,
                    }

                    if variables.chainTxType == "0":
                        txDetails['gasPrice'] = variables.web3.toWei(variables.buy_gasPrice,'gwei')

                    elif variables.chainTxType == "2":
                        txDetails['maxFeePerGas'] = variables.web3.toWei(variables.buy_gasPrice,'gwei')                  
                        txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.buy_gasPrice,'gwei')   
                    else:
                        pass

                    exchangeTX = getattr(contract.functions, variables.buyWithAltPairFunction)( #eg. BUSD -> token 
                    variables.web3.toWei(variables.tokenSnipeAmount, 'ether'), #minReceived,
                    0,
                    [tokenToSpend,tokenToBuy],
                    variables.walletAddress,
                    (int(time.time()) + variables.transactionRevertTime)
                    ).buildTransaction(txDetails)
                except:
                    debug.handleError(str(traceback.format_exc()), "buyToken_B")
                

        try:
            preSignedTX = variables.web3.eth.account.sign_transaction(exchangeTX, variables.walletPrivateKey)
            print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.GREEN + "Pre-signed buy TX.")
        except:
            debug.handleError(traceback.format_exc(), "preSignMain")
    except:
        debug.handleError(traceback.format_exc(), "preSign")


def buyToken(tokenAddress):
    global preSignedTX
    try:
        try:

            if variables.honeypotCheck:
                trading_check.repeatHoneypotCheck(tokenAddress)

            if(variables.antiBotDelay > 0):                         
                print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.YELLOW + "Delaying purchase for " + str(variables.antiBotDelay) + " seconds for antibot delay.")
                time.sleep(variables.antiBotDelay)

            tx_token = None
            while tx_token == None:
                try:
                    tx_token = variables.web3.eth.send_raw_transaction(preSignedTX.rawTransaction)
                except:
                    #print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    " + variables.YELLOW + "Reattempting transaction...")
                    debug.handleError(str(traceback.format_exc()), "buyToken_C")
                    init_nonce.initNonce()


         
            variables.tokenSymbol = token_details.getTokenSymbol(tokenAddress)

            txHash = str(variables.web3.toHex(tx_token))

            print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.GREEN + "Submitted buy TX for $" + variables.tokenSymbol + ", awaiting TX receipt...")
            print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + txHash)

        except:
            if variables.liquidityPairSymbol == variables.chainCurrencySymbol:
                print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Transaction failed, most likely not enough balance in your wallet. Check the blockchain explorer and if you have enough funds in your wallet.")
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Transaction failed, most likely not enough balance in your wallet. Check the blockchain explorer and if you have enough funds in your wallet.")     # Full error:", traceback.format_exc())# + str(web3.toHex(tx_token)))
            
                debug.handleError(str(traceback.format_exc()), "buyToken_D")
            print("")

            quit.quitSniper(True)

        txReceipt = None
        while txReceipt == None:
            try:
                txHash = str(variables.web3.toHex(tx_token))
                txReceipt = variables.web3.eth.wait_for_transaction_receipt(txHash, timeout=3600)
            except:
                pass

        if(txReceipt["status"] == 1):
            print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.GREEN + "Successfully bought $" + variables.tokenSymbol + " for " + variables.CYAN + str(variables.tokenSnipeAmount) + variables.GREEN + " " + variables.liquidityPairSymbol)
            print("")
            
            track_tx.trackTX("BUY", str(variables.tokenSnipeAmount), txHash)
                
            if(variables.sellTokens and variables.enableHotkeys):
                setup_hotkeys.setup_hotkeys()

            if variables.sellTokens:
                monitor_price.manualMonitorAndSell()
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.GREEN + "Transaction completed, selling tokens disabled.")
                quit.quitSniper(False)

        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.RED + "Transaction failed: likely not enough gas.")
            quit.quitSniper(True)


    except Exception as ex:
        print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.RED + "Transaction failed: possible scam token, bad contract or other issue.")
        debug.handleError(str(traceback.format_exc()), "buyToken_E")
        quit.quitSniper(True)