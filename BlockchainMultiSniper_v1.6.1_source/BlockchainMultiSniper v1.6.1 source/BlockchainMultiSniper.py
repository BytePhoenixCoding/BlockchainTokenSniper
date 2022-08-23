print("Loading...")

versionNumber = "v1.6.1"
backendFolder = "backend"

import threading
import warnings
import os
from web3 import Web3
from web3.auto import w3
from eth_account.messages import encode_defunct

from modules import variables
from modules import time_thread
from modules import connect_to_node
from modules import buy_token
from modules import approve_and_sell
from modules import update_title
from modules import token_cache
from modules import token_analyser
from modules import init_nonce
from modules import quit
from modules import telegram_listener
from modules import rug_monitor
from modules import check_authorisation

warnings.filterwarnings('ignore', message="Unverified HTTPS request")

variables.init()
variables.versionNumber = versionNumber
variables.backendFolder = backendFolder

timeStampThread = threading.Thread(target=time_thread.getTimestamp, )
timeStampThread.start()

connect_to_node.connect()
token_cache.setup_token_cache()
token_analyser.initFactoryContract()

if variables.honeypot_allowCheck:
    token_analyser.initHoneypotContract()

if variables.rugMonitoringEnabled:
    rug_monitor.startRugMonitor()

COLOUR = variables.chainLogoColour
RESET = variables.RESET

os.system("") # allows different colour text to be used in terminal


print(variables.RESET + '''
                                                .||||.  
                                                .||||.                                               
                                                .||||.                                               
                                                .||||.                                               
                                               .-||||-.                                              
                                      ..-:+||||--||||--||||+:-..                                     
                                  .-+|-||||||||||||||||||||||||-|+-.                                 
                  -|+.        ..+|||||||||-|||+.::::::.+|||-|||||||||+..        .+|-                 
                .||||-..    .+-||||||||:-.                  .-:||||||||-+.    ..-||||.               
                 -|||||-..  ..|||-|:.                            .:|-|||..  ..-|||||-                
                   -|||||-:   ..-                                    -..   :-|||||-                  
                     -|||||-:                     ''' + COLOUR + '''..''' + RESET + '''                     :-|||||-                    
                       :-|||||-                ''' + COLOUR + '''..||||..''' + RESET + '''                -|||||-:                      
                   .+.   :-|||||.           ''' + COLOUR + '''-+-||||||||-+-''' + RESET + '''           .|||||-:   .+.                  
                  ||||.   ..-|||:       ''' + COLOUR + '''.:|||||||-||-|||||||:.''' + RESET + '''       :|||-..   .||||                 
                .|||||:     .---.    ''' + COLOUR + '''..||||||||+..  ..+||||||||..''' + RESET + '''    .---.     :|||||.               
                |||||-           ''' + COLOUR + '''.-+-|||||||...        ...|||||||-+-.''' + RESET + '''           -|||||               
               |||||-        ''' + COLOUR + ''' .:|-|||||-|:.                .:|-|||||-|:.''' + RESET + '''         -|||||              
              :||||.         ''' + COLOUR + '''||||||||+-.                      .-+||||||||''' + RESET + '''         .||||:             
              -||||          ''' + COLOUR + '''||||||||:.                        .:||||||||''' + RESET + '''          ||||-             
             .||||.          ''' + COLOUR + '''|||||||||||+..                ..+|||||||||||''' + RESET + '''          .||||.            
             |||||           ''' + COLOUR + '''||||+:|||||||-|-.          .-|-|||||||:+||||''' + RESET + '''           |||||            
            .||||:           ''' + COLOUR + '''||||.  .:|-|||||||:.    .:|||||||-|:.  .||||''' + RESET + '''           :||||.           
 ...........:||||.           ''' + COLOUR + '''||||.      .+||||||||++||||||||+.      .||||''' + RESET + '''           .||||:...........
 ||||||||||||||||            ''' + COLOUR + '''||||.         .:||||||||||||:.         .||||''' + RESET + '''            ||||||||||||||||
 ||||||||||||||||            ''' + COLOUR + '''||||.             -||||||-             .||||''' + RESET + '''            ||||||||||||||||
 ...........:||||.           ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''           .||||:...........
            .||||:           ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''           :||||.           
             |||||           ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''           |||||            
             .||||.          ''' + COLOUR + '''||||.              .||||.              .||||''' + RESET + '''          .||||.            
              -||||          ''' + COLOUR + '''|||||..            .||||.            ..|||||''' + RESET + '''          ||||-             
              :||||.         ''' + COLOUR + '''||||||||+-.        .||||.        .-+||||||||''' + RESET + '''         .||||:             
               |||||-         ''' + COLOUR + '''.:|-|||||-|:.     .||||.     .:|-|||||-|:.''' + RESET + '''         -|||||              
                |||||-           ''' + COLOUR + '''.-+-|||||||... .||||. ...|||||||-+-.''' + RESET + '''           -|||||               
                .|||||:     .---.    ''' + COLOUR + '''..||||||||+:||||:+||||||||..''' + RESET + '''    .---.     :|||||.               
                  ||||.   ..-|||:       ''' + COLOUR + '''.:||||||||||||||||||:.''' + RESET + '''       :|||-..   .||||                 
                   .+.   :-|||||.           ''' + COLOUR + '''-+-||||||||-+-''' + RESET + '''           .|||||-:   .+.                  
                       :-|||||-                ''' + COLOUR + '''..||||..''' + RESET + '''                -|||||-:                      
                     -|||||-:                     ''' + COLOUR + '''..''' + RESET + '''                     :-|||||-                    
                   -|||||-:   ..-                                    -..   :-|||||-                  
                 -|||||-..  ..|||-|:.                            .:|-|||..  ..-|||||-                
                .||||-..    .+-||||||||:-.                  .-:||||||||-+.    ..-||||.               
                  -|+.        ..+|||||||||-|||+.::::::.+|||-|||||||||+..        .+|-                 
                                  .-+|-||||||||||||||||||||||||-|+-.                                 
                                      ..-:+||||--||||--||||+:-..                                     
                                               .-||||-.                                              
                                                .||||.                                               
                                                .||||.                                               
                                                .||||.                                               
                                                .||||.
    
''')

#----------------------- SETUP ACTIVE WALLET ADDRESS -----------------------------

print("")

signed_message = w3.eth.account.sign_message(encode_defunct(text="BlockchainTokenSniper"), private_key=Web3.toBytes(hexstr=variables.walletPrivateKey))

signedWalletAddress = w3.eth.account.recover_message(encode_defunct(text="BlockchainTokenSniper"), signature=signed_message.signature)

if signedWalletAddress != variables.walletAddress:
     print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Primary wallet address does not match private key.")
     quit.quitSniper(True)

connect_to_node.initAuthNode()
check_authorisation.checkAuth()

if variables.activeWalletAddress != None:
    variables.walletAddress = variables.activeWalletAddress
    variables.walletPrivateKey = variables.activeWalletPrivateKey

init_nonce.initNonce()
update_title.updateTitle()


#----------- SOME SETTING UP ------------------

print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Successfully connected to node.")
print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + "Using wallet address: " + variables.GREEN + variables.walletAddress)
print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.RED + "Do not make any other transactions involving your sniping wallet while bot is running. ")
print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + "Current tier: " + variables.GREEN + variables.userTier)

if not variables.buyTokens and not variables.sellTokens:
    print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "You cannot disable buying and selling at the same time!")
    quit.quitSniper(True)

if variables.tradingMode.upper() != "BASIC_AUTOSELL" and \
   variables.tradingMode.upper() != "TRAILING_STOP_LOSS" and \
   variables.tradingMode.upper() != "SELL_AFTER_TIME_DELAY":
    print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Unknown trading mode. Please refer to user guide.")
    quit.quitSniper(True)

if not variables.buyTokens:
    print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.YELLOW + "Token buying disabled.")

if not variables.sellTokens:
    print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.YELLOW + "Token selling disabled.")

if(variables.buyTokens and variables.totalAllowedSnipes != -1):
    print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.YELLOW + "Max " + str(variables.totalAllowedSnipes) + " snipe(s) allowed before buying stopped.")

print("")

if variables.buyTokens:
    channelNames = [] #create initial blank list

    for i in range(0, (len(variables.listeningChannels))):
        channelName = variables.listeningChannels[i]['channelName']
        channelNames.append(channelName)
    channelNames = tuple(channelNames)
    
    buy_token.initBuyTokenContract()

    startTGListenerThread = threading.Thread(target=telegram_listener.startTGListener, args=(channelNames, ))
    startTGListenerThread.start()


if variables.sellTokens and not variables.buyTokens:
    variables.threadLock = threading.Lock()
    monitorSellThread = threading.Thread(target=approve_and_sell.monitorAndSell, )
    monitorSellThread.start()
