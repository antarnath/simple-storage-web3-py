from solcx import compile_standard
import json
from web3 import Web3
from decouple import config

with open('./SimpleStorage.sol', 'r') as file:
  simple_storage_file = file.read()
  
  # print(simple_storage_file)

compiled_sol = compile_standard(
  {
    "language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
    "settings": {
      "outputSelection": {
        "*": {
          "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
        }
      }
    },
  },
  solc_version="0.6.0",
)

with open('compliled_code.json', 'w') as file:
  file.write(json.dumps(compiled_sol))

# print(compiled_sol)

bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# print(abi)

# for connecting to ganache 
w3 = Web3(Web3.HTTPProvider('http://0.0.0.0:7545'))
chain_id = 1337
my_address = '0xD7336A8ef0e8662bd9f13FBf45FA44948Eb742b5'
private_key = config('PRIVATE_KEY')

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)

# 1. Build a transaction 
# 2. Sign a transaction 
# 3. Send a transaction

transaction = SimpleStorage.constructor().build_transaction({
  'chainId': chain_id, 
  'from': my_address, 
  'nonce': nonce
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
print('Deploying Contract...')
# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Deployed!')

# Working with Contract, you need:
# Contract ABI
# Contract Address

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change


# Initial value of favorite number
print(simple_storage.functions.retrieve().call())

print('Updating Contract... set prifavoriteNumber to 999')
store_transaction = simple_storage.functions.store(999).build_transaction({
  'chainId': chain_id, 
  'from': my_address, 
  'nonce': nonce + 1
})

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print('Updated Contract!')
print(simple_storage.functions.retrieve().call())

print('Find FavoriteNumber for Antar: ',simple_storage.functions.nameToFavoriteNumber('Antar').call())

print('Updating Contract... add new person with Antar and 312')

addPerson_transaction = simple_storage.functions.addPerson('Antar', 312).build_transaction({
  'chainId': chain_id, 
  'from': my_address, 
  'nonce': nonce + 2
})

addPerson_txn = w3.eth.account.sign_transaction(addPerson_transaction, private_key)
addPerson_send_tx = w3.eth.send_raw_transaction(addPerson_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(addPerson_send_tx)

print('Updated Contract!')


# Get Person data

print('Find FavoriteNumber for Antar: ',simple_storage.functions.nameToFavoriteNumber('Antar').call())