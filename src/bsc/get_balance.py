import json
from web3 import Web3

bsc_rpc = "https://bsc-dataseed.binance.org/"
my_wallet_address = ''

# トークンアドレスとトークン名、abiディレクトリのファイル名をトークン名と揃えること
contract_address = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'
token_name = 'CAKE'



web3 = Web3(Web3.HTTPProvider(bsc_rpc))

with open(f'bsc/abi/{token_name}.json') as f:
   abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi)

balance = contract.functions.balanceOf(my_wallet_address).call()

print(token_name + ' Balance: {}'.format(web3.fromWei(balance,'ether')))
