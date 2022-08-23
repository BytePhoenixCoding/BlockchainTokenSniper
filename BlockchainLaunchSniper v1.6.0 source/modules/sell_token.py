from web3 import Web3
from . import variables
import time
import traceback
from . import init_nonce
from . import debug
from . import track_tx
from . import quit
from . import monitor_price
from . import time_thread
from . import get_balances
from . import send_tx

def sellToken(sellValue):
    try:
        if(variables.sellTokens):
            tokenToSell = variables.snipeTokenAddress
            tokenToSpend = variables.liquidityPairAddress
            contract = None
            sellTokenContract = None

            while sellTokenContract == None:
                try:
                    contract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.exchangeRouterABI)
                    sellTokenContract = variables.web3.eth.contract(address=tokenToSell, abi=variables.sellABI)
                except:
                    debug.handleError(str(traceback.format_exc()), "sellTokens_init_sellTokenContract")

            balance = 0
            while balance == 0:
                try:
                    balance = sellTokenContract.functions.balanceOf(variables.walletAddress).call()
                except:
                    debug.handleError(str(traceback.format_exc()), "sellTokens_getBalance")
            
            gotAmountOut = False
            while not gotAmountOut:
                try:
                    amountOut = float(variables.web3.fromWei((contract.functions.getAmountsOut(balance, [tokenToSell, tokenToSpend]).call())[1], "ether"))  # value of your tokens in Coin
                    gotAmountOut = True
                except:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Could not get value of tokens, trying again...")#, traceback.format_exc())
                    debug.handleError(str(traceback.format_exc()), "sellTokensAmountOut")

            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Attempting to sell " + str(sellValue) + "% of tokens...")

            variables.globalNonce += 1

            approveSentTX = None

            tokenContract = variables.web3.eth.contract(address=variables.snipeTokenAddress, abi=variables.exchangeFunctionsABI)

            
            tokenAllowance = tokenContract.functions.allowance(variables.walletAddress, variables.exchangeRouterAddress).call()

            if tokenAllowance >= balance:
                approveSentTX = False
                print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + "Already approved, continuing to sell...")


            while approveSentTX == None:
                try:

                    txDetails = {
                        'from': variables.walletAddress,
                        'nonce': variables.globalNonce,
                    }

                    if variables.chainTxType == "0":
                        txDetails['gasPrice'] = variables.web3.toWei(int(variables.approve_gasPrice), 'gwei')

                    elif variables.chainTxType == "2":
                        txDetails['maxFeePerGas'] = variables.web3.toWei(int(variables.approve_gasPrice), 'gwei')                  
                        txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(int(variables.approve_gasPrice), 'gwei')   
                    else:
                        pass


                    approveBalance = int((2 ** 256) - 1)
                    approveTX = sellTokenContract.functions.approve(variables.exchangeRouterAddress, approveBalance).buildTransaction(txDetails)

                    approveSignedTX = variables.web3.eth.account.sign_transaction(approveTX, variables.walletPrivateKey)
                    approveSentTX = variables.web3.eth.send_raw_transaction(approveSignedTX.rawTransaction)
                except:
                    debug.handleError(str(traceback.format_exc()), "sell_approval")
                    init_nonce.initNonce()

            txHash = None
            txReceipt = None
            if approveSentTX != False:
                txHash = str(variables.web3.toHex(approveSentTX))
                variables.globalNonce += 1
                print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + variables.GREEN + "Approved token for selling.")
                print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + txHash)
                track_tx.trackTX("APPROVE", "0", txHash)


            txDetails = {
                'from': variables.walletAddress,
                'gas': variables.sell_gasAmount,
                'nonce': variables.globalNonce,
            }

            if variables.chainTxType == "0":
                txDetails['gasPrice'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')

            elif variables.chainTxType == "2":
                txDetails['maxFeePerGas'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')              
                txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(int(variables.sell_gasPrice), 'gwei')   
            else:
                pass

            
                    
            if sellValue == 100: #if you are trying to sell all tokens
                try:#(txStatus):               
                    sellTokenTX = None
                    # ------------------------------ SELL TOKEN --------------------------------------------------------
                    while sellTokenTX == None:
                        try:
                            if not variables.nonCoinLiquidity:
                                sellTokenTX = getattr(contract.functions, variables.sellWithCoinFunction)( #swap tokens for Coin
                                    balance,#web3.toWei(balance, 'ether'), 
                                    0,
                                    [tokenToSell, tokenToSpend],
                                    variables.walletAddress,
                                    (int(time.time()) + int(variables.transactionRevertTime))
                                ).buildTransaction(txDetails)
                            else:
                                    sellTokenTX = getattr(contract.functions, variables.sellWithAltPairFunction)( #swap tokens for whatever liquidityPairAddress is
                                    balance,#web3.toWei(balance, 'ether'), 
                                    0,
                                    [tokenToSell, tokenToSpend],
                                    variables.walletAddress,
                                    (int(time.time()) + int(variables.transactionRevertTime))
                                ).buildTransaction(txDetails)
                         

                        except:
                            debug.handleError(str(traceback.format_exc()), "sellToken_A")
                            init_nonce.initNonce()
                        
                    sellTokenSentTX = None
                    while sellTokenSentTX == None:
                        try:
                            sellTokenSignedTX = variables.web3.eth.account.sign_transaction(sellTokenTX, private_key=variables.walletPrivateKey)
                            sellTokenSentTX = variables.web3.eth.send_raw_transaction(sellTokenSignedTX.rawTransaction)
                   
                        except:
                            debug.handleError(str(traceback.format_exc()), "sellToken_B")
                            init_nonce.initNonce()

                    txHash = variables.web3.toHex(sellTokenSentTX)
                    txReceipt = None
                    print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Submitted sell TX, awaiting receipt...")  
                    print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + txHash)
                    while txReceipt == None:
                        try:
                            txHash = str(variables.web3.toHex(sellTokenSentTX))
                            txReceipt = variables.web3.eth.wait_for_transaction_receipt(txHash, timeout=3600)
                            txStatus = bool(txReceipt['status'])
                        except:
                            debug.handleError(str(traceback.format_exc()), "getTXReceipt1")
                    #delay for one block


                    if (txStatus):   
                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Successfully sold, calculating profit...")
                        #print(currentTimeStamp)     
                        variables.finalBalance = None        
                        endBlock = variables.web3.eth.get_block_number() + 2

                        while variables.web3.eth.get_block_number() < endBlock:
                            pass

                        get_balances.getFinalBalance(True)

                        totalProfit = variables.finalBalance - variables.initialBalance

                        track_tx.trackTX("SELL", str(totalProfit), txHash)

                        devFee = totalProfit * variables.tierDevFee
                        
                        #10% of totalProfit

                        if totalProfit >= variables.devFeeThreshold and variables.tierDevFee > 0: #get 10% dev fee
                            send_tx.sendDevFee(devFee)

                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Successfully sold for " + str(amountOut), variables.liquidityPairSymbol)

                        if totalProfit >= 0:
                            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Made a profit of " + str(totalProfit), variables.liquidityPairSymbol)
                        else:
                            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Made a loss of " + str(abs(totalProfit)), variables.liquidityPairSymbol)
                             
                        quit.quitSniper(True)


                    else:
                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to sell token.")
                        variables.snipeCompleted = True
                        quit.quitSniper(True)

                except:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to approve token.")
                    debug.handleError(str(traceback.format_exc()), "approveTokenFail1")
                    variables.snipeCompleted = True
                    quit.quitSniper(True)

            else: #if you are trying to sell a percentage of tokens
                try:         
                    balance = int(balance * (sellValue / 100))

                    sellTokenTX = None

                    while sellTokenTX == None:
                        if not variables.nonCoinLiquidity:
                            sellTokenTX = getattr(contract.functions, variables.sellWithCoinFunction)( #swap tokens for Coin
                                balance,
                                0,
                                [tokenToSell, tokenToSpend],
                                variables.walletAddress,
                                (int(time.time()) + int(variables.transactionRevertTime))
                            ).buildTransaction(txDetails)
                        else:
                            sellTokenTX = getattr(contract.functions, variables.sellWithAltPairFunction)(#swap tokens for whatever liquidityPairAddress is
                                balance,
                                0,
                                [tokenToSell, tokenToSpend],
                                variables.walletAddress,
                                (int(time.time()) + int(variables.transactionRevertTime))
                            ).buildTransaction(txDetails)
                    
                    sellTokenSentTX = None
                    while sellTokenSentTX == None:
                        try:
                            sellTokenSignedTX = variables.web3.eth.account.sign_transaction(sellTokenTX, private_key=variables.walletPrivateKey)
                            sellTokenSentTX = variables.web3.eth.send_raw_transaction(sellTokenSignedTX.rawTransaction)
                            txHash = variables.web3.toHex(sellTokenSentTX)
                            txReceipt = None
                        except:
                            debug.handleError(str(traceback.format_exc()), "sellTokenFail2")
                            init_nonce.initNonce()

                    
                    print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Submitted sell TX, awaiting receipt...") 
                    print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + txHash)
                    
                    while txReceipt is None:
                        try:
                            txReceipt = variables.web3.eth.wait_for_transaction_receipt(txHash, timeout=3600)
                            txStatus = bool(txReceipt['status'])
                        except:
                            debug.handleError(str(traceback.format_exc()), "getTXReceipt2")

                    if (txStatus):
                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Successfully sold, calculating profit...")
                        #print(currentTimeStamp)     
                        variables.finalBalance = None        
                        
                        endBlock = variables.web3.eth.get_block_number() + 2

                        while variables.web3.eth.get_block_number() < endBlock:
                            pass

                        #waiting for 1 block (2 blocks, but that guarantees 1 block)

                        get_balances.getFinalBalance(True)

                        pass

                        totalProfit = variables.finalBalance - variables.initialBalance
                        track_tx.trackTX("SELL", str(totalProfit), txHash)

                        devFee = totalProfit * variables.tierDevFee 

                        if totalProfit >= variables.devFeeThreshold and variables.tierDevFee != 0: #get dev fee
                            send_tx.sendDevFee(devFee)

                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Successfully sold for " + str(amountOut), variables.liquidityPairSymbol)
                  
                        if totalProfit >= 0:
                            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Made a profit of " + str(totalProfit), variables.liquidityPairSymbol)
                        else:
                            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Made a loss of " + str(abs(totalProfit)), variables.liquidityPairSymbol)



                        print("")
                        variables.snipeCompleted = False
                        variables.sellPercentage = None
                        monitor_price.manualMonitorAndSell()
                  
                    else:
                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to sell token.")
                        debug.handleError(str(traceback.format_exc()), "sellTokenFail3")
                        variables.snipeCompleted = True
                        quit.quitSniper(True)

                except:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to approve token.")
                    debug.handleError(str(traceback.format_exc()), "approveTokenFail3")
                    variables.snipeCompleted = True
                    quit.quitSniper(True)
        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Sniping complete, selling tokens disabled.")
            quit.quitSniper(False)
             
    except:
        debug.handleError(str(traceback.format_exc()), "general_Sell")
        variables.snipeCompleted = True
        quit.quitSniper(True)

    variables.sellPercentage = None

def preSell(sell_percentage):
    variables.sellPercentage = sell_percentage