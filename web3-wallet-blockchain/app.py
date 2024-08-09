import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from web3 import Web3
import json

# Connect to Sepolia testnet
infura_url = 'https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID'
web3 = Web3(Web3.HTTPProvider(infura_url))

# Define the smart contract ABI and address (replace with your own)
contract_address = 'YOUR_CONTRACT_ADDRESS'
contract_abi = json.loads('YOUR_CONTRACT_ABI')

# Initialize the smart contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("NFT Dashboard"),
    dbc.Row([
        dbc.Col([
            html.Label("MetaMask Wallet Address:"),
            dcc.Input(id='wallet-address', type='text', placeholder='Enter your wallet address'),
            html.Button('Check NFT Balance', id='check-balance-btn', n_clicks=0),
            html.Div(id='nft-balance')
        ]),
        dbc.Col([
            html.Label("Customize NFT:"),
            dcc.Input(id='nft-id', type='text', placeholder='Enter NFT ID'),
            dcc.Input(id='new-info', type='text', placeholder='Enter new info'),
            html.Button('Update NFT Info', id='update-nft-btn', n_clicks=0),
            html.Div(id='update-status')
        ])
    ])
])

@app.callback(
    Output('nft-balance', 'children'),
    Input('check-balance-btn', 'n_clicks'),
    State('wallet-address', 'value')
)
def check_nft_balance(n_clicks, wallet_address):
    if n_clicks > 0:
        # Replace with actual function to check balance
        balance = contract.functions.balanceOf(wallet_address).call()
        return f'NFT Balance: {balance}'
    return ''

@app.callback(
    Output('update-status', 'children'),
    Input('update-nft-btn', 'n_clicks'),
    State('wallet-address', 'value'),
    State('nft-id', 'value'),
    State('new-info', 'value')
)
def update_nft_info(n_clicks, wallet_address, nft_id, new_info):
    if n_clicks > 0:
        # Replace with actual function to update NFT
        try:
            tx_hash = contract.functions.updateNFTInfo(nft_id, new_info).transact({'from': wallet_address})
            return f'Success! Transaction Hash: {tx_hash.hex()}'
        except Exception as e:
            return f'Error: {str(e)}'
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from web3 import Web3
import json

# Connect to Sepolia testnet
infura_url = 'https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID'
web3 = Web3(Web3.HTTPProvider(infura_url))

# Define the smart contract ABI and address (replace with your own)
contract_address = 'YOUR_CONTRACT_ADDRESS'
contract_abi = json.loads('YOUR_CONTRACT_ABI')

# Initialize the smart contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Web3 wallet and Blockchain Testing APP"),
    dbc.Row([
        dbc.Col([
            html.Label("MetaMask Wallet Address:"),
            dcc.Input(id='wallet-address', type='text', placeholder='Enter your wallet address'),
            html.Button('Check NFT Balance', id='check-balance-btn', n_clicks=0),
            html.Div(id='nft-balance')
        ]),
        dbc.Col([
            html.Label("Customize NFT:"),
            dcc.Input(id='nft-id', type='text', placeholder='Enter NFT ID'),
            dcc.Input(id='new-info', type='text', placeholder='Enter new info'),
            html.Button('Update NFT Info', id='update-nft-btn', n_clicks=0),
            html.Div(id='update-status')
        ])
    ])
])

@app.callback(
    Output('nft-balance', 'children'),
    Input('check-balance-btn', 'n_clicks'),
    State('wallet-address', 'value')
)
def check_nft_balance(n_clicks, wallet_address):
    if n_clicks > 0:
        # Replace with actual function to check balance
        balance = contract.functions.balanceOf(wallet_address).call()
        return f'NFT Balance: {balance}'
    return ''

@app.callback(
    Output('update-status', 'children'),
    Input('update-nft-btn', 'n_clicks'),
    State('wallet-address', 'value'),
    State('nft-id', 'value'),
    State('new-info', 'value')
)
def update_nft_info(n_clicks, wallet_address, nft_id, new_info):
    if n_clicks > 0:
        # Replace with actual function to update NFT
        try:
            tx_hash = contract.functions.updateNFTInfo(nft_id, new_info).transact({'from': wallet_address})
            return f'Success! Transaction Hash: {tx_hash.hex()}'
        except Exception as e:
            return f'Error: {str(e)}'
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
