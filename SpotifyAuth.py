"""

"""
# imports
import requests as requests
from os import environ
from base64 import b64encode
from json import loads





def bearAuthHeader():
    return authHeader(getBearerToken())

def authHeader(bearer):
    return {"Authorization":bearer}

def getBearerToken():
    params = {
        'Content-Type':"application/x-www-form-urlencoded;charset=UTF-8",
        'Authorization':"",
    }
    body = {
        'grant_type':'client_credentials',
    }
    client_key, client_secret = "SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"
    client_key, client_secret = environ[client_key], environ[client_secret]
    bearer_token_cred = client_key+":"+client_secret
    bearer_token_cred_bytes = bearer_token_cred.encode(encoding='utf-8')
    base64_encoded_bearer_cred = b64encode(bearer_token_cred_bytes)

    params['Authorization'] = 'Basic ' + base64_encoded_bearer_cred.decode(encoding='utf-8')
    req = requests.post('https://accounts.spotify.com/api/token', data=body, headers=params)
    return "Bearer "+ loads(req.text)['access_token']



if __name__ == "__main__":
    getBearerToken()
