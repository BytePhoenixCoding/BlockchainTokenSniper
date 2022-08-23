import time
import traceback
import os
from . import debug
from . import track_tx
from . import token_analyser
from . import variables
from . import update_title
from . import time_thread
from . import approve_and_sell

buyTokenContract = None

def initBuyTokenContract():
    global buyTokenContract
    buyTokenContract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.routerABI)

def buyToken(tokenAddress, liquidityPairIndex):
    global buyTokenContract
    liquidityPairAddress = variables.liquidityPairs[liquidityPairIndex]['liquidityPairAddress']
    liquidityPairSymbol = variables.liquidityPairs[liquidityPairIndex]['symbol']

    try:
        sentTX = None
        txHash = None
        while txHash == None:    
            if liquidityPairSymbol == variables.chainCurrencySymbol:
                try:           
                    tokenToBuy = tokenAddress
                    buyAmount = variables.web3.toWei(float(variables.liquidityPairs[liquidityPairIndex]['snipeAmount']), 'ether')
                    variables.globalNonce += 1

                    txDetails = {
                        'from': variables.walletAddress,
                        'value': buyAmount,
                        'gas': variables.buyGasAmount,
                        'nonce': variables.globalNonce - 1,
                    }

                    if variables.chainTxType == "0":
                        txDetails['gasPrice'] = variables.web3.toWei(variables.buyGasPrice,'gwei')

                    elif variables.chainTxType == "2":
                        txDetails['maxFeePerGas'] = variables.web3.toWei(variables.buyGasPrice, 'gwei')                           
                        txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.buyGasPrice, 'gwei')   
                    else:
                        pass


                    exchangeTX = getattr(buyTokenContract.functions, variables.buyWithCoinFunction)(
                        0,
                        [liquidityPairAddress, tokenToBuy],
                        variables.walletAddress,
                        (int(time.time()) + variables.transactionRevertTime)
                    ).buildTransaction(txDetails)

                    signedTX = variables.web3.eth.account.sign_transaction(exchangeTX, variables.walletPrivateKey)
                    sentTX = variables.web3.eth.send_raw_transaction(signedTX.rawTransaction)

                            
                    buyAmount = variables.web3.fromWei(buyAmount, 'ether')

                                
                    txHash = str(variables.web3.toHex(sentTX))

                except:
                    debug.handleError(traceback.format_exc(), "buyToken_initialBuy")
            else:
                try:                     
                    tokenToBuy = tokenAddress


                    buyAmount = variables.web3.toWei(float(variables.liquidityPairs[liquidityPairIndex]['snipeAmount']), 'ether')
                    variables.globalNonce += 1

                    txDetails = {
                        'from': variables.walletAddress,
                        'gas': variables.buyGasAmount,
                        'nonce': variables.globalNonce - 1,
                    }

                    if variables.chainTxType == "0":
                        txDetails['gasPrice'] = variables.web3.toWei(variables.buyGasPrice,'gwei')

                    elif variables.chainTxType == "2":
                        txDetails['maxFeePerGas'] = variables.web3.toWei(variables.buyGasPrice, 'gwei')                           
                        txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.buyGasPrice, 'gwei')   
                    else:
                        pass



                    exchangeTX = getattr(buyTokenContract.functions, variables.buyWithAltPairFunction)(
                        buyAmount,
                        0,
                        [liquidityPairAddress, tokenToBuy],
                        variables.walletAddress,
                        (int(time.time()) + variables.transactionRevertTime)
                    ).buildTransaction(txDetails)

                    signedTX = variables.web3.eth.account.sign_transaction(exchangeTX, variables.walletPrivateKey)
                    sentTX = variables.web3.eth.send_raw_transaction(signedTX.rawTransaction)

                            
                    buyAmount = variables.web3.fromWei(buyAmount, 'ether')

                                
                    txHash = str(variables.web3.toHex(sentTX))

                except:
                    debug.handleError(traceback.format_exc(), "buyToken_initialBuy2")

        getTokenName = variables.web3.eth.contract(address=tokenAddress, abi=variables.tokenNameABI)

        tokenName = getTokenName.functions.name().call().encode("ascii", "ignore").decode() #get rid of non ascii 
        tokenSymbol = getTokenName.functions.symbol().call().encode("ascii", "ignore").decode() #get rid of non ascii

        print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.YELLOW + "Submitted TX for $" + tokenSymbol + ", awaiting TX receipt...")

        buyTXReceipt = None
        txStatus = None
        try:
            buyTXReceipt = variables.web3.eth.wait_for_transaction_receipt(txHash, timeout=variables.transactionRevertTime)
            txStatus = bool(buyTXReceipt['status'])
        except:
            pass

        if (txStatus):
            print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.GREEN + "Successfully bought $" + tokenSymbol + " for " + variables.CYAN + str(buyAmount) + " " + liquidityPairSymbol + variables.GREEN + " - " + variables.MAGENTA + txHash)
            variables.numTokensBought += 1 #its been successful, so snipe the token

            # ----------------------------------------- APPEND NEW TOKEN TO TOKENCACHE.CSV ----------------------------------------------------

            sellAmount = 1 #initialise

            if variables.tradingMode.upper() == "BASIC_AUTOSELL":
                sellAmount = float(buyAmount) * float(variables.basicAutoSellMultiplier)

            elif variables.tradingMode.upper() == "TRAILING_STOP_LOSS":
                endBlock = variables.web3.eth.get_block_number() + 2

                while variables.web3.eth.get_block_number() < endBlock:
                    pass


                exchangeContract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.routerABI)
                sellTokenContract = variables.web3.eth.contract(address=tokenAddress, abi=variables.sellABI) 
                balance = sellTokenContract.functions.balanceOf(variables.walletAddress).call()
                amount = exchangeContract.functions.getAmountsOut(balance, [tokenAddress, liquidityPairAddress]).call()[1]
                amountOut = float(variables.web3.fromWei(amount, "ether"))#value of your tokens in BNB
                sellAmount = float(amountOut) / float(buyAmount)

            elif variables.tradingMode.upper() == "SELL_AFTER_TIME_DELAY":
                sellAmount = time.time() + int(variables.sellAfterSeconds)

            else:
                pass


            with open(os.path.join("temp", (variables.chainName + 'TokenCache.csv')), 'a') as fileData:             
                fileData.write(tokenAddress + "," + tokenName + "," + tokenSymbol + "," + str(buyAmount) + "," + str(sellAmount) + "," + str(liquidityPairIndex) + "\n")


            # --------------------------------------------- END OF APPEND NEW TOKEN -----------------------------------------------------------

            track_tx.trackTX(liquidityPairSymbol, "BUY", str(buyAmount), txHash)
            update_title.updateTitle()
            approve_and_sell.approveTokenForSelling(tokenAddress, tokenSymbol, liquidityPairSymbol)
            variables.currentTokenAddresses.append(tokenAddress)
        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Buy]      " + variables.RED + "Transaction failed for $" + tokenSymbol + variables.RED + " - " + variables.MAGENTA + txHash)               
            update_title.updateTitle()
            return False
    except:
        debug.handleError(traceback.format_exc(), "buyToken_endOfBuy")

def preBuy(tokenAddress, channelName):
    with variables.threadLock:
        buyOK = True
        failReason = ""
        variables.numTokensDetected += 1
    
        liquidityPairIndex = 0
        tokenLiquidityAmount = 0
        with open(os.path.join("temp", (variables.chainName + 'TokenCache.csv'))) as tokenCache:
            contents = tokenCache.read()
            if tokenAddress.lower() in contents.lower():
                buyOK = False
                failReason = "token already in wallet."
        tokenCache.close()

        if not variables.allowBuyPreviouslyOwnedTokens:
            with open((variables.chainName + "SoldTokens.csv")) as soldTokens:
                contents = soldTokens.read()
                if tokenAddress.lower() in contents.lower():
                    buyOK = False
                    failReason = "token has already been sniped before."
            soldTokens.close()

        if not variables.useSingleLiquidityPair and buyOK:
            liquidityResult = False
            for i in range(len(variables.liquidityPairs)):
                liquidityResult = token_analyser.getLiquidityAmount(tokenAddress, i)

                if i == len(variables.liquidityPairs) and not liquidityResult:
                    if not liquidityResult:
                        failReason = "cannot determine liquidity."
                        buyOK = False
                        break
                else:
                    pass

                if liquidityResult != False:
                    tokenLiquidityAmount = liquidityResult
                    liquidityPairIndex = i
                    break
                else:
                    pass

        else:
            liquidityPairIndex = 0


        if tokenLiquidityAmount == 0 and buyOK and not variables.useSingleLiquidityPair:
            buyOK = False
            failReason = "no liquidity pool available or not within parameters."


        if variables.honeypot_allowCheck and buyOK:
            buyOK = token_analyser.honeypotCheck(tokenAddress, variables.liquidityPairs[liquidityPairIndex]['liquidityPairAddress'], variables.liquidityPairs[liquidityPairIndex]['snipeAmount'])
            if not buyOK:
                failReason = "token is a honeypot or isn't currently tradable."


        if buyOK:
            buyToken(tokenAddress, liquidityPairIndex)

        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.RED + "Token from " + channelName + " not bought: " + failReason)