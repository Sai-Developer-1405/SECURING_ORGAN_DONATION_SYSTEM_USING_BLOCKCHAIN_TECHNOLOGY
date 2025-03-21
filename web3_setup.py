from web3 import Web3

# Initialize a web3 instance connected to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Paste the contract address you copied from the Truffle output
contract_address = '0xd8ad04f4f44c331fecf4669a0e9554980823cab3'

# Define your contract's ABI
contract_abi = [
    {
        "constant": false,
        "inputs": [],
        "name": "yourFunctionName",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    }
    # Add more functions from your contract's ABI as needed
]

# Instantiate your contract object
contract = w3.eth.contract(address=contract_address, abi=contract_abi)