import httplib2
import json
import oauth2 as oauth
import urllib
from nose.tools import *
from pylabs import q, i
from . import Constants, prepare, cleanup

SIGN_METHOD = oauth.SignatureMethod_HMAC_SHA1()

class TestEcm:
    def setUp(self):
        prepare()

    def tearDown(self):
        cleanup()

    def testEcm_Get(self):
        TEST_URL_PATH = '/ecm'
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        parameters = dict()
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='GET', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='GET', headers=headers)
        ecm = json.loads(content)
        assert_equals(resp['status'],'200')
        assert_equals(len(ecm), 2)
        assert_equals(ecm['version'], '0.1')
        assert_equals(ecm['installedDate'], '19/04/2011')