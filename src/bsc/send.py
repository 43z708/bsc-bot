from web3 import Web3

bsc_rpc = "https://bsc-dataseed.binance.org/"

my_wallet_address = '*** 自分のウォレットのアドレス ***' # 自分のウォレットのアドレス
my_secret_key = '*** 自分のウォレットの秘密鍵 ***' # 自分のウォレットの秘密鍵
to_wallet = '*** 送り先のアドレス ***' # 送り先のアドレス
amount = 0.01 # 送金料

web3 = Web3(Web3.HTTPProvider(bsc_rpc))

nonce = web3.eth.getTransactionCount(my_wallet_address)

tx = {
        'nonce': nonce,
        'to': to_wallet,
        'value': web3.toWei(amount, 'ether'),
        'gas': 25000,
        'gasPrice': web3.toWei('5', 'gwei')
    }

signed_tx = web3.eth.account.sign_transaction(tx, key_A)

tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(web3.toHex(tx_hash))
