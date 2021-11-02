* BSCTokenSniper v1.4 Beta is available for testing which is far better than the above versions, please check the telegram link for a link to the testing group where you can find the zip file.

* v1.3 and earlier versions are now abandoned in favour of v1.4. The code isn't available on github yet and more testing still needs to be done but it is mostly reliable.

* This description is still a bit of a mess as new features are still being added and tested constantly to v1.4. Some parts of the description are irrelevant or outdated.


<!--[![Contributors][contributors-shield][contributors-url] -->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<!--[![LinkedIn][linkedin-shield]
[linkedin-url]-->

## Environment 
<p align='left'>
  <img src='https://img.shields.io/badge/OS-Windows10-007ef9?style=for-the-badge&logo=microsoft' alt='Windows11'>
  <img src='https://img.shields.io/badge/OS-Linux-blue?style=for-the-badge&logo=linux' alt='Linux'>
  <img src='https://img.shields.io/badge/OS-Android12-green?style=for-the-badge&logo=android' alt='Android'>
  <img src='https://img.shields.io/badge/IDE-VSCode%20-44b26f?style=for-the-badge&logo=visualstudiocode&logoColor=44b26f' alt='VSCode'>



<!-- PROJECT LOGO -->
<!--
 <br />
 <p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">BSCTokenSniper</h3>

  <p align="center">
    A sniper bot written in Python to buy tokens as soon as liquidity is added and sell on later when the price increases.
    <br />
    <a href="https://github.com/BytePhoenixData/BSCTokenSniper/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/BytePhoenixData/BSCTokenSniper/issues">Report Bugs</a>
    ·
    <a href="https://github.com/BytePhoenixData/BSCTokenSniper/issues">Request Feature</a>
    ·
    <a href="https://t.me/joinchat/7TtO_mvE90UzYmM0">Telegram Group</a>
  </p>
</p>



<!-- Snipe the shit -->
<details open="open">
  <summary>Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#operating-system">Operating System</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
<!--    <li><a href="#usage">Usage</a></li> -->

<li><a href="#configuration-file">Configuration File</a></li>
    <li><a href="#mini-audit">Mini audit</a></li>
    <li><a href="#things-to-note">Things to note</a></li>
    <li><a href="#common-errors-and-how-to-fix-them">Common errors and how to fix them</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li>
        <a href="#contributing">Contributing</a>
    </li>
    <li>
      <a href="#version">Versions</a>
      <ul>
        <li><a href="#v14">v1.4 Beta</a></li>
        <li><a href="#v13">v1.3</a></li>
        <li><a href="#v12">v1.2</a></li>
        <li><a href="#v11">v1.1</a></li>
      </ul>
    </li>    
    <li><a href="#risks">Risks</a></li>
    <li><a href="#faqs">FAQs</a></li>
    <li><a href="#donations">Donations</a></li>
    <li><a href="#things-to-do--improve--fix">Things to do / improve / fix</a></li>
    <li><a href="#how-to-pre-audit-tokens-for-launch-sniping">How to pre-audit tokens for launch sniping</a></li>
  
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

<!--[![Product Name Screen Shot][product-screenshot]](https://example.com)-->

BSCTokenSniper is a completely free collection of 2 tools (BSCMultiSniper and BSCLaunchSniper) programmed in Python and Web3 which aim to automatically buy newly listed tokens and auto sell tokens when profitable.

BSCMultiSniper detects new tokens as soon as liquidity is added. It will check if it is not a scam and if not will buy it. It will then monitor the price of the token and auto sell at the specified profit margin (eg. 1.5x, 2x, 10x etc).

BSCLaunchSniper allows you to snipe new token launches paired with any token (eg. BNB, BUSD). It has the ability to mempool snipe and will instantly buy when liquidity is added. It constantly updates the price and shows you the profit you've made, has the ability to autosell at a specified profit margin (eg, 2x, 10x etc) and also allows you to sell manually with your keyboard. You can use the spacebar to sell 100% of your tokens or use keys 1-9 to sell 10-90% of your tokens.

 The multisniper is able to check if:
 - Token is a honeypot
 - Token's buy/sell fees are too large
 - Token has any scams / exploits in code
 - Token's code is verified
 - Token's ownership is renounced
 - Token's liquidity is locked


The user can decide whether to enable the mini audit or turn it off (bear in mind you will likely be investing in a lot of scams / rugpulls / honeypots if you don’t).
Once the token has/hasn't been through a mini audit the bot will then attempt to buy X amount of tokens with the specified amount of BNB.
The bot will buy the tokens directly through the Binance Smart Chain using the PancakeSwap v2 router and factory address, so it is much quicker than the PancakeSwap web interface.

By avoiding web interfaces & Metamask and directly with nodes you can snipe tokens faster than any of the web-based platforms. This allows tokens to be sniped almost instantly. During our testing we found the bot would typically be within the first 3 buy transactions of all tokens it finds.
The bot buys the tokens using the user's wallet address and private key. This information is kept secure, is only stored locally on your computer, and is only ever used to buy tokens.

The bot does not incur any additional fees except from the dev fees on profit made, only fees are BSC / PancakeSwap gas fees.

The bot's source code is heavily obfuscated and compiled to prevent people stealing code and scammers trying to bypass this system as this has happened before. If you have concerns about the security of this bot then you should create a new wallet with a small amount of BNB and use that wallet's details in the config file. If you make a profit then that can be transferred to your main wallet. You can also use a virtual machine if you like.

How do the developers make money? What are the fees?

From v1.4 onwards the bot will have a fee on profit made: both bots will have a sell fee of 10% of profits made. The fee is only sent when profit is made and there is no dev fees if you break even or lose money. This allows us to offer everyone the bot free of charge, as most people do not want to pay hundreds or thousands of dollars for sniper bots that they can't even trial first. The fees made massively support the project and allow us to test out new features.

 We would also like to give a massive thanks to the devs at StaySAFU scanner for allowing us to use their token scanner API.
 
© Copyright 2021 - any attempt to sell, modify, decompile, copy or replicate this code is strictly forbidden and may result in legal action.

### Built With

This project is built with:

* [Python3.9](https://www.python.org/downloads/)
* [Web3](https://web3py.readthedocs.io/en/stable/)
* [Keyboard Module](https://pypi.org/project/keyboard/) (for launch sniper)


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple steps.

### Prerequisites

BSCTokenSniper is completely free to use and there are no setup costs.

- Windows, Mac, Linux or Android OS (windows preferred)
- A reasonably fast internet connection
- Python 3 or later installed (ideally 3.9.7 or later)
- BSC wallet address and private key (not seed phrase)
- A BSC node (generate one free of charge from moralis.io - steps are available further below)
- Enough BNB in your wallet to snipe tokens (and other paired tokens if you choose a different liquidity pair address eg. BUSD)

### Operating System

The bot can be run on the following OS's:
  1.  Windows
  2.  Linux 
  3.  Mac 
  4.  Android (more advanced) 

## Installation

### Windows

1. Download git [Git](https://git-scm.com/)
2. Download python [Python3.9](https://www.python.org/)
3. Clone the repo: 

      ```sh
      git clone https://github.com/BytePhoenixData/BSCTokenSniper.git 
      ```

4. Go to repo directory

5. and run : 
      ```sh
      cd BSCTokenSniper
      ```
6. Install Web3:

      ```sh
      pip install web3
      ```

   If you facing an error during the web3 installation, you may need the following microsoft visual studio build tool.
   use this [link](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019).
   
## Linux User
   
  Install the package With 

  ```sh 
  sudo
  ```
Debian / Ubuntu: 
1. install all dependencies using command below.

```sh
apt install git && apt install python3-pip && pip install web3
```

2. Clone repository and install web3

```sh
git clone https://github.com/BytePhoenixData/BSCTokenSniper.git && cd BSCTokenSniper && pip install web3
```

Fedora Linux / Centos
 1. install all dependency using command below.

```sh
dnf install git && dnf install python3-pip && pip install web3 
``` 

2. Clone repository and install web3

```sh
git clone https://github.com/BytePhoenixData/BSCTokenSniper.git && cd BSCTokenSniper && pip install web3
```

Arch Linux
 1. install all dependency using command below.

 ```sh
 pacman -S git && pacman -S install python3-pip && pip install web3 
 ``` 

2. Clone repository and install web3

```sh
git clone https://github.com/BytePhoenixData/BSCTokenSniper.git && cd BSCTokenSniper && pip install web3
```

- If you all find the error try this bellow command and may fix your problem.

```
pip uninstall web3 && pip install web3
```

or

```sh
pip install -U web3
```

## Mac (Intel / Universal)

NOTE: BSCLaunchSniper is currently not working for M1 Macs (Apple silicon chips) due to the keyboard module being incompatible.

1) Make sure python 3 is installed

- open terminal window
- type : python3 --version
- if you get an error message and python3 isn't installed, you need to add it.

- go to https://www.python.org/ and install latest version of python for mac

- in terminal window one last check to see you have Python 3 installed
- type : python3 --version
- should see Python 3.9.7 or later showing

2) Install web3

- open terminal window
- type : pip3 install web3
- wait while web3 installs
- NOTE : part way through the install you may be prompted to install xcode
- if this happens carry on and install xcode
- some errors may be now showing in terminal window
- go back to terminal and type : pip3 install web3
- after this (xcode installation) web3 should be good to go

3) Edit config.json

- recommended opening a fresh metamask wallet for sniper testing
- Edit lines 2+3 of config.json with your wallet address + private key
   "walletAddress": "put_your_wallet_address_here",
   "walletPrivateKey": "put_your_private_key_here",
- To get private key from metamask click the 3 dots just under the favicon
- Select 'Account Details'
- Select 'Export Private Key'

- Add Speedy Node to line 13
   "bscNode": "Enter node URL here",
- https://admin.moralis.io/register to get your free speedy node
- Go to 'Speedy Nodes' on the left
- Choose yellow BSC Network icon on right
- Click Endpoints
- Take key from top line and paste in (address must start with wss://)

- Add your BscScan private API key to line 14
   "bscScanAPIKey": "put_BSC_API_key_here",
- To get a free API key just register at https://bscscan.com/
- Go to API-KEYs menu option on left
- Click blue '+Add' button next to text 'My API Keys'
- Choose name for API key (can be anything)
- Copy key value from 'API-Key token' column


4) Run script 

- Get in terminal window
- Make sure you are in the directory of the script before you run it.
- type : python3 BSCTokenSniper.pyc

5) Open finder, then click Applications —> Python 3.7 folder to expand it. 
There should be a file called 'Install Certificated.command', double click the file to run it. 
It will open another popup terminal window and show below command execution output text. 
Once it is complete close it and run the bot.

## Android
1. Install Termux [Link](https://play.google.com/store/apps/details?id=com.termux&hl=en&gl=US)
2. Update

  ```sh
  pkg update && pkg upgrade
  ```

   3. Install dependency

```sh 
pkg install git python3 python3-pip
```

   4. Install web3 

```sh
pip install web3
```

```sh
pip install -U web3
```

   5. Clone the repo using git

```sh
git clone https://github.com/BytePhoenixData/BSCTokenSniper.git && cd BSCTokenSniper
```

Note:
You may encounter an error when installing web3 in android. You should install the dependency needed by web3 manually using pip.
The web3 version that work for this bot is web3 5.x.x, if your web3 is 3.x.x or lower then the bot will not work.
 
## Run python script

Assuming you are in BSCTokenSniper Directory:
run 

```sh
python3 BSCMultiSniper.pyc (or BSCLaunchSniper.pyc)
```

for V1.3 or latest, you should install Python 3.9 or later

# Configuration File

When you download the bot, you will find a config.json file. This is where you need to add the following data.

For BSCMultiSniper:

* walletAddress (string): your BSC wallet address (e.g., Metamask) 
* walletPrivateKey (string): your private key of your wallet address (your private key is kept safe and not shared in any other place: DO NOT share with anyone else)

* totalAllowedSnipes (integer): total amount of new tokens you would like to snipe until program will stop buying. Leave at -1 to disable (to buy new tokens indefinitely).
* amountToSpendPerSnipe (float): The amount in BNB you want your wallet to spend on every new token. (e.g, 0.00025 means a new snipe will spend 0.00025 BNB on the new token)

* transactionRevertTimeSeconds (integer): Time to spend in seconds before transaction reverts. Recommended to leave at default.

* gasAmount (integer): amount of max gas to use per transaction. Recommended to leave at default.

* gasPrice (integer):  max price of gas to use per transaction. Recommended to leave at default.

* bscNode (string): Address for custom BSC node. Make sure it starts with (wss://). Recommended to leave at default.

* liquidityPairAddress (string): Address for liquidity pairs. Recommended to leave at default.

* minLiquidityAmount (float): The minimum amount of liquidity in BNB in a token that the bot will purchase. The bot detects the amount of BNB in a newly detected token, and only buys tokens that have liquidity higher than the amount specified in the config file. Set to -1 to disable.

* autoSellTakeProfitMultiplier (float): Profit multiplier to auto-sell at, eg. set to 2 to sell at 2x original purchase value, 10 for 10x etc.

* approveSellTimeDelay (integer): Time in seconds to wait until bot will try to attempt approve transaction for selling. Recommended to leave at default.

* observeOnly (True/False): Allows you to see how the bot detects new token. Recommended to leave at default.

* enableMiniAudit (True/False): Allows you to enable/disable mini audit. Highly recommended to enable or you will most likely be buying scam tokens.

- The following options are related to the mini audit feature:

* checkHoneypot (True/False): Check if token is a honeypot. Highly recommended to enable.

* maxBuyFee (integer): Max buy fee allowed for sniping in percentage eg. set to 20 to avoid buying tokens with over 20% buy fee. Recommended to leave at 20 or lower.
 
* maxSellFee (integer): Max sell fee allowed for sniping in percentage eg. set to 20 to avoid buying tokens with over 20% buy fee. Recommended to leave at 20 or lower.
 
* maxLiquidityRisk (integer): Max liquidity risk (0-100) allowed. 0 is safest, 100 is least safest. Recommended to leave at 0. 
 
* checkCodeVerified (True/False): Check if code is verified eg. set to true to avoid tokens that haven't verified code. Recommended to leave at True.
 
* allowOwnerAccess (True/False): Check if contract owner has access to token eg. set to False to disable tokens that haven't renounced ownership. Recommended to leave at False.




For BSCLaunchSniper:

* walletAddress: wallet address to use for sniping.

* walletPrivateKey: wallet private key (must be a private key, NOT seed phrase)

* pancakeSwapRouterAddress: chosen router address, recommended to leave at default

* liquidityPairAddress: chosen liquidity pair address - is WBNB by default, but you can set to BUSD, USDC, USDT etc to snipe BUSD etc paired tokens

* nonBNBPairAddress: (True/False) if the liquidity pair address is not BNB, eg. if you use BUSD then set to False, if using BNB then set to True

* bscNode: your BSD node URL (must start with wss://), recommended to use speedynode but you can use a private node if you wish

* transactionRevertTimeSeconds: TX revert time in seconds, recommended to leave at default

* gasAmount: amount of gas for bot to use in TX's, recommended to leave at 3 mil

* gasPrice: price of gas for but to use in TX's, recommended to leave at 5, you can increase for faster snipes eg. 6, 7 (you may have to increase gas amount though)

* approveSellTimeDelay: time to delay for getting receipt of approve TX's, recommended to leave at default

* stopLossMultiplier: the bot will sell when value of tokens is below the threshold eg. 0.5 means bot will sell when less than 1/2 of its original value.

* sellTokens: (True/False) Do you want to sell tokens through the bot. Recommended to leave at True as selling will be alot faster and easier.

* showPoocoinPage: (True/False) Do you want to display poocoin page in your web browser when tokens are bought.


# Mini audit

The bot has an optional mini audit feature which aims to filter some of the scam coins (eg. wrongly configured, honeypots). Obviously, this is not going to be as good as a proper audit (eg. CertiK) but at least the coins the bot will buy will be higher quality and if you enable the options, you should be able to sell the tokens later on (provided it hasn’t been rugged).

The bot uses RugDoc API to check for honeypots although we may use a different API in the future.

Note: be very careful when editing config.json and make sure to not alter the syntax. For mini audit options, either use “True” or “False” making sure to capitalise the 1st letter. Any other spelling will not work.

# Things to note

-	Do not worry if you are not seeing any new tokens being detected. There are often around 10-20 new tokens being created per minute but that can vary quite a lot. Sometimes no new tokens may be detected for a few minutes.

- make sure your input a private key (eg. 7d655977921bf21e25d29075712ee7aFce28b8d71aa4c7d8d5d403e28efeb879) into the program and not a seed phrase.

-	Please check that you have enough BNB in your wallet to afford sniping new tokens. If you don’t the bot will not work. If using a different liquidity pair address make sure theres enough of that token to use for sniping as well.

-	Please be careful when editing the config.json file. If you delete a comma or quotation mark etc. the bot will not work and throw an error.

-	To launch the bot, run the ‘launch.bat’. The bot should then open in a cmd window and load.

-	Don’t left click in the cmd window as it will enable select mode and stop the output (you will see ‘Select’ in the title). If this happens right click your mouse to deselect it. 

To use other version you need to go to the directory needed and run the python script.


# Common errors and how to fix them

```Incorrectly configured config.json file```
This means the bot cannot read your config.json file. Check that it is syntactically correct with no missing symbols, all fields are 
filled out correctly and restart the program.

```Cannot connect to BSC node```
The bot cannot connect to the BSC node. Make sure that you are using a valid BSC websocket node (starting with wss://) and restart.

```ValueError: {'code': -32000, 'message': '(replacement) transaction underpriced'}```
You are using too low gas. Increase gas price / limit and restart.

```websockets.exceptions.ConnectionClosedError: code = 4040 (private use), reason = Draining connection```
The bot cannot connect properly to the node. Make sure the node not overloaded / your internet connection is good enough / you dont have firewall software interfering with the bot / try a different node and try again.

```RuntimeError: Bad magic error in .pyc file```
Your python version is too low. Use the latest version of python (3.9.7 has been tested and works well) and uninstall older versions of python.

```ValueError: {'code': -32000, 'message': 'insufficient funds for gas * price + value'}```
You do not have enough BNB in your wallet to snipe with, or you dont have enough of the liquidity paired token specified (eg. BUSD). Make sure your wallet has enough BNB / specified pair token and try again.

```ModuleNotFoundError: No module named 'web3'```
You do not have web3 installed or python does not recognise it. Install it with ```pip install web3``` in cmd line or reinstall if faulty.

```ModuleNotFoundError: No module named 'keyboard'```
You do not have keyboard module installed or python doesn't recognise it. Install it with ```pip install keyboard``` in cmd line or reinstall if faulty.

```PancakeLibrary: INSUFFICIENT_INPUT_AMOUNT```
Bug with program, should be fixed later on.

```[Warning] Could not initialise filter or connect to node, trying again...```
This warning shows when the node deletes the filter or somehow stops the connection with the bot. The bot will auto-attempt to reconnect and if you only see this error once or twice then there is nothing to worry about. If it repeatedly shows then please let the developers know.



<!-- USAGE EXAMPLES -->
<!--
## Usage

Nothing interesting here.
-->


## Versions
v1.4 is being worked on and will be released on github shortly. It is available in the telegram testing group

# FAQs

I've sniped loads of coins - but how can I check which ones have made a profit?
-	For this go to poocoin.app, click 'Wallet' and connect your Web3 wallet that you are using for your bot (eg. Metamask).
-	It will then give you the list of tokens in your wallet and show you which ones have made the highest profit.
-	Click the descending arrow next to the balance tab to show highest to lowest tokens value.

I keep getting ‘Transaction failed’ – what’s going on?
Either:
-	Gas amount / price too low
-	Wallet address / private key incorrect
-	Not enough BNB to pay for the token and TX fees

The bot isn’t sniping that fast (eg. couple seconds between detection and buying)
- This is mainly due to your internet speed, the node you are using and your computer processing power. 

# Risks

Investing in BSC tokens / shitcoins is risky and you should be aware you could lose all your money. For this reason, NEVER invest more money than you can afford to lose. 

When using the launch sniper, DYOR. Look at the TG group, the contract's code and scanning tools.

The mini audit feature does not guarantee that the token is 100% safe but the chances of it being a scam are very small.
If a programmer creates token code in a unique way, they may be able to bypass detection although this is generally quite rare, as the majority of tokens are forks of big projects with very little of the code having been changed e.g, Safemoon.

Some good tools to use for detecting scams:

rugpulldetector.com
bscheck.eu
moonarch.app/token
honeypot.is
rugdoc.io/honeypot
rugscan.finance
tokensniffer.com
app.staysafu.org/scanner

# Things to do / improve / fix

 - Look into rugpull detection - we have got a license from StaySAFU to use their API, this will be integrated into the bot in the future.
 
- Modify bot to work on different blockchains eg. Ethereum, Polygon

- Improve reliability: the program can sometimes unexpectedly freeze / quit. This is being investigated.

- Allow user to set slippage percentage - currently bot just selects the best slippage automatically.

## Donations

We greatly welcome any donation of any token, it is massively appreciated and helps alot with the development of the project.

| Dev | BSC Address |
|:---:|:---:|
| BytePhoenix (founder) | 0x17fC36Fd733D2b2762c020e34E45b5C95723c9b3 |
| CVA_CryptoPlayground | 0x3a5A12dfffD327AFdaC7BEA60ECF7A48410E873a |


# How to pre audit tokens for launch sniping

There are a few tokens you can use to audit tokens.

Before a token is ready to launch, I would recommend the following steps:

1) Try and find the contract address before launch. If it hasn't been posted, search BSCscan for recently 
created contracts and it may appear. Make sure it is created recently.
3) Check if the source code is verified. If it isn't, stay away as its probably a scam. Legit developers have nothing to hide.
4) Check the source code for any suspicious functions by going to rugpulldetector.com and inputting the contract code. If there's any red
warnings then do not snipe it.
5) Check the TG group. Most of the time, the groups that have mute messaging most / all the time are scams. If theres more muted time than unmuted time
then its likely to be a scam.
6) If you can message in the group, post a message like "Everyone, please make sure to check the token is not a scam on honeypot.is / bscheck.eu / rugpulldetector.com". Do not directly say that it is a scam, legit admins should not have a problem with a message like this, scam admins will most likely block you / delete the message.
7) Use option 2 of the sniper a few mins before launch (5-10 mins) and it is recommended to sell early (first 5 mins).

# Future plans

- Convert launch sniper and multi sniper to work on ethereum and polygon blockchain.
- Develop website (domain blockchaintokensniper.com has been registered)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!--[contributors-shield]: https://img.shields.io/github/BytePhoenixData/BSCTokenSniper.svg?style=for-the-badge
[contributors-url]: https://github.com/BytePhoenixData/BSCTokenSniper/graphs/contributors -->
[forks-shield]: https://img.shields.io/github/forks/BytePhoenixData/BSCTokenSniper.svg?style=for-the-badge
[forks-url]: https://github.com/BytePhoenixData/BSCTokenSniper/network/members
[stars-shield]: https://img.shields.io/github/stars/BytePhoenixData/BSCTokenSniper.svg?style=for-the-badge
[stars-url]: https://github.com/BytePhoenixData/BSCTokenSniper/stargazers
[issues-shield]: https://img.shields.io/github/issues/BytePhoenixData/BSCTokenSniper.svg?style=for-the-badge
[issues-url]: https://github.com/BytePhoenixData/BSCTokenSniper/issues
[license-shield]: https://img.shields.io/github/license/BytePhoenixData/BSCTokenSniper.svg?style=for-the-badge
[license-url]: https://github.com/BytePhoenixData/BSCTokenSniper/blob/master/LICENSE.txt
<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555 -->
<!--[linkedin-url]: https://linkedin.com/in/othneildrew -->
[product-screenshot]: images/screenshot.png
