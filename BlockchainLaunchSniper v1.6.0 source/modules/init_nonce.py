import traceback
from web3 import Web3
from . import variables
from . import time_thread
from . import debug

def initNonce():
    getNonce = False
    while getNonce == False:
        try:
            variables.globalNonce = variables.web3.eth.get_transaction_count(variables.walletAddress)
            getNonce = True
        except:
            debug.handleError(traceback.format_exc(), "initNonceMain")