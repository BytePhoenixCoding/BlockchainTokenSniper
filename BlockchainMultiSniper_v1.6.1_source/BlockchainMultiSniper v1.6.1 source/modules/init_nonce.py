from . import variables
import traceback
from . import debug

def initNonce():
    variables.globalNonce = None
    try:
        variables.globalNonce = variables.web3.eth.get_transaction_count(variables.walletAddress)      
    except:
        debug.handleError(traceback.format_exc(), "initNonce")
        initNonce()



