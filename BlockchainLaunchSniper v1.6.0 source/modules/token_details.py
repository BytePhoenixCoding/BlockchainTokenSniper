from . import variables
from web3 import Web3
from . import debug
import traceback

def getTokenSymbol(tokenToBuy):   
    tokenSymbol = None
    while tokenSymbol == None:
        try:
            getTokenName = variables.web3.eth.contract(address=tokenToBuy, abi=variables.exchangeFunctionsABI)
            return getTokenName.functions.symbol().call().encode("ascii", "ignore").decode()
        except:
            debug.handleError(traceback.format_exc(), "getTokenSymbol")
            getTokenSymbol(tokenToBuy)