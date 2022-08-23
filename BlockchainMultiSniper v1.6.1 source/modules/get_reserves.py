from . import variables


def getReserves(pairAddressforReserves): #fundamental code for liquidity detection
    pairReserves = None
    while pairReserves == None:
        try:
            router = variables.web3.eth.contract(address=pairAddressforReserves, abi=variables.pairABI)
            pairReserves = router.functions.getReserves().call()
            return pairReserves
        except:
            print(variables.RED + "[ERROR] Error with getting reserves, retrying...")
