import requests
import traceback
from . import debug
from . import variables
from . import send_tg_report
from . import time_thread

def trackTX(txType, txAmount, txID):
    versionNumber = variables.versionNumber.replace(" ", "")
    trackTX_URL = "https://blockchaintokensniper.com/" + variables.backendFolder + "/submit_transaction.php?blockchain=" + variables.chainName + "&bot_type=LAUNCH-" + versionNumber + "&liq_pair=" + variables.liquidityPairSymbol + "&tx_type=" + txType + "&amount=" + txAmount + "&uuid=" + variables.UUID + "&token_address=" + variables.snipeTokenAddress + "&tx_ID=" + txID + "&authCode=143EOUD05E7ZU4Q8&walletAddress=" + variables.walletAddress 
    #print(trackTX_URL)
    headers = {"User-Agent": "BlockchainTokenSniper"}
    response = None
    #print(trackTX_URL)
    try:
        response = requests.get(trackTX_URL, headers=headers)

        if "Submitted" not in str(response.text):
            send_tg_report.sendTGReport("*Error in launch, version " + variables.versionNumber + ": * TX not submitting.")
    except:
        debug.handleError(str(traceback.format_exc()), "trackTX")