from . import variables
from . import time_thread
from . import quit
from . import debug
import json
import traceback

def checkAuth():
    try:
        authContractABI = json.loads('[{"inputs":[{"internalType":"uint256","name":"tierID","type":"uint256"},{"internalType":"address","name":"refAddress","type":"address"}],"name":"buyTier","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tierID","type":"uint256"},{"internalType":"address","name":"refAddress","type":"address"}],"name":"upgradeTier","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"botLatestVersion","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"devFeeAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"tierDevFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"tierPrices","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userTier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
        authContractAddress = "0xf96Bcf9D4A340911f3fd735B56d11ad5cb6AD85d"

        authContract = variables.web3_auth.eth.contract(address=authContractAddress, abi=authContractABI)

        userTier = authContract.functions.userTier(variables.walletAddress).call()

        devFee = authContract.functions.tierDevFees(userTier).call()

        variables.devFeeAddress = authContract.functions.devFeeAddress().call()

        variables.tierDevFee = (devFee / 100)

        if userTier == 1:
            variables.userTier = "Free Trial"
            print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "Dev fees on profit are " + str(devFee) + "% for trial tier.")

        elif userTier == 2:
            variables.userTier = "Bronze"

        elif userTier == 3:
            variables.userTier = "Silver"

        elif userTier == 4:
            variables.userTier = "Gold"

        elif userTier == 5:
            variables.userTier = "Diamond"

        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "You do not have a tier. Please buy one from blockchaintokensniper.com/buy")
            quit.quitSniper(False)


        latestVersion = authContract.functions.botLatestVersion("LAUNCH").call()

        if(latestVersion != variables.versionNumber):
            print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "You are using version " + variables.versionNumber + ", however version " + latestVersion + " is available. Update from blockchaintokensniper.com.")
        else:
            print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "√ Version up to date.")
        print("")

    except:
        print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Authentication unsuccessful. Please reload bot and try again.")
        debug.handleError(traceback.format_exc(), "checkAuthMain")


