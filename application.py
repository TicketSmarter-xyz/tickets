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
import sys
from mnemonic import Mnemonic
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from eth_account.messages import encode_defunct
from web3.auto import w3
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from web3.auto import w3
from eth_account.messages import encode_defunct
from gql.transport.aiohttp import AIOHTTPTransport

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

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv("SUPABASE_KEY")

#Supabase object
supabase = create_client(url, key)
#Flask server
application = Flask(__name__)
# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api-mumbai.lens.dev/")
# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

@application.route("/")
def index(): #landing
    return render_template('index.html')

@application.route("/login", methods=["GET","POST"])
def login_page():
    return render_template('login.html')

@application.route("/dashboard")
def dashboard(user_address):
    advanced_used_inapp_balance = get_balance(address)
    return render_template('events.html')

@application.route("/event_<event_id>")
def event_page(event_id):
    site_name = "event_" + event_id + ".html"
    return render_template(site_name)

@application.route("/marketplace")
def marketplace():
    return render_template('marketplace.html')

# Advanced user in-app balance retriever
def get_user_balance(address):
    wei = w3.eth.getBalance(address, block_identifier = w3.eth.defaultBlock)
    eth = w3.fromWei(wei, 'ether')
    return eth

#Inserts a user info to the Supa Database
def insert_supa_user(tabla, words, privatekey, address, email, token_oath=None):
	data = supabase.table(tabla).insert({"phrase":words, "privatekey":privatekey, "address":address, "email":email, "token_oath":token_oath}).execute()
	assert len(data.data) > 0

#Inserts an event info to the Supa Database
def insert_supa_event(tabla, user, artist, veneu, date, price,total_tickets, mintdate, image):
	data = supabase.table(tabla).insert({"user":user, "name_event":name_event, "artist":artist, "price":price, "total_tickets":total_tickets, "mintdate":mintdate, "image":image}).execute()
	assert len(data.data) > 0

def create_wallet(email, token_oath = None):
	load_dotenv()
	url = os.getenv('SUPABASE_URL')
	key = os.getenv("SUPABASE_KEY")
	supabase = create_client(url, key)
	mnemo = Mnemonic("english")
	words = mnemo.generate(strength=128)
	seed = mnemo.to_seed(words, passphrase="test")
	#MAIN_NET_HTTP_ENDPOINT = "https://polygon-rpc.com/"
	MAIN_NET_HTTP_ENDPOINT = "https://rpc-mumbai.maticvigil.com/"
	w3 = Web3(Web3.HTTPProvider(MAIN_NET_HTTP_ENDPOINT))
	account = w3.eth.account.privateKeyToAccount(seed[:32])
	private_key = account.privateKey.hex()
	public_key = account.address
	insert_supa_user("users", words, private_key, public_key, email, token_oath)
	return True

#Create user profile
@application.route("/login_new", methods=["GET", "POST"])
def create_internal_profile():
    wallet_address = create_wallet(email, token_oath)
    #fondear la wallet
    lens_profile = create_lens_profile(seed)
    supabase_insert = insert_supa_user(tabla, words, privatekey, address, email, token_oath=None)
    x = request.form['nm']
    return True

#Orginizer / attendee
def create_lens_profile(wallet, handle):
    access_token = lens_auth()
    if access_token == None:
        return False
    #create profile
    query_profile = gql(
        """

        mutation CreateProfile($request: CreateProfileRequest!) {
    	 createProfile(request: $request){
    	   ...on RelayerResult {
    		txHash
    	   }
    	   ...on RelayError {
    		reason
    	   }
    	 }
        }
    """
    )
    params_profile = {
        "request": {
        "handle": handle,
        "profilePictureUri": "https://gateway.pinata.cloud/ipfs/bafkreiefgakk2cftozqhxafpla2fs75ux7iljt6mi6h25jyshrknvblkmm",
        "followModule": None,
        "followNFTURI": None
      }
    }

    headers_profile={
      "x-access-token":
    	"Bearer " + accesstoken
    }
    headers = { "x-access-token": "Bearer " + accesstoken }
    transport2 = AIOHTTPTransport(url="https://api-mumbai.lens.dev/", headers=headers )
    client2 = Client(transport=transport2)
    result = client2.execute(query_profile, params_profile)
    print (result)
    return True

def lens_auth(address="0x47f016C4B972C04bc2d7606Bde58E9C4Fce7683F", private_key = "04b33951cb7d3bd5205b3fe6121c08b94e557c7f234e88b2ad5b2f85b3460582"):
    # To get a JWT token, you must first request a challenge from the server, which will return you some text to sign with the wallet to prove ownership.
    # Provide a GraphQL query
    query = gql(
        """
        query($request: ChallengeRequest!) {
    	   challenge(request: $request) { text }
        }
    """
    )
    params = {
    	 "request": {
    	   "address": address
    	 }
        }
    result = client.execute(query, params)
    print(result)
    #firmar tx
    challenge_text = result['challenge']['text']
    message = encode_defunct(text=challenge_text)
    signed_message =  w3.eth.account.sign_message(message, private_key=private_key)
    mensajefirmado = signed_message.signature.hex()
    print('signed_message')
    print(signed_message)
    print('mensajefirmado')
    print(mensajefirmado)
    query =  " mutation Authenticate {" + "authenticate(request: { " + "address: \"" + address + "\", " + "signature: \"" + mensajefirmado + "\"}) {"+ "accessToken " + "refreshToken" + "}" + "}"
    queryAuth = gql( query )
    resultauth = client.execute(queryAuth)
    accesstoken = resultauth['authenticate']['accessToken']
    #Reference Module would ensure you can't share/participate in the event's group unless you have collect NFT but it is not ready yet, as per the Lens' team explanation
    return accesstoken

#Collect Module allows other users to mint NFTs that link to the publication's ContentURI.
def collect_NFT():

    return True

#Create event / Publication
def create_lens_post():
    #Staking a guarantee is a future option
    return True

#Signs a message using w3
def sign_message(message = None, private_key="04b33951cb7d3bd5205b3fe6121c08b94e557c7f234e88b2ad5b2f85b3460582"):
    if message == None:
        print("El mensaje está vacío")
        return False
    message = encode_defunct(text=msg)
    signed_message =  w3.eth.account.sign_message(message, private_key)
    print(signed_message)
    return signed_message

# def create_event(user, name_event, artist, veneu, date, price,total_tickets, mintdate, image ):
# 	insert_supa_event("events",user, name_event, artist, veneu, date, price,total_tickets, mintdate, image )



if __name__ == '__main__':
    print("application.py is RUNNING")
    # import pdb; pdb.set_trace()
    application.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True)
    # create_wallet("erik@mail.com", token_oath)
