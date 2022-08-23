import time
import sys
import os
import datetime
from . import init_nonce
from . import variables
from . import quit
from . import time_thread
from . import send_tg_report


def doInsufficientBytesCheck():
    variables.insufficientBytesAttempts += 1
    if variables.insufficientBytesAttempts == 1:
        variables.firstInsufficientBytesTimestamp = datetime.datetime.now()
    if variables.insufficientBytesAttempts == 6:
        variables.lastInsufficientBytesTimestamp = datetime.datetime.now()
       
    if variables.insufficientBytesAttempts == 6:
        timeDifference = variables.lastInsufficientBytesTimestamp - variables.firstInsufficientBytesTimestamp 

        if timeDifference.seconds < 10:
            print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Cannot receive data from node. Try deleting token cache and/or editing config settings.")
            quit.quitSniper(True)

        variables.insufficientBytesAttempts = 0


def handleError(errorMsg, errorLocation):
    if "insufficient funds" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Insufficient funds: please add more funds / adjust gas settings.")
        quit.quitSniper(True)

    elif "PancakeLibrary: INSUFFICIENT_INPUT_AMOUNT" in errorMsg:
        pass

    elif "cannot schedule new futures" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Encountered internal node / bot error, restarting..." + variables.RESET)
        quit.quitSniper(False)

    elif "0 bytes read on a total of 2 expected bytes" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "IncompleteReadError: possible issue with node / internet connection...")

    elif "nonce too low" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Nonce too low.")
        init_nonce.initNonce()

    elif "120 seconds" in errorMsg:
        print("[Debug] TX receipt refresh in " + errorLocation)

    elif "web3.exceptions.ContractLogicError: execution reverted" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Execution reverted error...")

    elif "private use" in errorMsg:
        pass

    elif "closed abnormally" in errorMsg:
        pass

    elif "transaction underpriced" in errorMsg:
        print("[Debug] (Replacement) TX underpriced error in " + errorLocation)

    elif "Non-hexadecimal digit found" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Your private key is incorrect. Please ensure you are using a private key and not a seed phrase.")
        quit.quitSniper(True)

    elif "semaphore timeout period" in errorMsg:
        print("[Debug] Semaphore timeout error in " + errorLocation + ": Most likely an issue with your internet connection.")

    elif "InsufficientDataBytes:" in errorMsg:
        doInsufficientBytesCheck()


    elif "cannot call recv" in errorMsg:
        print("[Debug] Recv error in " + errorLocation)
        #connect_to_node.quickConnect()

    elif "websockets.exceptions.ConnectionClosedOK" in errorMsg:
        print("[Debug] ConnectionClosedOK error in " + errorLocation)

    elif "asyncio.exceptions.CancelledError" in errorMsg:
        print("[Debug] Asyncio cancelledError in " + errorLocation)

    elif "ConnectionResetError(10054" in errorMsg:
        print("[Debug] ConnectionResetError in " + errorLocation)

    elif "asyncio.exceptions.TimeoutError" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Timeout error: check your network connection.")

    elif "web3.exceptions.BadFunctionCallOutput" in errorMsg:
        pass

    elif "cannot unpack non-iterable NoneType object" in errorMsg and "repeatHoneypotCheck" in errorMsg:
        pass

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
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "ABI function not found. Please check that the ABIs you use are correct.")
        quit.quitSniper(True) 

    elif "Could not identify the intended function with name" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Could not identify the intended function in ABI. Please check that the ABIs you use are correct.")
        quit.quitSniper(True) 

    elif "KeyError: 'whitelistedText'" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Whitelisted text not found in config / config invalid. Please refer to user guide.")
        quit.quitSniper(True)
    elif "KeyError: 'blacklistedText'" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Blacklisted text not found in config / config invalid. Please refer to user guide.")
        quit.quitSniper(True)

    elif "FileNotFoundError" in errorMsg and "TokenCache" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Token cache file not found. Please make sure it is available or restart bot.")
        quit.quitSniper(True)

    elif "sqlite3.OperationalError: database is locked" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "TG database file locked. Check that you aren't running 2 instances of the bot on same chain at same time.")
        quit.quitSniper(True)

    elif "PermissionError: Errno 13 Permission denied" in errorMsg:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "File permission denied. Please check that your file permissions are set correctly.")
        quit.quitSniper(True)

    else:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Encountered unknown error, sending error report...")
        send_tg_report.sendTGReport("*Error report in multi*: " + variables.versionNumber + " - " + errorMsg)
        print("[Debug] Unhandled error in " + errorLocation + ": " + errorMsg)
        time.sleep(3)
    #time.sleep(1)