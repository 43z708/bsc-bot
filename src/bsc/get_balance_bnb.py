from web3 import Web3

bsc_rpc = "https://bsc-dataseed.binance.org/"

web3 = Web3(Web3.HTTPProvider(bsc_rpc))

my_wallet_address = ''

balance = web3.eth.getBalance(my_wallet_address)

print('Wallet A BNB Balance: ', (web3.fromWei(balance, 'Ether')))
