def init():
    from web3 import Web3
    import os
    import os.path
    import json
    import traceback
    import sys
    from . import quit
   
    global BLACK
    global RED
    global GREEN
    global YELLOW
    global BLUE
    global MAGENTA
    global CYAN
    global WHITE
    global ORANGE
    global UNDERLINE
    global RESET

    global versionNumber

    global web3
    global web3_auth

    global configData

    global numTokensDetected
    global numTokensBought
    global numTokensSold
    global walletBalance
    global foundTokenThreadBusy

    global routerABI
    global factoryABI
    global tokenNameABI
    global pairABI
    global sellABI
    global rugpullABI
    global tokenPairABI
    global tradingABI

    global exchangeRouterAddress
    global exchangeFactoryAddress
    global walletAddress
    global walletPrivateKey
    global blockchainNode
    global transactionRevertTime
    global liquidityPairSymbol

    global enableProxy
    global proxyType
    global proxyAddress
    global proxyPort

    global useProxyCredentials
    global proxyUsername
    global proxyPassword
    global useProxyRDNS

    global liquidityPairs

    global buyGasAmount
    global buyGasPrice
    global approveGasPrice
    global sellGasAmount
    global sellGasPrice

    global stopLossMultiplier

    global basicAutoSellMultiplier
    global enableBasicAutoSell

    global buyTokens
    global sellTokens
    global totalAllowedSnipes
    global autoSellPercentage
    global listeningChannels
    global api_hash
    global api_id

    global buyWithCoinFunction
    global buyWithAltPairFunction
    global sellWithCoinFunction
    global sellWithAltPairFunction
    global honeypotCheckerAddress

    global allowHoneypotCheck

    global honeypot_allowCheck
    global honeypot_maxBuyFee
    global honeypot_maxSellFee


    global globalNonce

    global sessionProfit

    global enableConsoleColours

    global userTier 
    global tierDevFee 
    global enableAds 
    global waitForAds 

    global threadLock
    global enableConsolePriceUpdates
    global allowBuyPreviouslyOwnedTokens
    global useSingleLiquidityPair

    global enableTrailingStopLoss
    global minTrailingStopLossMultiplier
    global trailMultiplierAmount 
    global trailingStopLossHardcap

    global priceUpdateDelayTime

    global scamFunctionHashes
    global rugMonitoringEnabled

    global currentTokenAddresses

    global tradingMode
    global sellAfterSeconds

    global chainID
    global chainName
    global chainCurrencySymbol 
    global chainLogoColour
    global chainTxType

    global insufficientBytesAttempts
    global firstInsufficientBytesTimestamp
    global lastInsufficientBytesTimestamp

    global devFeeGasPrice

    global adWaitTime

    global activeWalletAddress
    global activeWalletPrivateKey

    global backendFolder

    global devFeeAddress

    currentTokenAddresses = []

    scamFunctionHashesFile = open('scamFunctionHashes.lib') # Open file on read mode
    scamFunctionHashes = scamFunctionHashesFile.read().splitlines() # List with stripped line-breaks
    scamFunctionHashesFile.close() # Close file

    configFile = ""

    try:
        for i in sys.argv:
            if ".json" in i:
                configFile = i
                break
    except:
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
    web3_auth = None

    devFeeAddress = ""


    chainID = 0

    enableConsoleColours = eval(configData['miscellaneous']['enableConsoleColours'])

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
        ORANGE = '\033[38;5;202m'
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

    try:
        #------------------------ GENERAL SETTINGS ------------------------------------
        blockchainNode = configData['blockchainNode']

        #-------------------------- TELEGRAM SETTINGS -----------------------------

        enableProxy = eval(configData['telegramSettings']['proxySettings']['enableProxy'])
        proxyType = configData['telegramSettings']['proxySettings']['proxyType']
        proxyAddress = configData['telegramSettings']['proxySettings']['proxyAddress']
        proxyPort = configData['telegramSettings']['proxySettings']['proxyPort']
        useProxyCredentials = eval(configData['telegramSettings']['proxySettings']['useProxyCredentials'])
        proxyUsername = configData['telegramSettings']['proxySettings']['proxyUsername']
        proxyPassword = configData['telegramSettings']['proxySettings']['proxyPassword']
        useProxyRDNS = eval(configData['telegramSettings']['proxySettings']['useProxyRDNS'])

        api_id = configData['telegramSettings']['api_id']
        api_hash = configData['telegramSettings']['api_hash']

        #---------------------------- DEX SETTINGS --------------------------------

        routerABIFile = configData['exchangeSettings']['routerABI']
        factoryABIFile = configData['exchangeSettings']['factoryABI']

        exchangeRouterAddress = Web3.toChecksumAddress(configData['exchangeSettings']['routerAddress'])
        exchangeFactoryAddress = Web3.toChecksumAddress(configData['exchangeSettings']['factoryAddress'])

        routerABI = json.loads(open(os.path.join("ABI", routerABIFile)).read())
        factoryABI = json.loads(open(os.path.join("ABI", factoryABIFile)).read())
        tokenNameABI = json.loads(open(os.path.join("ABI", "functionsABI.json")).read())
        pairABI = json.loads(open(os.path.join("ABI", "pairABI.json")).read())
        sellABI = json.loads(open(os.path.join("ABI", "sellABI.json")).read())
        devFeeABI = json.loads(open(os.path.join("ABI", "sendABI.json")).read())
        tradingABI = json.loads(open(os.path.join("ABI", "tradingABI.json")).read())

        buyWithCoinFunction = configData['exchangeSettings']['buyWithCoinFunction']
        buyWithAltPairFunction = configData['exchangeSettings']['buyWithAltPairFunction']
        sellWithCoinFunction = configData['exchangeSettings']['sellWithCoinFunction']
        sellWithAltPairFunction = configData['exchangeSettings']['sellWithAltPairFunction']

        #------------------------GAS SETTINGS --------------------------------------

        buyGasAmount = int(configData['gasSettings']['buy_gasAmount'])
        buyGasPrice = int(configData['gasSettings']['buy_gasPrice'])
        approveGasPrice = int(configData['gasSettings']['approve_gasPrice'])
        sellGasAmount = int(configData['gasSettings']['sell_gasAmount'])
        sellGasPrice = int(configData['gasSettings']['sell_gasPrice'])

        #------------------------------ TRADING SETTINGS ------------------------------
        
        basicAutoSellMultiplier = float(configData['tradingSettings']['basicAutoSell']['autoSellMultiplier'])

        stopLossMultiplier = float(configData['tradingSettings']['stopLossMultiplier'])

        buyTokens = eval(configData['tradingSettings']['buyTokens'])
        sellTokens = eval(configData['tradingSettings']['sellTokens'])
        tradingMode = configData['tradingSettings']['tradingMode']
        totalAllowedSnipes = int(configData['tradingSettings']['totalAllowedSnipes'])
        autoSellPercentage = float(configData['tradingSettings']['autoSellPercentage'])
        allowBuyPreviouslyOwnedTokens = eval(configData['tradingSettings']['allowBuyPreviouslyOwnedTokens'])
        useSingleLiquidityPair = eval(configData['tradingSettings']['useSingleLiquidityPair'])
        transactionRevertTime = int(configData['tradingSettings']['transactionRevertTime'])
        minTrailingStopLossMultiplier = eval(configData['tradingSettings']['trailingStopLoss']['minTrailingStopLossMultiplier'])
        trailMultiplierAmount = eval(configData['tradingSettings']['trailingStopLoss']['trailMultiplierAmount'])
        trailingStopLossHardcap = eval(configData['tradingSettings']['trailingStopLoss']['trailingStopLossHardcap'])

        rugMonitoringEnabled = eval(configData['tradingSettings']['rugMonitoringEnabled'])


        sellAfterSeconds = int(configData['tradingSettings']['sellAfterTimeDelay']['sellAfterSeconds'])



        #------------------------------ HONEYPOT CHECKER SETTINGS ---------------------

        honeypot_allowCheck = eval(configData['honeypotCheckerSettings']['allowCheck'])
        honeypot_maxBuyFee = int(configData['honeypotCheckerSettings']['maxBuyFee'])
        honeypot_maxSellFee = int(configData['honeypotCheckerSettings']['maxSellFee'])

        if honeypot_allowCheck:
            honeypotCheckerAddress = Web3.toChecksumAddress(configData['honeypotCheckerSettings']['honeypotCheckerAddress'])
        else:
            honeypotCheckerAddress = None

        #------------------------------- LIQUIDITY PAIRS -----------------------------

        liquidityPairs = configData['liquidityPairs']

        #checksum all addresses in liquidity pairs

        for i in range(len(liquidityPairs)):
            liquidityPairs[i]['liquidityPairAddress'] = Web3.toChecksumAddress(liquidityPairs[i]['liquidityPairAddress'])

        listeningChannels = configData['telegramChannels']
        liquidityPairSymbol = configData['liquidityPairs'][0]['symbol']


        #-------------------------------- MISCELLANEOUS ---------------------------
        userTier = ""
        tierDevFee = 1

        enableConsolePriceUpdates = eval(configData['miscellaneous']['enableConsolePriceUpdates'])
        priceUpdateDelayTime = float(configData['miscellaneous']['priceUpdateDelayTime'])

        #------------------------------ OTHER NON CONFIG VARIABLES ---------------------

        numTokensDetected = 0
        numTokensBought = 0
        numTokensSold = 0
        walletBalance = 0

        threadLock = None

        monitorSellThread = None


        nonce = 0
        nonceInitialized = False



        chainID = None
        chainName = None
        chainCurrencySymbol = None
        chainLogoColour = None
        chainTxType = 0


        insufficientBytesAttempts = 0
        firstInsufficientBytesTimestamp = None
        lastInsufficientBytesTimestamp = None

        devFeeGasPrice = 0

        backendFolder = ""

        adWaitTime = 0
        globalNonce = -1
        sessionProfit = 0


    except:
        print("FATAL ERROR: Incorrectly configured config.json file.")
        print("Please check that it syntactically correct with no missing/extra colons, quotation marks, curly brackets or omitted entries, or that data types are correct, and restart the program.")
        print(traceback.format_exc())
        quit.quitSniper(True)

    versionNumber = ""
