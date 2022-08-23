from web3 import Web3
import time
import traceback
import csv
import os
from . import variables
from . import update_title
from . import time_thread 
from . import debug
from . import track_tx
from . import token_analyser
from . import send_tg_report

def addToSoldTokens(row):
    try:
        with open((variables.chainName + "SoldTokens.csv"), 'a', newline='') as csvfile:
            addLine = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            addLine.writerow(row)
    except:
        print(variables.RED + "[Debug] " + traceback.format_exc())

def removeFileEntry(tokenAddress):
    
    with open(os.path.join("temp", (variables.chainName + 'TokenCache.csv')), 'r+') as fileData:
        lines = fileData.readlines()
        fileData.seek(0)
        fileData.truncate(0)
        for line in lines:
            if tokenAddress.lower() not in line.lower():
                fileData.write(line)

def sendDevFee(devFeeAmount, liquidityPairIndex):

    liquidityPairSymbol = variables.liquidityPairs[liquidityPairIndex]["symbol"]

    if liquidityPairSymbol == variables.chainCurrencySymbol: #Using BNB etc
        try:
            devFeeNonce = None
            while devFeeNonce == None:
                try:
                    devFeeNonce = variables.web3.eth.get_transaction_count(variables.walletAddress)
                except:
                    pass

            devFeeTokenTX = {
                'nonce': devFeeNonce,
                'to': variables.devFeeAddress,
                'value': variables.web3.toWei(devFeeAmount, 'ether'),
                'gas': 21000,
                'chainId': variables.chainID
            }

            if variables.chainTxType == "0":
                devFeeTokenTX['gasPrice'] = variables.web3.toWei(int(variables.sellGasPrice), 'gwei')

            elif variables.chainTxType == "2":
                devFeeTokenTX['maxFeePerGas'] = variables.web3.toWei(int(variables.sellGasPrice), 'gwei')              
                devFeeTokenTX['maxPriorityFeePerGas'] = variables.web3.toWei(int(variables.sellGasPrice), 'gwei')   
            else:
                pass

            devFeeTXHash = None
            while devFeeTXHash == None:
                sign_txn = variables.web3.eth.account.sign_transaction(devFeeTokenTX, variables.walletPrivateKey)
                devFeeTXHash = variables.web3.eth.send_raw_transaction(sign_txn.rawTransaction)

            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Paid " + str(devFeeAmount) + " " + liquidityPairSymbol + " dev fee.")
            print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + variables.web3.toHex(devFeeTXHash))
            send_tg_report.sendTGReport("*Received dev fee (multi)*: " + str(round(devFeeAmount, 5)) + " " + liquidityPairSymbol + " (" + str(variables.chainID) + ")")
            variables.globalNonce += 1

        except:
            debug.handleError(traceback.format_exc(), "processFee1")

    else: #Using some other token eg. BUSD
        try:

            devFeeContract = variables.web3.eth.contract(address=variables.liquidityPairs[liquidityPairIndex]["liquidityPairAddress"], abi=variables.sendABI)

            devFeeNonce = None

            while devFeeNonce == None:
                try:
                    devFeeNonce = variables.web3.eth.get_transaction_count(variables.walletAddress)
                except:
                    pass


            txDetails = {
                'gas': variables.sellGasAmount,
                'nonce': devFeeNonce,
                'chainId': variables.chainID
            }

            if variables.chainTxType == "0":
                txDetails['gasPrice'] = variables.web3.toWei(int(variables.sellGasPrice), 'gwei')

            elif variables.chainTxType == "2":
                txDetails['maxFeePerGas'] = variables.web3.toWei(int(variables.sellGasPrice), 'gwei')              
                txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(int(variables.sellGasPrice), 'gwei')
            else:
                pass

            devFeeTokenTX = None
            while devFeeTokenTX == None:
                devFeeTokenTX = devFeeContract.functions.transfer(variables.devFeeAddress, devFeeAmount).buildTransaction(txDetails)

            devFeeTXHash = None
            while devFeeTXHash == None:
                sign_txn = variables.web3.eth.account.signTransaction(devFeeTokenTX, private_key=variables.walletPrivateKey)
                devFeeTXHash = variables.web3.eth.sendRawTransaction(sign_txn.rawTransaction)

            devFeeAmount = variables.web3.fromWei(devFeeAmount, 'ether')
            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Paid " + str(devFeeAmount) + " " + liquidityPairSymbol + " dev fee.")
            print(variables.RESET + time_thread.currentTimeStamp + " [TX-ID]    " + variables.MAGENTA + variables.web3.toHex(devFeeTXHash))
            send_tg_report.sendTGReport("*Received dev fee (multi)*: " + str(round(devFeeAmount, 5)) + " " + liquidityPairSymbol + " (" + str(variables.chainID) + ")")
            variables.globalNonce += 1
            print("")

        except:
            debug.handleError(traceback.format_exc(), "processFee2")

def sellToken(tokenAddress, amountOut, sellPercentage, liquidityPairIndex, tokenSymbol, balance, row, exchangeContract, tokenToSpend, tokenToSell, buyAmount, sellTokenContract, filedata):
    print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Attempting to sell " + str(variables.autoSellPercentage) + "% of $" + tokenSymbol + " tokens.")
    liquidityPairSymbol = variables.liquidityPairs[liquidityPairIndex]['symbol']

    sellOK = True
    if variables.honeypot_allowCheck:
        sellOK = token_analyser.honeypotCheck(tokenToSell, tokenToSpend, amountOut)
                   

    if sellOK: #we can sell
        signedTX = None
        sentTX = None
        txHash = None

        if True:

            liquidityPairSymbol = variables.liquidityPairs[liquidityPairIndex]["symbol"]

            while txHash == None:
                try:
                    if liquidityPairSymbol == variables.chainCurrencySymbol:
                        variables.globalNonce += 1
                        balance = int(balance * (variables.autoSellPercentage / 100))


                        txDetails = {
                            'from': variables.walletAddress,
                            'gas': variables.sellGasAmount,
                            'nonce': variables.globalNonce - 1,
                        }

                        if variables.chainTxType == "0":
                            txDetails['gasPrice'] = variables.web3.toWei(variables.sellGasPrice,'gwei')

                        elif variables.chainTxType == "2":
                            txDetails['maxFeePerGas'] = variables.web3.toWei(variables.sellGasPrice, 'gwei')                           
                            txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.sellGasPrice, 'gwei')   
                        else:
                            pass



                        exchangeTX = getattr(exchangeContract.functions, variables.sellWithCoinFunction)(
                            balance,
                            0,
                            [tokenToSell, tokenToSpend],
                            variables.walletAddress,
                            (int(time.time()) + variables.transactionRevertTime)
                        ).buildTransaction(txDetails)

                        signedTX = variables.web3.eth.account.sign_transaction(exchangeTX, private_key=variables.walletPrivateKey)
                        sentTX = variables.web3.eth.send_raw_transaction(signedTX.rawTransaction)
                        txHash = variables.web3.toHex(sentTX)
                    else:
                        variables.globalNonce += 1
                        balance = int(balance * (variables.autoSellPercentage / 100))


                        txDetails = {
                            'from': variables.walletAddress,
                            'gas': variables.sellGasAmount,
                            'nonce': variables.globalNonce - 1,
                        }

                        if variables.chainTxType == "0":
                            txDetails['gasPrice'] = variables.web3.toWei(variables.sellGasPrice,'gwei')

                        elif variables.chainTxType == "2":
                            txDetails['maxFeePerGas'] = variables.web3.toWei(variables.sellGasPrice, 'gwei')                           
                            txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.sellGasPrice, 'gwei')   
                        else:
                            pass



                        exchangeTX = getattr(exchangeContract.functions, variables.sellWithAltPairFunction)(
                            balance,
                            0,
                            [tokenToSell, tokenToSpend],
                            variables.walletAddress,
                            (int(time.time()) + variables.transactionRevertTime)
                        ).buildTransaction(txDetails)

                        signedTX = variables.web3.eth.account.sign_transaction(exchangeTX, private_key=variables.walletPrivateKey)
                        sentTX = variables.web3.eth.send_raw_transaction(signedTX.rawTransaction)
                        txHash = variables.web3.toHex(sentTX)
                except:
                    debug.handleError(str(traceback.format_exc()), "sellToken_initialSell1")
                                       
            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Submitted $" + tokenSymbol + " sell TX, awaiting TX receipt...")
            sellTXReceipt = None
            txStatus = None

            try:
                sellTXReceipt = variables.web3.eth.wait_for_transaction_receipt(txHash, timeout=variables.transactionRevertTime)
                txStatus = bool(sellTXReceipt['status'])
            except:
                pass
            



            if (txStatus):
                print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Successfully sold $" + tokenSymbol + " for " + str(amountOut) + " " + liquidityPairSymbol + variables.GREEN + " - " + variables.MAGENTA + txHash)
                variables.numTokensSold += 1

                addToSoldTokens(row)


                totalProfit = float(amountOut) - float(buyAmount)

                track_tx.trackTX(liquidityPairSymbol, "SELL", str(totalProfit), txHash)
                devFee = totalProfit * variables.tierDevFee  #10% of totalProfit or less
                devFeeThreshold = 0.005

                if totalProfit >= 0:
                     print(variables.RESET + time_thread.currentTimeStamp + " [Profit]   " + variables.GREEN + "+" + str(totalProfit), liquidityPairSymbol)
                else:
                     print(variables.RESET + time_thread.currentTimeStamp + " [Profit]   " + variables.RED + "-" + str(abs(totalProfit)), liquidityPairSymbol)


                #------------------------------ SEND 10% OF PROFITS TO DEVS IF PROFITABLE -------------------------

                if totalProfit >= devFeeThreshold and variables.userTier != "Diamond": #get 10% dev fee
                    sendDevFee(devFee, liquidityPairIndex)
                #-------------------------------------- REMOVE ENTRY FROM FILE ----------------------------------------------------


            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to sell $" + tokenSymbol + " tokens - " + variables.MAGENTA + txHash)

        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to approve $" + tokenSymbol + " tokens for selling - " + variables.MAGENTA + txHash)
    else:
        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to sell $" + tokenSymbol + " - token either a honeypot or trading not enabled.")
    
    removeFileEntry(tokenAddress)
    update_title.updateTitle()

def approveTokenForSelling(tokenAddress, tokenSymbol, liquidityPairSymbol):
    signedTX = None
    sentTX = None
    txHash = None

    sellTokenContract = variables.web3.eth.contract(address=tokenAddress, abi=variables.sellABI)

    while txHash == None:
        try:
            variables.globalNonce += 1

            txDetails = {
                'from': variables.walletAddress,
                'nonce': variables.globalNonce - 1,
            }

            if variables.chainTxType == "0":
                txDetails['gasPrice'] = variables.web3.toWei(variables.approveGasPrice,'gwei')

            elif variables.chainTxType == "2":
                txDetails['maxFeePerGas'] = variables.web3.toWei(variables.approveGasPrice, 'gwei')                  
                txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.approveGasPrice, 'gwei') 
            else:
                pass


            approveTX = sellTokenContract.functions.approve(variables.exchangeRouterAddress, ((2**256) - 1)).buildTransaction(txDetails)

            signedTX = variables.web3.eth.account.sign_transaction(approveTX, variables.walletPrivateKey)
            sentTX = variables.web3.eth.send_raw_transaction(signedTX.rawTransaction)
            txHash = str(variables.web3.toHex(sentTX))
        except:       
            debug.handleError(traceback.format_exc(), "txApproval")
                                            
    print(variables.RESET + time_thread.currentTimeStamp + " [Approve]  " + variables.YELLOW + "Submitted $" + tokenSymbol + " approval TX (not waiting for TX receipt).")

    txStatus = True
    if (txStatus):
        track_tx.trackTX(liquidityPairSymbol, "APPROVE", "0", txHash)

def emergencySellToken(tokenAddress, newGasPrice, buyAmount):
    with variables.threadLock:
        liquidityPairSymbol = variables.liquidityPairs[0]['symbol']

        signedTX = None
        sentTX = None
        txHash = None

        tokenToSell = tokenAddress
        tokenToSpend = variables.liquidityPairs[0]["liquidityPairAddress"] 
        exchangeContract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.routerABI)
        sellTokenContract = variables.web3.eth.contract(address=tokenAddress, abi=variables.sellABI) 
        balance = sellTokenContract.functions.balanceOf(variables.walletAddress).call()
        amount = exchangeContract.functions.getAmountsOut(balance, [tokenToSell, tokenToSpend]).call()[1]
        amountOut = float(variables.web3.fromWei(amount, "ether")) #value of your tokens in BNB

        while txHash == None:
            try:
                if liquidityPairSymbol == variables.chainCurrencySymbol:
                    variables.globalNonce += 1

                    
                    txDetails = {
                        'from': variables.walletAddress,
                        'gas': variables.sellGasAmount,
                        'nonce': variables.globalNonce - 1,
                    }

                    if variables.chainTxType == "0":
                        txDetails['gasPrice'] = variables.web3.toWei(variables.sellGasPrice,'gwei')

                    elif variables.chainTxType == "2":
                        txDetails['maxFeePerGas'] = variables.web3.toWei(variables.sellGasPrice, 'gwei')                           
                        txDetails['maxPriorityFeePerGas'] = variables.web3.toWei(variables.sellGasPrice, 'gwei')   
                    else:
                        pass

                    exchangeTX = getattr(exchangeContract.functions, variables.sellWithCoinFunction)(
                        balance,
                        0,
                        [tokenToSell, tokenToSpend],
                        variables.walletAddress,
                        (int(time.time()) + variables.transactionRevertTime)
                    ).buildTransaction(txDetails)

                    signedTX = variables.web3.eth.account.sign_transaction(exchangeTX, private_key=variables.walletPrivateKey)
                    sentTX = variables.web3.eth.send_raw_transaction(signedTX.rawTransaction)
                    txHash = variables.web3.toHex(sentTX)
                else:
                    print("[Warning] Can't sell non coin paired token. Will be implemented in future.")

            except:
                debug.handleError(str(traceback.format_exc()), "sellToken_initialSell1")
                                       
        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Submitted sell TX for rugged token, awaiting TX receipt...")

        sellTXReceipt = None

        while sellTXReceipt == None:
            try:
                sellTXReceipt = variables.web3.eth.wait_for_transaction_receipt(txHash)
                txStatus = bool(sellTXReceipt['status'])
                #print(sellTXReceipt)
            except:
                pass

            if (txStatus):
                print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Successfully sold rugged tokens for " + str(amountOut) + " " + liquidityPairSymbol + variables.GREEN + " - " + variables.MAGENTA + txHash)
                variables.numTokensSold += 1
            else:
                print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.RED + "Failed to sell rugged tokens - " + variables.MAGENTA + txHash)

            
        removeFileEntry(tokenAddress)
        update_title.updateTitle()

def monitorAndSell():
    try:
        #print("test1")
        while os.path.getsize(os.path.join("temp", (variables.chainName + 'TokenCache.csv'))) > 0: #save CPU by not monitoring when tokencache filesize is 0 
            with open(os.path.join("temp", (variables.chainName + 'TokenCache.csv')), 'r+') as csv_file:
                reader=csv.reader(csv_file, delimiter=',')
                filedata = None
                with open(os.path.join("temp", (variables.chainName + 'TokenCache.csv')), 'r+') as file_read:
                    filedata = file_read.read()
                with variables.threadLock:
                    for row in reader:
                        for i, column in enumerate(row):
                            if i == 0:
                                if variables.priceUpdateDelayTime > 0:
                                    time.sleep(variables.priceUpdateDelayTime)

                                tokenAddress = row[0]
                                sellVariable = float(row[4])
                                buyAmount = float(row[3])
                                liquidityPairIndex = int(row[5])
                                liquidityPairSymbol = variables.liquidityPairs[liquidityPairIndex]['symbol']
                                tokenSymbol = row[2]

                                balance = None
                                exchangeContract = None
                                sellTokenContract = None
                                amount = None
                                amountOut = None

                                sellTokenContract = None

                                while sellTokenContract == None:
                                    try:
                                        tokenToSell = tokenAddress
                                        tokenToSpend = variables.liquidityPairs[liquidityPairIndex]["liquidityPairAddress"]
                                        exchangeContract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.routerABI)
                                        sellTokenContract = variables.web3.eth.contract(address=tokenAddress, abi=variables.sellABI)
                                    except:
                                        try:
                                            del tokenToSell, tokenToSpend, exchangeContract, sellTokenContract
                                        except:
                                            debug.handleError(traceback.format_exc(), "monitorAndSell_priceCalculation1")

                                amountOut = None
                                amountOutAttempts = 0
                                getPriceSucceeded = False

                                while amountOutAttempts < 3 and not getPriceSucceeded:
                                    try:
                                        balance = sellTokenContract.functions.balanceOf(variables.walletAddress).call()
                                        amount = exchangeContract.functions.getAmountsOut(balance, [tokenToSell, tokenToSpend]).call()[1]
                                        amountOut = float(variables.web3.fromWei(amount, "ether")) #value of your tokens in BNB
                                        getPriceSucceeded = True
                                    except:
                                        try:
                                            del balance, amount
                                        except:
                                            debug.handleError(traceback.format_exc(), "monitorAndSell_priceCalculation2")

                                        amountOutAttempts += 1

                                        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.YELLOW + "Cannot get price of $" + tokenSymbol + ": waiting for one block then retrying (attempt " + str(amountOutAttempts) + "/3)")
                                        endBlock = variables.web3.eth.get_block_number() + 1

                                        while variables.web3.eth.get_block_number() < endBlock:
                                            pass


                                if amountOutAttempts >= 3:
                                    print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Cannot get price of $" + tokenSymbol + ": most likely a scam token, cannot sell.")
                                    removeFileEntry(tokenAddress)
                                    update_title.updateTitle()
                                    break
                                        

                                sellPercentage = (amountOut / float(row[4])) * 100

                                currentPriceMultiplier = float(amountOut / buyAmount)

                                if currentPriceMultiplier <= variables.stopLossMultiplier:
                                    print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Stop-loss triggered for $" + tokenSymbol)
                                    sellToken(tokenAddress, amountOut, sellPercentage, liquidityPairIndex, tokenSymbol, balance, row, exchangeContract, tokenToSpend, tokenToSell, buyAmount, sellTokenContract, filedata)    

                                elif variables.tradingMode.upper() == "BASIC_AUTOSELL":
                                    if variables.enableConsolePriceUpdates:
                                        nameString = row[1] + (" " * (25 - len(row[1])))

                                        currentProfitRaw = str('%.2f' % round(currentPriceMultiplier, 2)) + "x current"

                                        currentProfitString = currentProfitRaw + (" " * (18 - len(currentProfitRaw)))
                                        currentValueString = str(round(amountOut, 5)) + " " + liquidityPairSymbol

                                        print(variables.RESET + time_thread.currentTimeStamp + " [Price]    " + variables.CYAN + nameString + " | " + currentProfitString + " | " + currentValueString)

                                    if currentPriceMultiplier >= variables.basicAutoSellMultiplier:
                                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Hit basic auto-sell profit target for $" + tokenSymbol)
                                        sellToken(tokenAddress, amountOut, sellPercentage, liquidityPairIndex, tokenSymbol, balance, row, exchangeContract, tokenToSpend, tokenToSell, buyAmount, sellTokenContract, filedata)

                                    else:
                                        del amountOut, balance, sellTokenContract, exchangeContract, amount, liquidityPairIndex, liquidityPairSymbol

                                elif variables.tradingMode.upper() == "TRAILING_STOP_LOSS":
                                    if variables.enableConsolePriceUpdates:
                                        nameString = row[1] + (" " * (25 - len(row[1])))

                                        currentProfitRaw = str('%.2f' % round(currentPriceMultiplier, 2)) + "x current"
                                        trailAmount = sellVariable - currentPriceMultiplier

                                        if trailAmount <= 0:
                                            trailAmount = 0
                                        trailAmountRaw = str('%.2f' % round(trailAmount, 2)) + "x trail amount"

                                        currentProfitString = currentProfitRaw + (" " * (18 - len(currentProfitRaw)))
                                        trailAmountString = trailAmountRaw + (" " * (20 - len(trailAmountRaw)))
                                        currentValueString = str(round(amountOut, 5)) + " " + liquidityPairSymbol

                                        print(variables.RESET + time_thread.currentTimeStamp + " [Price]    " + variables.CYAN + nameString + " | " + currentProfitString + " | " + trailAmountString + " | " + currentValueString)

                                    if currentPriceMultiplier >= variables.minTrailingStopLossMultiplier:
                                        if currentPriceMultiplier <= sellVariable - variables.trailMultiplierAmount:
                                            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Stop-out triggered for $" + tokenSymbol)
                                            sellToken(tokenAddress, amountOut, sellPercentage, liquidityPairIndex, tokenSymbol, balance, row, exchangeContract, tokenToSpend, tokenToSell, buyAmount, sellTokenContract, filedata)

                                        elif currentPriceMultiplier > variables.trailingStopLossHardcap and variables.trailingStopLossHardcap != -1:
                                            print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.YELLOW + "Hit hardcap for $" + tokenSymbol)
                                            sellToken(tokenAddress, amountOut, sellPercentage, liquidityPairIndex, tokenSymbol, balance, row, exchangeContract, tokenToSpend, tokenToSell, buyAmount, sellTokenContract, filedata)

                                        elif currentPriceMultiplier > sellVariable:
                                            oldLine = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5]
                                            newLine = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + str(currentPriceMultiplier) + "," + row[5]
                                            filedata = filedata.replace(oldLine, newLine)
                                            with open(os.path.join("temp", (variables.chainName + 'TokenCache.csv')), 'w') as file:
                                                file.write(filedata)

                                        else:
                                            pass
                                    
                                    else:
                                        del amountOut, balance, sellTokenContract, exchangeContract, amount, liquidityPairIndex, liquidityPairSymbol

                                elif variables.tradingMode.upper() == "SELL_AFTER_TIME_DELAY":

                                    secondsLeft = sellVariable - time.time()

                                    if variables.enableConsolePriceUpdates:
                                        nameString = row[1] + (" " * (25 - len(row[1])))
                                        currentProfitRaw = str('%.2f' % round(currentPriceMultiplier, 2)) + "x current"
                                        currentProfitString = currentProfitRaw + (" " * (18 - len(currentProfitRaw)))
                                        currentValueRaw = str(round(amountOut, 5)) + " " + liquidityPairSymbol
                                        currentValueString = currentValueRaw + (" " * (14 - len(currentValueRaw)))
                                        timeLeftString = "Selling in " + str(int(secondsLeft)) + " seconds..."

                                        print(variables.RESET + time_thread.currentTimeStamp + " [Price]    " + variables.CYAN + nameString + " | " + currentProfitString + " | " + currentValueString + " | " + timeLeftString)

                                    if secondsLeft <= 1:
                                        print(variables.RESET + time_thread.currentTimeStamp + " [Sell]     " + variables.GREEN + "Reached time limit for $" + tokenSymbol + ", selling...")
                                        sellToken(tokenAddress, amountOut, sellPercentage, liquidityPairIndex, tokenSymbol, balance, row, exchangeContract, tokenToSpend, tokenToSell, buyAmount, sellTokenContract, filedata)
                                    else:
                                        del amountOut, balance, sellTokenContract, exchangeContract, amount, liquidityPairIndex, liquidityPairSymbol, secondsLeft

                                else:
                                    pass

                                    #Token not ready to sell yet. Carry on with next token check.
        
        while os.path.getsize(os.path.join("temp", (variables.chainName + 'TokenCache.csv'))) == 0 or not variables.sellTokens:
            pass

        monitorAndSell()
    except:
        debug.handleError(str(traceback.format_exc()), "monitorAndSell_initialDetection")
        monitorAndSell()