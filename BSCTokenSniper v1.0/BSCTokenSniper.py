print("Loading...")

from web3 import Web3
import datetime 
import threading
import json
import asyncio
import requests
import time
import os
import sys
import ctypes

os.system("mode con: lines=32766")
os.system("") #allows different colour text to be used

class style(): # Class of different text colours - default is white
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(style.MAGENTA) #change following text to magenta

print(" ██████╗ ███████╗ ██████╗    ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗    ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ ")
print(" ██╔══██╗██╔════╝██╔════╝    ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║    ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗")
print(" ██████╔╝███████╗██║            ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║    ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝")
print(" ██╔══██╗╚════██║██║            ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║    ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗")
print(" ██████╔╝███████║╚██████╗       ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║    ███████║██║ ╚████║██║██║     ███████╗██║  ██║")
print(" ╚═════╝ ╚══════╝ ╚═════╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝    ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝")

print(style.WHITE)

ctypes.windll.kernel32.SetConsoleTitleW("BSCTokenSniper | Loading...")

currentTimeStamp = ""
def getTimestamp():
    while True:
        timeStampData = datetime.datetime.now()
        global currentTimeStamp
        currentTimeStamp = "[" + timeStampData.strftime("%H:%M:%S.%f")[:-3] + "]"
    
    

#-------------------------------- INITIALISE ------------------------------------------

timeStampThread = threading.Thread(target=getTimestamp)
timeStampThread.start()


numTokensDetected = 0
numTokensBought = 0
walletBalance = 0

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

if web3.isConnected():
    print(currentTimeStamp + " [Info] Web3 successfully connected")
    
#load json data

configFilePath = os.path.abspath('') + '\config.json'

with open(configFilePath, 'r') as configdata:
    data=configdata.read()

# parse file
obj = json.loads(data)

pancakeSwapRouterAddress = obj['pancakeSwapRouterAddress'] #load config data from JSON file into program
pancakeSwapFactoryAddress = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73' #read from JSON later
walletAddress = obj['walletAddress']
private_key = obj['walletPrivateKey'] #private key is kept safe and only used in the program

snipeBNBAmount = float(obj['amountToSpendPerSnipe'])
transactionRevertTime = int(obj['transactionRevertTimeSeconds']) #number of seconds after transaction processes to cancel it if it hasn't completed
gasAmount = int(obj['gasAmount'])
gasPrice = int(obj['gasPrice'])
bscScanAPIKey = obj['bscScanAPIKey']
observeOnly = obj['observeOnly']

checkSourceCode = obj['checkSourceCode']
checkValidPancakeV2 = obj['checkValidPancakeV2']
checkMintFunction = obj['checkMintFunction']
checkHoneypot = obj['checkHoneypot']
checkPancakeV1Router = obj['checkPancakeV1Router']

enableMiniAudit = False

if checkSourceCode == "True" and (checkValidPancakeV2 == "True" or checkMintFunction == "True" or checkHoneypot == "True" or checkPancakeV1Router == "True"):
    enableMiniAudit = True

def updateTitle():
    walletBalance = web3.fromWei(web3.eth.get_balance(walletAddress),'ether') #There are references to ether in the code but it's set to BNB, its just how Web3 was originally designed
    walletBalance = round(walletBalance, -(int("{:e}".format(walletBalance).split('e')[1]) - 4)) #the number '4' is the wallet balance significant figures + 1, so shows 5 sig figs
    ctypes.windll.kernel32.SetConsoleTitleW("BSCTokenSniper | Tokens Detected: " + str(numTokensDetected) + " | Tokens Bought: " + str(numTokensBought) + " | Wallet Balance: " + str(walletBalance) + " BNB")

updateTitle()


print(currentTimeStamp + " [Info] Using Wallet Address: " + walletAddress)
print(currentTimeStamp + " [Info] Using Snipe Amount: " + str(snipeBNBAmount), "BNB")

pancakeABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
listeningABI = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
tokenNameABI = json.loads('[ { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "spender", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "to", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "_owner", "type": "address" }, { "internalType": "address", "name": "spender", "type": "address" } ], "name": "allowance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "spender", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "approve", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "account", "type": "address" } ], "name": "balanceOf", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "decimals", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getOwner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "name", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "symbol", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "totalSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transfer", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transferFrom", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')




#------------------------------------- BUY SPECIFIED TOKEN ON PANCAKESWAP ----------------------------------------------------------


    

def Buy(tokenAddress, tokenSymbol):
    if(tokenAddress != None):
        tokenToBuy = web3.toChecksumAddress(tokenAddress)
        spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  #wbnb contract address
        contract = web3.eth.contract(address=pancakeSwapRouterAddress, abi=pancakeABI)
        nonce = web3.eth.get_transaction_count(walletAddress)
        start = time.time()
        pancakeswap2_txn = contract.functions.swapExactETHForTokens(
        0, # Set to 0 or specify min number of tokens - setting to 0 just buys X amount of token at its current price for whatever BNB specified
        [spend,tokenToBuy],
        walletAddress,
        (int(time.time()) + transactionRevertTime)
        ).buildTransaction({
        'from': walletAddress,
        'value': web3.toWei(float(snipeBNBAmount), 'ether'), #This is the Token(BNB) amount you want to Swap from
        'gas': gasAmount,
        'gasPrice': web3.toWei(gasPrice,'gwei'),
        'nonce': nonce,
        })

        try:
            signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction) #BUY THE TOKEN
        except:
            print(style.RED + currentTimeStamp + " Transaction failed.")
            print("") # line break: move onto scanning for next token
    
        txHash = str(web3.toHex(tx_token))


        #TOKEN IS BOUGHT

        checkTransactionSuccessURL = "https://api.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash=" + txHash + "&apikey=" + bscScanAPIKey
        checkTransactionRequest = requests.get(url = checkTransactionSuccessURL)
        txResult = checkTransactionRequest.json()['status']


        if(txResult == "1"):
            print(style.GREEN + currentTimeStamp + " Successfully bought $" + tokenSymbol + " for " + style.BLUE + str(snipeBNBAmount) + style.GREEN + " BNB - TX ID: ", txHash)

        else:
            print(style.RED + currentTimeStamp + " Transaction failed: likely not enough gas.")

        updateTitle()

    
buyTokenThread = threading.Thread(target=Buy(None, None))
buyTokenThread.start()




#------------------------------------- LISTEN FOR TOKENS ON BINANCE SMART CHAIN THAT HAVE JUST ADDED LIQUIDITY ----------------------------------------------------------


contract = web3.eth.contract(address=pancakeSwapFactoryAddress, abi=listeningABI)

print(currentTimeStamp + " [Info] Scanning for new tokens...")
print("") #line break



def foundToken(event):
    try:
        jsonEventContents = json.loads(Web3.toJSON(event))
        if(jsonEventContents['args']['token1'] == "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"): #check if pair is WBNB, if not then ignore it
            tokenAddress = jsonEventContents['args']['token0']
       
            getTokenName = web3.eth.contract(address=tokenAddress, abi=tokenNameABI) #code to get name and symbol from token address

            tokenName = getTokenName.functions.name().call()
            tokenSymbol = getTokenName.functions.symbol().call()
            print(style.YELLOW + currentTimeStamp + " [Token] New potential token detected: " + style.CYAN + tokenName + " (" + tokenSymbol + "): " + style.MAGENTA + tokenAddress + style.RESET)
            global numTokensDetected
            global numTokensBought
            numTokensDetected = numTokensDetected + 1 
            updateTitle()


         #--------------------------------------------MINI AUDIT FEATURE-------------------------------------------------------

            if(enableMiniAudit == True): #enable mini audit feature: quickly scans token for potential features that make it a scam / honeypot / rugpull etc
                print(style.YELLOW + "[Token] Starting Mini Audit...")
                contractCodeGetRequestURL = "https://api.bscscan.com/api?module=contract&action=getsourcecode&address=" + tokenAddress + "&apikey=" + bscScanAPIKey
                contractCodeRequest = requests.get(url = contractCodeGetRequestURL)
                tokenContractCode = contractCodeRequest.json()

                if(str(tokenContractCode['result'][0]['ABI']) == "Contract source code not verified") and checkSourceCode == "True": #check if source code is verified
                    print(style.RED + "[FAIL] Contract source code isn't verified.")

                elif ("0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F" in str(tokenContractCode['result'][0]['SourceCode'])) and checkPancakeV1Router == "True": #check if pancakeswap v1 router is used
                    print(style.RED + "[FAIL] Contract uses PancakeSwap v1 router.")


                elif (str(pancakeSwapRouterAddress) not in str(tokenContractCode['result'][0]['SourceCode'])) and checkValidPancakeV2 == "True": #check if pancakeswap v2 router is used
                    print(style.RED + "[FAIL] Contract doesn't use valid PancakeSwap v2 router.")

                elif "mint" in str(tokenContractCode['result'][0]['SourceCode']) and checkMintFunction == "True": #check if any mint function enabled
                    print(style.RED + "[FAIL] Contract has mint function enabled.")


                elif ("function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool)" in str(tokenContractCode['result'][0]['SourceCode']) or "function _approve(address owner, address spender, uint256 amount) internal" in str(tokenContractCode['result'][0]['SourceCode']) or "newun" in str(tokenContractCode['result'][0]['SourceCode'])) and checkHoneypot == "True": #check if token is honeypot
                    print(style.RED + "[FAIL] Contract is a honeypot.")

                else:
                    print(style.GREEN + "[SUCCESS] Token has passed mini audit.") #now you can buy
                    numTokensBought = numTokensBought + 1
                    if(observeOnly == "False"):
                        Buy(tokenAddress, tokenSymbol)
                        updateTitle()
                    
                    

              

            else: #we dont care about audit, just buy it
                if(observeOnly == "False"):
                    Buy(tokenAddress, tokenSymbol)
                    numTokensBought += 1
                    updateTitle()
                    
            print("") # line break: move onto scanning for next token

    except:
        pass

                

      
      #------------------------------------END OF MINI AUDIT FEATURE---------------------------------------------------------------
        
        
        
#-----------------------------------------TOKEN SCANNER BACKGROUND CODE----------------------------------------------------------------------
        
async def tokenLoop(event_filter, poll_interval):
    while True:
        try:
            for PairCreated in event_filter.get_new_entries():
                foundToken(PairCreated)
            await asyncio.sleep(poll_interval)
        except:
            pass
            
            


def listenForTokens():
    event_filter = contract.events.PairCreated.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                tokenLoop(event_filter, 0)))       
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
                 
    finally:
        # close loop to free up system resources
        #loop.close()
        #print("loop close")
        listenForTokens()

        #beware of valueerror code -32000 which is a glitch. make it ignore it and go bakc to listening



listenForTokens()

input("")
#------------------------------------------END OF TOKEN SCANNER BACKGROUND CODE---------------------------------------------------------------------



