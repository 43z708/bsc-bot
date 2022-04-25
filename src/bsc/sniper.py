# import the following dependencies
import json
from web3 import Web3
import asyncio
import time

# add your blockchain connection information
bsc = 'https://bsc-dataseed.binance.org/'    
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())



my_wallet_address = ''
my_secret_key = '*** 自分のウォレットの秘密鍵 ***'
spend_token_address = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c' # WBNB
token_adress_to_buy = '0x899559c7151ddc01Fc084341B36101EAC1B6C01B'
bnb_amount = 0.01

# uniswap factory address and abi = pancakeswap factory
uniswap_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'  #Testnet  #0x6725F303b657a9451d8BA641348b6761A6CC7a17
with open(f'bsc/abi/uniswap.json') as f:
   uniswap_factory_abi = json.load(f)
contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)


#pancakeswap router abi 
panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'    #Testnet #0xD99D1c33F9fC3444f8101754aBC46c52416550D1
with open(f'bsc/abi/pancake.json') as f:
   pancake_abi = json.load(f)
contractbuy = web3.eth.contract(address=panRouterContractAddress, abi=pancake_abi)


wbnb = web3.toChecksumAddress(spend_token_address)   
sender_address = web3.toChecksumAddress(my_wallet_address) #the address which buys the token
tokenToBuy = web3.toChecksumAddress(token_adress_to_buy) # want to buy


#If conditions are met we buy the token
def buy():
    
    spend = web3.toChecksumAddress(spend_token_address)  #wbnb contract address

    nonce = web3.eth.get_transaction_count(sender_address)

    pancakeswap2_txn = contractbuy.functions.swapExactETHForTokens(
    0, # set to 0, or specify minimum amount of token you want to receive - consider decimals!!!
    [spend,tokenToBuy],
    sender_address,
    (int(time.time()) + 10000)
    ).buildTransaction({
    'from': sender_address,
    'value': web3.toWei(bnb_amount,'ether'),#This is the Token(BNB) amount you want to Swap from
    'gasPrice': web3.toWei('5','gwei'),
    'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=my_secret_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Snipe was succesfull, bought: " + web3.toHex(tx_token))



# define function to handle events and print to the console
def handle_event(event):
    #print(Web3.toJSON(event))
    # and whatever
    pair = Web3.toJSON(event)

    print(pair)
    
    token0 = str(Web3.toJSON(event['args']['token1']))
    token1 = str(Web3.toJSON(event['args']['token0']))
    #block =  Web3.toJSON(event['blockNumber'])
    #txhash = Web3.toJSON(event['transactionHash'])
   # print("Block: " + block)
    #print("Txhash: " + txhash)
    print("Token0: " + token0)
    print("Token1: " + token1)
    
    
    wbnb2 = wbnb.upper()
    
    tokenToBuy2 = tokenToBuy.upper()
    
    
    if(token0.upper().strip('"') == wbnb2 and token1.upper().strip('"') == tokenToBuy2):
        print("pair detected")
        buy()
    elif(token0.upper().strip('"') == tokenToBuy2 and token1.upper().strip('"') == wbnb2):
        print("pair detected")
        buy()
    else:
        print("next pair")


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.PairCreated.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter,2 )))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()



main()
