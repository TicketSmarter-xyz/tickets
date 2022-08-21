
#Usuario Organizador

private_key = "04b33951cb7d3bd5205b3fe6121c08b94e557c7f234e88b2ad5b2f85b3460582"
address="0x47f016C4B972C04bc2d7606Bde58E9C4Fce7683F"




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
