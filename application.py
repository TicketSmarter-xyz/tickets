import json
import time
import datetime
import os
from random import random
from time import sleep
import pdb
import flask
from flask import Flask, render_template, url_for, copy_current_request_context, request, redirect
from web3 import Web3, HTTPProvider, exceptions, _utils
from web3.contract import ConciseContract
import regex as re
import comun
import sys

Matic_Mainnet = {
'name': "Matic_Mainnet",
'chain_id': 137,
'chain_id_hex': "0x89",
'infura_key': "",
'endpoint': "",
'token': "MATIC",
"test_network": False,
'block_explorer': "https://polygonscan.com/address/",
}

Matic_Mumbai_Testnet = {
'name': "Matic_Mumbai_Testnet",
'chain_id': 80001,
'chain_id_hex': "0x13881",
'infura_key': "", # Sign up for a free dedicated RPC URL at https://rpc.maticvigil.com/ or other hosted node providers.
# 'endpoint': 'https://rpc-mumbai.matic.today',
'endpoint': 'https://matic-mumbai.chainstacklabs.com',
'token': "MATIC",
"test_network": True,
'block_explorer': "https://mumbai.polygonscan.com/address/",
}

application = Flask(__name__)

@application.route("/")
def index(): #landing
    return "Welcome"

@application.route("/login", methods=["GET","POST"])
def login():
    print(request.args.get("test"))
    return "please login"

@application.route("/dashboard")
def dashboard(user_address):
    advanced_used_inapp_balance = get_balance(address)
    return "dashboard"

@application.route("/event_<event_id>")
def event_page(event_id):
    return "Welcome to event " + event_id

@application.route("/marketplace")
def marketplace():
    return "marketplace"

def create_profile():
    # recibe body con la data del formulario
    # la manda al contrato para crear el nft
    return True

def create_wallet(random_seed = 'xyz' + str(random_seed)):
    acct = w3.eth.account.create(random_seed)
    return acct.address, acct.privateKey.hex()

def get_balance(address):
    wei = w3.eth.getBalance(address, block_identifier = w3.eth.defaultBlock)
    eth = w3.fromWei(wei, 'ether')
    return eth

def deploy_contract(deploy_key, param1, param2):
    print("W3 connection status:")
    connection = w3.isConnected()
    print(connection)
    if connection == False:
        return False
    ### make sure to encrypt later ###
    acct = w3.eth.account.privateKeyToAccount(deploy_key)
    contract= w3.eth.contract(bytecode=bytecode, abi=abi)
    gasprice = w3.eth.gasPrice
    # building and signing transaction
    transaction = {'from': acct.address, 'nonce': w3.eth.getTransactionCount(acct.address), 'gas': 350000, 'gasPrice': gasprice, 'value': w3.toWei(param2,'ether')}
    construct_txn = contract.constructor(acct.address, param1).buildTransaction(transaction)
    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    print("Tx hash: ", tx_hash.hex())
    print("Waiting for deployment...")
    time.sleep(20) #hardcode
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Contract deployed at: ", tx_receipt['contractAddress'])
    return True

#Create user profile
def create_internal_profile():
    return user_info_json

#Orginizer / attendee
def create_lens_profile():
    return

#Create event
def create_lens_post():
    #Staking a guarantee is a future option
    
    return

def collect_NFT():

    #Reference Module would ensure you can't participate in the community unless you have collect NFT
    return





if __name__ == '__main__':
    print("application.py is RUNNING")
    application.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True)
