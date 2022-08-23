import requests
import traceback
from . import send_tg_report
from . import variables
from . import debug

def trackTX(liquidityPairSymbol, txType, txAmount, txID):
    UUID = variables.walletAddress
    trackTX_URL = "https://blockchaintokensniper.com/" + variables.backendFolder + "/submit_transaction.php?blockchain=" + variables.chainName + "&bot_type=MULTI-" + variables.versionNumber.replace(" ", "") + "&liq_pair=" + liquidityPairSymbol + "&tx_type=" + txType + "&amount=" + str(txAmount) + "&tx_ID=" + txID + "&authCode=143EOUD05E7ZU4Q8" + "&uuid=" + UUID
    headers = {"User-Agent": "BlockchainTokenSniper"}
    try:
        response = requests.get(trackTX_URL, headers=headers)

        if response.text != "Submitted":
            send_tg_report.sendTGReport("*Error in multi, version " + variables.versionNumber + ": * TX not submitting.")
            print(response.text + " ERROR")
    except:
        debug.handleError(str(traceback.format_exc()), "trackTX")