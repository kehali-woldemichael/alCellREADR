from __future__ import print_function
from base64 import b64encode
import json
from urllib import request, parse
import keyring
import requests 


def return_complexity_score(testSeq):
    """Returns complexity results for screening given sequence using screeningBlockSequences endpoint
    from IDTDNA 

    Args:
        testSeq (string): sequence to be tested in string form 

    Returns:
        json: json object containing different sequence properties (e.g. Score, ...) 
    """
    authorization_bearer = f"Bearer {get_access_token()}"
    url = "https://www.idtdna.com/api/complexities/screengBlockSequences"

    payload = json.dumps([
    {
        "Name": "My gBlock2",
        "Sequence": testSeq
    }
    ])
    headers = {
    'Content-Type': 'application/json',
    'Authorization': authorization_bearer,
    'Cookie': 'ARRWestffinity=500405b2a40425c0bc104c1e01d2b25a72c67638e8a81fc1390f090154ea7df7'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()[0][0]

def get_access_token():
    """
    Create the HTTP request, transmit it, and then parse the response for the 
    access token.
    
    The body_dict will also contain the fields "expires_in" that provides the 
    time window the token is valid for (in seconds) and "token_type".
    """

    # Get idtdna login details and api client keys from system keyring 
    idt_username = keyring.get_password("idtdna_username", "idt_user_name")
    idt_password = keyring.get_password("idtdna_password", idt_username)
    client_id = keyring.get_password("idtdna_client_id", "client_id")
    client_secret = keyring.get_password("idtdna_client_secret", client_id)

    # Construct the HTTP request
    authorization_string = b64encode(bytes(client_id + ":" + client_secret, "utf-8")).decode()
    request_headers = { "Content-Type" : "application/x-www-form-urlencoded",
                        "Authorization" : "Basic " + authorization_string }
                    
    data_dict = {   "grant_type" : "password",
                    "scope" : "test",
                    "username" : idt_username,
                    "password" : idt_password }
    request_data = parse.urlencode(data_dict).encode()

    post_request = request.Request("https://www.idtdna.com/Identityserver/connect/token", 
                                    data = request_data, 
                                    headers = request_headers,
                                    method = "POST")

    # Transmit the HTTP request and get HTTP response
    response = request.urlopen(post_request)

    # Process the HTTP response for the desired data
    body = response.read().decode()
    
    # Error and return the response from the endpoint if there was a problem
    if (response.status != 200):
        raise RuntimeError("Request failed with error code:" + response.status + "\nBody:\n" + body)
    
    # Return access token 
    return json.loads(body)['access_token']
