from web3 import Web3
import traceback
from . import debug
from . import time_thread
from . import variables

checkHoneypotContract = None
factoryContract = None

def initFactoryContract():
    global factoryContract
    try:
        factoryContract = variables.web3.eth.contract(address=variables.exchangeFactoryAddress, abi=variables.factoryABI)
        while factoryContract == None:
            factoryContract = variables.web3.eth.contract(address=variables.exchangeFactoryAddress, abi=variables.factoryABI)
            print("[Debug] Reinitialising tokenAnalyser factory contract...")
    except:
        debug.handleError(traceback.format_exc(), "initFactoryContract")
        initFactoryContract()



def initHoneypotContract():
    global checkHoneypotContract
    try:
        honeypotContractAddress = variables.honeypotCheckerAddress #smart contract address
        checkHoneypotContract = variables.web3.eth.contract(address=honeypotContractAddress, abi=variables.tradingABI)
        pass
    except:
        debug.handleError(traceback.format_exc(), "initHoneypotContract")



def honeypotCheck(tokenAddress, liquidityPairAddress, tokenSnipeAmount):
    global checkHoneypotContract

    if variables.honeypot_allowCheck and tokenAddress != None:
        tokenAddress = tokenAddress
        try:                                   
            tokenInfo = checkHoneypotContract.functions.buy(liquidityPairAddress, tokenAddress).call({"value": Web3.toWei(tokenSnipeAmount, 'ether') })
            buy_tax = round((tokenInfo[0] - tokenInfo[1]) / tokenInfo[0] * 100)
            sell_tax = round((tokenInfo[3] - tokenInfo[4]) / tokenInfo[3] * 100)

            if buy_tax >= variables.honeypot_maxBuyFee or sell_tax >= variables.honeypot_maxSellFee:
                return False
            else:
                return True

        except:
            return False

        

def getLiquidityAmount(tokenAddress, liquidityPairIndex):
    liquidityPairAddress = variables.liquidityPairs[liquidityPairIndex]['liquidityPairAddress']
    minLiquidityAmount = float(variables.liquidityPairs[liquidityPairIndex]['minLiquidityAmount'])
    maxLiquidityAmount = float(variables.liquidityPairs[liquidityPairIndex]['maxLiquidityAmount'])
    liquidityPairSymbol = variables.liquidityPairs[liquidityPairIndex]['symbol']
    global factoryContract
    try:       
        pairAddress = None
        while pairAddress == None:
            try:
                pairAddress = factoryContract.functions.getPair(liquidityPairAddress, tokenAddress).call()
            except:
                debug.handleError(traceback.format_exc(), "getLiquidityAmountInit")
                #time.sleep(5)
        
        contract = variables.web3.eth.contract(address=pairAddress, abi=variables.pairABI)

        liqDecimals = 18

        liqPair0 = contract.functions.token0().call()
        if liqPair0 == liquidityPairAddress:
            reserves = contract.functions.getReserves().call()
            liquidityAmount0 = reserves[0] / (10 ** liqDecimals)

            if minLiquidityAmount != -1 and maxLiquidityAmount != -1:
                if liquidityAmount0 < minLiquidityAmount or liquidityAmount0 > maxLiquidityAmount:
                    return False
                else:
                    return liquidityAmount0
            else:
                return liquidityAmount0

        liqPair1 = contract.functions.token1().call()
        if liqPair1 == liquidityPairAddress:
            reserves = contract.functions.getReserves().call()
            liquidityAmount1 = reserves[1] / (10 ** liqDecimals)

            if minLiquidityAmount != -1 and maxLiquidityAmount != -1:
                if liquidityAmount1 < minLiquidityAmount or liquidityAmount1 > maxLiquidityAmount:
                    return False
                else:
                    return liquidityAmount1
            else:
                return liquidityAmount1
    except:
        return False



