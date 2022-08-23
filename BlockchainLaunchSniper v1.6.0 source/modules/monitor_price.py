from web3 import Web3
import os
import traceback
import webbrowser
import time
from . import variables
from . import sell_token
from . import time_thread
from . import sell_token
from . import debug
from . import resume_snipe

def manualMonitorAndSell():
    tokenToSell = variables.snipeTokenAddress
    tokenToSpend = variables.liquidityPairAddress           
    contract = variables.web3.eth.contract(address=variables.exchangeRouterAddress, abi=variables.exchangeRouterABI)
    sellTokenContract = variables.web3.eth.contract(address=tokenToSell, abi=variables.sellABI)
    while variables.snipeCompleted == False:
        try:    
            if variables.sellPercentage != None and variables.sellPercentage > 0:
                variables.snipeCompleted = True
                print("")
                sell_token.sellToken(int(variables.sellPercentage))
                variables.sellPercentage = None #stop from selling again

            balance = sellTokenContract.functions.balanceOf(variables.walletAddress).call()
            amountOut = float(variables.web3.fromWei((contract.functions.getAmountsOut(balance, [tokenToSell, tokenToSpend]).call())[1], "ether"))

            if variables.initialTokenPrice == None:
                variables.initialTokenPrice = amountOut
                
            if variables.snipeStateInitialised == False:
                resume_snipe.writeSnipeState()
                variables.snipeStateInitialised = True


            #--------------------- CALCULATE + DISPLAY PROFIT ----------------------------------------

            tokenPriceMultiplier = None
            tokenPriceMultiplier = float(amountOut / variables.initialTokenPrice)

            profitPercentage = round((((amountOut / variables.initialTokenPrice) * 100) - 100), 5)

            priceMultiplierString = str(round(tokenPriceMultiplier, 6)) + "x"
            balanceString = str(round(amountOut, 6)) + " " + variables.liquidityPairSymbol

            if len(priceMultiplierString) < 12:
                priceMultiplierString += (" " * int(12 - len(priceMultiplierString)))

            if len(balanceString) < 16:
                balanceString += (" " * int(16 - len(balanceString)))
             

            #print("test3")
            if variables.sellPercentage == None: #if we have nothing to sell
                print(variables.RESET + time_thread.currentTimeStamp + " [Price]    " +  variables.CYAN + priceMultiplierString + " | " + balanceString + " | " + str(profitPercentage) + "%")
             
            #-----------------------------------------------------------------------------------------                              


            #deal with trailing stop loss
            if variables.enableTrailingStopLoss and tokenPriceMultiplier >= variables.minTrailingStopLossMultiplier:
                highestPriceMultiplier = None
                #get current highestPriceMultiplier

                with open(os.path.join("temp", (variables.chainName + "SnipeState.tmp")), 'r+') as snipeState:
                    snipeState.seek(0)
                    snipeStateString = snipeState.read()
                    if snipeStateString != "":
                        parameters = snipeStateString.split(',')
                        highestPriceMultiplier = float(parameters[3])

                if tokenPriceMultiplier <= highestPriceMultiplier - variables.trailMultiplierAmount:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.YELLOW + "Stop-out triggered")
                    sell_token.sellToken(100)

                elif tokenPriceMultiplier > variables.trailingStopLossHardcap and variables.trailingStopLossHardcap != -1:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.YELLOW + "Hardcap reached")
                    sell_token.sellToken(100)

                elif tokenPriceMultiplier > highestPriceMultiplier:
                    #update config with highest price multiplier

                    with open(os.path.join("temp", (variables.chainName + "SnipeState.tmp")), 'w+') as snipeState:
                        snipeState.seek(0)
                        snipeStateString = variables.snipeTokenAddress + "," + variables.liquidityPairAddress + "," + str(variables.initialTokenPrice) + "," + str(tokenPriceMultiplier)
                        snipeState.write(snipeStateString)
                    #move on
                else:
                    del highestPriceMultiplier                              

            else:
                del amountOut, balance
                    #Token not ready to sell yet. Carry on with next token check.
                if tokenPriceMultiplier <= variables.stopLossMultiplier and variables.stopLossMultiplier != 0:
                    print(variables.RESET + time_thread.currentTimeStamp + " [Price]    " +  variables.CYAN + priceMultiplierString + " | " + balanceString + " | " + str(profitPercentage) + "%")
                    print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.RED + "Reached stop loss target, selling...")
                    sell_token.sellToken(100)

                elif variables.autoSellMultiplier != None and not variables.enableTrailingStopLoss:
                    if tokenPriceMultiplier >= variables.autoSellMultiplier:
                        print(variables.RESET + time_thread.currentTimeStamp + " [Price]    " +  variables.CYAN + priceMultiplierString + " | " + balanceString + " | " + str(profitPercentage) + "%")
                        print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Reached profit target, selling...")
                        sell_token.sellToken(100)
                else:
                    pass

        except:
            debug.handleError(str(traceback.format_exc()), "general_manualMonitorAndSell")
            manualMonitorAndSell()
   