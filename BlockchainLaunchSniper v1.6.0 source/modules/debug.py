from . import variables
from . import quit
from . import time_thread
from . import init_nonce
from . import send_tg_report
import time
import datetime


def doFilterDebugCheck():
    variables.resetFilterAttempts += 1
    if variables.resetFilterAttempts == 1:
        variables.firstResetFilterTimestamp = datetime.datetime.now()
    if variables.resetFilterAttempts == 6:
        variables.sixthResetFilterTimestamp = datetime.datetime.now()
       
    if variables.resetFilterAttempts >= 6:
        timeDifference = variables.sixthResetFilterTimestamp - variables.firstResetFilterTimestamp

        if timeDifference.seconds < 20:
            print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Too many filter resets. Most likely is a problem with your node / internet connection. Please check your connections and restart.")
            quit.quitSniper(False)

        variables.resetFilterAttempts = 0

def doConnectionDebugCheck():
    variables.lostConnectionAttempts += 1
    if variables.lostConnectionAttempts == 1:
        variables.firstLostConnectionTimestamp = datetime.datetime.now()
    if variables.lostConnectionAttempts == 6:
        variables.sixthLostConnectionTimestamp = datetime.datetime.now()
        
    if variables.lostConnectionAttempts >= 6:
        timeDifference = variables.sixthLostConnectionTimestamp - variables.firstLostConnectionTimestamp

        if timeDifference.seconds < 20:
            print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Error with internet / node connection. Please ensure you can connect to node / network.")
            quit.quitSniper(False)

        variables.lostConnectionAttempts = 0

def doInsufficientInputAmountDebugCheck():
    variables.insufficientInputAmountAttempts += 1
    if variables.insufficientInputAmountAttempts == 1:
        variables.firstInsufficientInputAmountTimestamp = datetime.datetime.now()
    if variables.insufficientInputAmountAttempts == 6:
        variables.lastInsufficientInputAmountTimestamp = datetime.datetime.now()
        
    if variables.insufficientInputAmountAttempts >= 10:
        timeDifference = variables.lastInsufficientInputAmountTimestamp - variables.firstInsufficientInputAmountTimestamp

        if timeDifference.seconds < 20:
            print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "INSUFFICENT_INPUT_AMOUNT error: you may have too few tokens.")
            quit.quitSniper(True)

        variables.insufficientInputAmountAttempts = 0

def handleError(errorMsg, errorLocation):
    if "private use" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    4040 error in " + errorLocation + ": Please check your network / node connection is OK.")
    elif "insufficient funds" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Insufficient funds in wallet: Please add more " + variables.liquidityPairSymbol + " to your wallet.")
        quit.quitSniper(False)
    elif "nonce too low" in errorMsg:
        #print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    Nonce too low.")
        variables.resetNonceAttempts += 1
        init_nonce.initNonce()
        if variables.resetNonceAttempts == 10:
            print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Unable to calculate nonce. Check that a TX was not made involving your sniping wallet while bot was open.")
            quit.quitSniper(False)
    elif "closed abnormally" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    1006 error in " + errorLocation + ": Please check your network connection / node connection is OK.")
    elif "execution reverted" in errorMsg and "INSUFFICIENT_INPUT_AMOUNT" not in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    Execution reverted error in " + errorLocation)
    elif "filter not found" in errorMsg:
        doFilterDebugCheck()
    elif "websockets.exceptions.InvalidStatusCode" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    HTTP 429 error in " + errorLocation)
    elif "cannot call recv" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    RuntimeError Recv error in " + errorLocation)
    elif "INSUFFICIENT_INPUT_AMOUNT" in errorMsg:
        #print("test55")
        doInsufficientInputAmountDebugCheck() #pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    INSUFFICIENT_INPUT_AMOUNT error in " + errorLocation + " (usually temporary) - retrying...")
    elif "asyncio.exceptions.CancelledError" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    Asyncio cancelledError in " + errorLocation + ": Please check your network connection / node connection is OK.")
        doConnectionDebugCheck()
    elif "transaction underpriced" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    (replacement) TX underpriced error in " + errorLocation + ": retrying...")
    elif "exceptions.TimeoutError()" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    Asyncio Timeout error in " + errorLocation + ": Please check your network connection / node connection is OK.")
        doConnectionDebugCheck()
    elif "asyncio.exceptions.CancelledError" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    Asyncio Cancelled error in " + errorLocation + ": Please check your network connection / node connection is OK.")
        doConnectionDebugCheck()
    elif "Non-hexadecimal digit found" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Your private key is incorrect. Please make sure that you are using a private key and not a seed phrase.")
        quit.quitSniper(True)

    elif "web3.exceptions.BadFunctionCallOutput" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    Bad function output error in " + errorLocation + ": Possible issue with node.")

    elif "cannot unpack non-iterable NoneType object" in errorMsg and "repeatHoneypotCheck" in errorMsg:
        pass#print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    Unknown issue with honeypot checker. ")

    elif "An existing connection was forcibly closed by the remote host" in errorMsg:
        pass
    elif "Cannot convert None of type <class 'NoneType'> to bytes" in errorMsg:
        pass

    elif "requests.exceptions.ReadTimeout" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Timeout error: check node / internet connection.")

    elif "KeyboardInterrupt" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Keyboard interrupted: bot has been stopped.")
        quit.quitSniper(False) 

    elif "urllib3.exceptions.MaxRetryError" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Timeout error: check node / internet connection.")

    elif "ConnectionResetError" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Connection reset error: check node / internet connection.")

    elif "requests.exceptions.HTTPError" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Forbidden request error: check node / internet connection.")

    elif "requests.exceptions.ConnectionError" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Connection error: check node / internet connection.")

    elif "web3.exceptions.ABIFunctionNotFound" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "ABI function not found. Please check that the ABI you have used is correct.")

    elif "from field must match key's %s, but it was %s" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Your private key does not match your wallet address. Please make sure that you are using the correct private key.")
        quit.quitSniper(True)

    else:
        send_tg_report.sendTGReport("*Error report in launch*: " + variables.versionNumber + " - " + errorMsg)
        print(variables.RESET + time_thread.currentTimeStamp + " [Debug]    " + variables.YELLOW + "Unhandled error in " + errorLocation + " (please notify developers): " + errorMsg)