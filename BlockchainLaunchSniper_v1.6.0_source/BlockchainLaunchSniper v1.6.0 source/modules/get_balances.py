from web3 import Web3
from . import variables
import threading
from . import time_thread

def getFinalBalance(init):
    if init:
        variables.finalBalance = 0
        while variables.finalBalance == 0:
            pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    " + variables.YELLOW + "Getting final balance...")
            try:
                if variables.nonCoinLiquidity == True:
                    sellTokenContract = variables.web3.eth.contract(address=variables.liquidityPairAddress, abi=variables.sellABI)
                    variables.finalBalance = float(variables.web3.fromWei(sellTokenContract.functions.balanceOf(variables.walletAddress).call(), 'ether'))
                else:
                    variables.finalBalance = float(variables.web3.fromWei(variables.web3.eth.getBalance(variables.walletAddress), 'ether'))
                #del sellTokenContract
            except:
                pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    " + variables.YELLOW + "Reattempting final balance...")      