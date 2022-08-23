import os
from . import variables

def setup_token_cache():
    current_directory = os.getcwd()
    temp_directory = os.path.join(current_directory, r'temp')
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

    tokenCacheFilePath = os.path.join('temp', (variables.chainName + 'TokenCache.csv'))

    try:
        fp = open(tokenCacheFilePath)
        fp.close()
    except IOError:
        # If not exists, create the file
        fp = open(tokenCacheFilePath, 'w+')
        fp.close()

    soldTokensFilePath = variables.chainName + 'SoldTokens.csv'
    try:
        fp = open(soldTokensFilePath)
        fp.close()
    except IOError:
        # If not exists, create the file
        fp = open(soldTokensFilePath, 'w+')
        fp.close()

    #load token addresses to memory

    with open(tokenCacheFilePath, "r") as tokenCache:
        tokenCacheLines = tokenCache.readlines()

        for line in tokenCacheLines:
            tokenAddress = line.split(",")[0]
            variables.currentTokenAddresses.append(tokenAddress)



