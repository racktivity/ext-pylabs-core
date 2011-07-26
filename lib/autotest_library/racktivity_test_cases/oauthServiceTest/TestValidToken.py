from nose.tools import *
from . import DistibutedLoginClient
import oauth2 as oauth
import time
import json

CONSUMER_KEY = 'admin'

def setup():
    pass

def teardown():
    pass

def testListCloudusers_5():
    client = DistibutedLoginClient()
    access_token = client.getToken()
    headers = {'oauth_token':"token_%s"%access_token['oauth_token'], 'oauth_token_secret':access_token['oauth_token_secret'], 
               'oauth_consumer_key':CONSUMER_KEY, 'oauth_nonce':oauth.generate_nonce(), 'oauth_verifier':'', 'oauth_timestamp': str(time.time())}
    response = client.send_request(headers)
    response = json.loads(response)
    assert_true(len(response) > 0, 'the cloud api call is successful')
