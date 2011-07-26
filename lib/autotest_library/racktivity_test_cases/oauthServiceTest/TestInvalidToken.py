from nose.tools import *
from . import DistibutedLoginClient
import oauth2 as oauth
import time
import arakoon

CONSUMER_KEY = 'admin'

def setup():
    pass

def teardown():
    pass

def testListCloudusers_2():
    client = DistibutedLoginClient()
    access_token = client.getToken()
    access_token = client.tamperData(access_token, 'INVALIDATE_KEY')
    headers = {'oauth_token':'token_$(%s)'%access_token['oauth_token'], 'oauth_token_secret':access_token['oauth_token_secret'], 
               'oauth_consumer_key':CONSUMER_KEY, 'oauth_nonce':oauth.generate_nonce(), 'oauth_verifier':'', 'oauth_timestamp': str(time.time())}
    
    response = client.send_request(headers)
    assert_true(str(response).index('ArakoonNotFound')>0, 'Invalid key found!')