from telethon import TelegramClient, events, sync
from telethon.sync import TelegramClient
from telethon.tl.types import MessageEntityTextUrl
from web3 import Web3
import traceback
import asyncio
import threading
import os
from . import debug
from . import quit
from . import approve_and_sell
from . import variables
from . import time_thread
from . import buy_token
from . import send_tg_report


def startTGListener(channelNames):
    try:
        sessionFilePath = os.path.join("temp", (variables.chainName + "MultiSniper"))
        tgProxy = ""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = None
        if variables.enableProxy:
            txProxy = None

            if variables.useProxyRDNS:
                if variables.useProxyCredentials:
                    txProxy = {
                        'proxy_type': variables.proxyType, # (mandatory) protocol to use (see above)
                        'addr': variables.proxyAddress,      # (mandatory) proxy IP address
                        'port': variables.proxyPort,           # (mandatory) proxy port number
                        'username': variables.proxyUsername,      # (optional) username if the proxy requires auth
                        'password': variables.proxyPassword,      # (optional) password if the proxy requires auth
                        'rdns': True           # (optional) whether to use remote or local resolve, default remote
                    }
                else:
                    txProxy = {
                        'proxy_type': variables.proxyType, # (mandatory) protocol to use (see above)
                        'addr': variables.proxyAddress,      # (mandatory) proxy IP address
                        'port': variables.proxyPort,           # (mandatory) proxy port number
                        'rdns': True                          # (optional) whether to use remote or local resolve, default remote
                    }
            else:
                if variables.useProxyCredentials:
                    txProxy = {
                        'proxy_type': variables.proxyType, # (mandatory) protocol to use (see above)
                        'addr': variables.proxyAddress,      # (mandatory) proxy IP address
                        'port': variables.proxyPort,           # (mandatory) proxy port number
                        'username': variables.proxyUsername,      # (optional) username if the proxy requires auth
                        'password': variables.proxyPassword,      # (optional) password if the proxy requires auth
                        'rdns': False           # (optional) whether to use remote or local resolve, default remote
                    }
                else:
                    txProxy = {
                        'proxy_type': variables.proxyType, # (mandatory) protocol to use (see above)
                        'addr': variables.proxyAddress,      # (mandatory) proxy IP address
                        'port': variables.proxyPort,           # (mandatory) proxy port number
                        'rdns': False           # (optional) whether to use remote or local resolve, default remote
                    }

            client = TelegramClient(sessionFilePath, variables.api_id, variables.api_hash, loop=loop, proxy=tgProxy)
        else:
            client = TelegramClient(sessionFilePath, variables.api_id, variables.api_hash, loop=loop)#establish connection

        variables.threadLock = threading.Lock()

        @client.on(events.NewMessage(channelNames))
        async def normal_handler(event):
            msg=event.message.to_dict()['message'] #get message

            #print(msg)
            for url_entity, inner_text in event.message.get_entities_text(MessageEntityTextUrl):
                url = url_entity.url
                msg += url

            channelName = await client.get_entity(event.message.to_dict()['peer_id']['channel_id'])
            channelName = channelName.username

            allowedToSnipe = True
            if variables.totalAllowedSnipes != -1 and variables.numTokensBought >= variables.totalAllowedSnipes:
                allowedToSnipe = False

            #print("something happnd", str(allowedToSnipe))

            failReason = "unknown error."
            try:
                if allowedToSnipe:
                    tokenAddress = ""
                    try:
                        tokenAddress = Web3.toChecksumAddress("0x" + msg.split("0x",1)[1][:40]) #gets the CA from the message
                    except:
                        isPostValid = False
                        failReason = "unable to determine token address."


                    whitelistedText = []
                    blacklistedText = []

                    for i in range(0, len(variables.listeningChannels)):
                        if variables.listeningChannels[i]['channelName'] == channelName:
                            whitelistedText = variables.listeningChannels[i]['whitelistedText']
                            blacklistedText = variables.listeningChannels[i]['blacklistedText']

                    isPostValid = True
                    for i in range(0, len(whitelistedText)):
                        if whitelistedText[i] in msg:
                            pass
                        else:
                            isPostValid = False
                            failReason = "post does not contain required whitelisted text."

                    for i in range(0, len(blacklistedText)):
                        if blacklistedText[i] in msg:
                            #print(whitelistedText[i] + " in msg")
                            isPostValid = False
                            failReason = "post contains forbidden blacklisted text."
                        else:
                            pass

                    if isPostValid:
                        buyTokenThread = threading.Thread(target=buy_token.preBuy, args=(tokenAddress, channelName, ))
                        buyTokenThread.start()

                    else:
                        print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.RED + "Invalid post received from " + channelName + ": " + failReason)

            except:
                print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.RED + "Invalid post received from " + channelName + ": " + failReason)
                if failReason == "unknown error.":
                    debug.handleError(traceback.format_exc(), 'tgListenMain')

        try:
            client.connect()
            while not client.is_user_authorized():
                try:
                    phoneNumber = input(variables.RESET + time_thread.currentTimeStamp + " [Telegram] " + variables.GREEN + "Please enter your phone number or bot token: ")
                    client.send_code_request(phoneNumber)
                    try:
                        client.sign_in(phoneNumber, input(variables.RESET + time_thread.currentTimeStamp + " [Telegram] " + variables.GREEN + "Please enter the login code sent to your Telegram client: "))
                    except:
                        client.sign_in(password=input(variables.RESET + time_thread.currentTimeStamp + " [Telegram] " + variables.GREEN + "Please enter your Telegram 2FA password: "))
                except:
                    pass
        except:
            debug.handleError(traceback.format_exc(), "tgLogin")
            print(variables.RESET + time_thread.currentTimeStamp + " [Error]    " + variables.RED + "Cannot login to Telegram. Please restart bot and try again.")
            quit.quitSniper(True)

        print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Listening for token signals on Telegram channels...")

        if variables.sellTokens:
            monitorSellThread = threading.Thread(target=approve_and_sell.monitorAndSell, )
            monitorSellThread.start()

        client.run_until_disconnected()
    except:
        debug.handleError(traceback.format_exc(), "startTGListenerMain")
    
    


