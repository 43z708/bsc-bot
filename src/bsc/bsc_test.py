from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
isConnected = web3.isConnected()

if isConnected:
    print('Connected to BSC')