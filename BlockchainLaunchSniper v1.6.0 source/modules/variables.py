from web3 import Web3
import json
import fileinput
import os
import sys
import traceback
#import os.path

def init():
    global configData

    global walletAddress
    global walletPrivateKey

    global activeWalletAddress
    global activeWalletPrivateKey

    global addLiquidityFunctionHashes

    global blockchainNode

    global tokenSnipeAmount
    global transactionRevertTime

    global buy_gasAmount
    global buy_gasPrice
    global approve_gasPrice
    global sell_gasAmount
    global sell_gasPrice

    global liquidityPairAddress
    global antiBotDelay
    global tokenSymbol

    global snipeTokenAddress
    global snipeCompleted
    global honeypotCheck
    global nonCoinLiquidity

    global sellTokens

    global initialTokenPrice

    global specifiedTokenAmount

    global liquidityPairSymbol
    global devFeeThreshold
    global devFeeAddress
    global autoSellMultiplier

    global globalNonce

    global stopLossMultiplier

    global sellPercentage

    global initialBalance
    global finalBalance

    global enableHotkeys

    global enableConsoleColours

    global BLACK
    global RED
    global GREEN
    global YELLOW
    global BLUE
    global MAGENTA
    global CYAN
    global WHITE
    global UNDERLINE
    global RESET
    global ORANGE

    global web3

    global UUID

    global honeypot_maxBuyFee
    global honeypot_maxSellFee


    global exchangeRouterABI
    global exchangeFunctionsABI

    global sellABI
    global sendABI# =
    global tradingABI

    global exchangeRouterAddress
    global honeypotCheckerAddress
    global buyWithCoinFunction
    global buyWithAltPairFunction
    global sellWithAltPairFunction
    global sellWithCoinFunction

    global resetFilterAttempts
    global firstResetFilterTimestamp
    global sixthResetFilterTimestamp

    global lostConnectionAttempts
    global firstLostConnectionTimestamp
    global sixthLostConnectionTimestamp

    global resetNonceAttempts

    global insufficientInputAmountAttempts
    global firstInsufficientInputAmountTimestamp
    global lastInsufficientInputAmountTimestamp

    global keyboardListeningEnabled

    global snipeStateInitialised

    global userTier
    global tierDevFee
    global enableAds
    global waitForAds

    global enableTrailingStopLoss 
    global minTrailingStopLossMultiplier 
    global trailMultiplierAmount
    global trailingStopLossHardcap

    global chainID
    global chainName
    global chainCurrencySymbol 
    global chainLogoColour
    global chainTxType

    global devFeeGasPrice

    global versionNumber
    global backendFolder

    global web3_auth

    try:  
        
        configFile = None

        for argument in sys.argv:
            if ".json" in argument:
                configFile = argument
                break
        if configFile == None:
            configFile = "config.json"

        #check if config.json exists
        if not os.path.exists(configFile):
            input("ERROR: Config file does not exist. Please ensure config.json exists or use command line argument to specify config file.")
            exit()
            quit()

        configFilePath = os.path.join(os.path.abspath(''), configFile)

        with open(configFilePath, 'r', encoding='utf-8-sig') as configdata:
            configData = json.loads(configdata.read())

        web3 = None
        chainID = 0
        devFeeAddress = ""
        web3 = None
        web3_auth = None
        tokenSymbol = None
        
        
        walletAddress = configData['walletAddress']
        if walletAddress[0:2] != "0x" or len(walletAddress) != 42:
            print("[Error] " + "Incorrect wallet address format. Please resolve the issue and restart bot.")
            input()
            quit()
            exit()
        walletAddress = Web3.toChecksumAddress(walletAddress) 

        walletPrivateKey = configData['walletPrivateKey'] #private key is kept safe and only used in the program
        if len(walletPrivateKey) != 64 or " " in walletPrivateKey:
            print("[Error] " + "Incorrect private key format. Please resolve the issue and restart bot.")
            input()
            quit()
            exit()


        activeWalletAddress = None
        activeWalletPrivateKey = None

        try: 
            configData['activeWalletAddress'] #check it's defined
            configData['activeWalletPrivateKey']

            activeWalletAddress = configData['activeWalletAddress']
            if activeWalletAddress[0:2] != "0x" or len(activeWalletAddress) != 42:
                print("[Error] " + "Incorrect active wallet address format. Please resolve the issue and restart bot.")
                input()
                quit()
                exit()
            activeWalletAddress = Web3.toChecksumAddress(activeWalletAddress) 

            activeWalletPrivateKey = configData['activeWalletPrivateKey'] #private key is kept safe and only used in the program
            if len(activeWalletPrivateKey) != 64 or " " in activeWalletPrivateKey:
                print("[Error] " + "Incorrect active private key format. Please resolve the issue and restart bot.")
                input()
                quit()
                exit()

        except:
            pass
      


        UUID = str(walletAddress)
        blockchainNode = str(configData['blockchainNode'])

        globalNonce = -1

        nonCoinLiquidity = True



        #---------------------- EXCHANGE SETTING ---------------------------------------

        exchangeRouterAddress = Web3.toChecksumAddress(configData['exchangeSettings']['routerAddress'])
        buyWithCoinFunction = configData['exchangeSettings']['buyWithCoinFunction']
        buyWithAltPairFunction = configData['exchangeSettings']['buyWithAltPairFunction']
        sellWithCoinFunction = configData['exchangeSettings']['sellWithCoinFunction']
        sellWithAltPairFunction = configData['exchangeSettings']['sellWithAltPairFunction']

        exchangeRouterABI = json.loads(open(os.path.join("ABI", configData['exchangeSettings']['routerABI'])).read())
        exchangeFunctionsABI = json.loads(open(os.path.join("ABI", "functionsABI.json")).read())
        sellABI = json.loads(open(os.path.join("ABI", "sellABI.json")).read())
        sendABI = json.loads(open(os.path.join("ABI", "sendABI.json")).read())
        tradingABI = json.loads(open(os.path.join("ABI", "tradingABI.json")).read())


        #----------------------- GAS SETTINGS ---------------------------------

        buy_gasAmount = int(configData['gasSettings']['buy_gasAmount'])
        buy_gasPrice = int(configData['gasSettings']['buy_gasPrice'])
        approve_gasPrice = int(configData['gasSettings']['approve_gasPrice'])
        sell_gasAmount = int(configData['gasSettings']['sell_gasAmount'])
        sell_gasPrice = int(configData['gasSettings']['sell_gasPrice'])

        #----------------------- TRADING SETTINGS ------------------------------------

        liquidityPairAddress = Web3.toChecksumAddress(configData['tradingSettings']['liquidityPairAddress'])
        transactionRevertTime = int(configData['tradingSettings']['transactionRevertTime']) #number of seconds after transaction processes to cancel it if it hasn't completed
        stopLossMultiplier = float(configData['tradingSettings']['stopLossMultiplier'])
        sellTokens = eval(configData['tradingSettings']['sellTokens']) 

        enableTrailingStopLoss = eval(configData['tradingSettings']['trailingStopLoss']['enableTrailingStopLoss'])
        minTrailingStopLossMultiplier = float(configData['tradingSettings']['trailingStopLoss']['minTrailingStopLossMultiplier'])
        trailMultiplierAmount = float(configData['tradingSettings']['trailingStopLoss']['trailMultiplierAmount'])
        trailingStopLossHardcap = float(configData['tradingSettings']['trailingStopLoss']['trailingStopLossHardcap'])


        #ADD TRAILING STOP LOSS

        #----------------------- HONEYPOT CHECKER SETTINGS --------------------------

        honeypot_maxBuyFee = int(configData['honeypotCheckerSettings']['maxBuyFee'])
        honeypot_maxSellFee = int(configData['honeypotCheckerSettings']['maxSellFee'])
        honeypotCheckerAddress = configData['honeypotCheckerSettings']['honeypotCheckerAddress']

        if honeypotCheckerAddress != "":
            honeypotCheckerAddress = Web3.toChecksumAddress(honeypotCheckerAddress)

        #----------------------- MISCELLANEOUS SETTINGS ------------------------------

        enableHotkeys = eval(configData['miscellaneous']['enableHotkeys'])
        enableConsoleColours = eval(configData['miscellaneous']['enableConsoleColours'])

        #---------------------------------------------------------------------------------------------------------------





        if enableConsoleColours:
            BLACK = '\033[30m'
            RED = '\033[91m'#'\033[31m'
            GREEN = '\033[92m'#'\033[32m'
            YELLOW = '\033[93m'#'\033[33m'
            BLUE = '\033[34m'
            MAGENTA = '\033[95m'#'\033[35m'
            CYAN = '\033[96m'#'\033[36m'
            WHITE = '\033[37m'
            UNDERLINE = '\033[4m'
            RESET = '\033[0m'
            ORANGE = '\033[38;5;202m'#\033[202m'
        else:
            BLACK = ''
            RED = ''
            GREEN = ''
            YELLOW = ''
            BLUE = ''
            MAGENTA = ''
            CYAN = ''
            WHITE = ''
            UNDERLINE = ''
            RESET = ''
            ORANGE = ''

        addLiquidityFile = open('addLiquidityFunctionHashes.lib') # Open file on read mode
        addLiquidityFunctionHashes = addLiquidityFile.read().splitlines() # List with stripped line-breaks
        addLiquidityFile.close() # Close file

        userTier = None
        tierDevFee = 0.1
        enableAds = True
        waitForAds = True


        snipeTokenAddress = ""
        snipeCompleted = False
        tokenSnipeAmount = None
        initialTokenPrice = None
        autoSellMultiplier = None


        resetFilterAttempts = 0
        firstResetFilterTimestamp = None
        sixthResetFilterTimestamp = None

        lostConnectionAttempts = 0
        firstLostConnectionTimestamp = None
        sixthLostConnectionTimestamp = None

        insufficientInputAmountAttempts = 0
        firstInsufficientInputAmountTimestamp = None
        lastInsufficientInputAmountTimestamp = None

        chainID = None
        chainName = None
        chainCurrencySymbol = None
        chainLogoColour = None
        chainTxType = 0

        insufficientBytesAttempts = 0
        firstInsufficientBytesTimestamp = None
        lastInsufficientBytesTimestamp = None

        versionNumber = ""

        resetNonceAttempts = 0

        keyboardListeningEnabled = False

        devFeeGasPrice = 0

        devFeeThreshold = 0.005
        sellPercentage = None

        snipeStateInitialised = False

        backendFolder = ""
    except:
        print("[Error] " + "Incorrectly configured config.json file.")
        print("Please check that it syntactically correct with no missing/extra colons, quotation marks, curly brackets or omitted entries, or that data types are correct, and restart bot.")