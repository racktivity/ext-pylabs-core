import httplib2
import json
import oauth2 as oauth
import urllib
from nose.tools import *
from pylabs import q, i
from . import Constants, prepare, cleanup

SIGN_METHOD = oauth.SignatureMethod_HMAC_SHA1()

class TestWidgetTypes:
    def setUp(self):
        prepare()

    def tearDown(self):
        cleanup()

    def testWidgetTypes_Get(self):
        TEST_URL_PATH = '/widgettypes'
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        parameters = dict()
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='GET', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='GET', headers=headers)
        jsonDict = json.loads(content)
        assert_equals(resp['status'],'200')
        assert_true(len(jsonDict) >= 2)
        type1found = False
        type2found = False
        for widgetType in jsonDict:
            if widgetType['guid'] == Constants.WIDGETTYPE1_GUID:
                type1found = True
                assert_equals(len(widgetType), 7)
                assert_equals(widgetType['name'], Constants.WIDGETTYPE1_NAME)
                assert_equals(widgetType['icon'], "%s.png" % Constants.WIDGETTYPE1_NAME)
                assert_equals(widgetType['packagename'], "racktivity_%s" % Constants.WIDGETTYPE1_NAME)
                assert_equals(widgetType['packageversion'], "1.1")
                assert_equals(widgetType['tags'], Constants.WIDGETTYPE1_TAGS)
                assert_equals(widgetType['description'], Constants.WIDGETTYPE1_DESCRIPTION)
            elif widgetType['guid'] == Constants.WIDGETTYPE2_GUID:
                type2found = True
                assert_equals(len(widgetType), 7)
                assert_equals(widgetType['name'], Constants.WIDGETTYPE2_NAME)
                assert_equals(widgetType['icon'], "%s.png" % Constants.WIDGETTYPE2_NAME)
                assert_equals(widgetType['packagename'], "racktivity_%s" % Constants.WIDGETTYPE2_NAME)
                assert_equals(widgetType['packageversion'], "1.1")
                assert_equals(widgetType['tags'], Constants.WIDGETTYPE2_TAGS)
                assert_equals(widgetType['description'], Constants.WIDGETTYPE2_DESCRIPTION)
        assert_true(type1found)
        assert_true(type2found)


    def testWidgetType_Get(self):
        TEST_URL_PATH = '/widgettype?guid=%s' % Constants.WIDGETTYPE1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        parameters = {'guid': Constants.WIDGETTYPE1_GUID}
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='GET', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='GET', headers=headers)
        widgetType = json.loads(content)
        assert_equals(resp['status'],'200')
        assert_equals(len(widgetType), 7)
        assert_equals(widgetType['guid'], Constants.WIDGETTYPE1_GUID)
        assert_equals(widgetType['name'], Constants.WIDGETTYPE1_NAME)
        assert_equals(widgetType['icon'], "%s.png" % Constants.WIDGETTYPE1_NAME)
        assert_equals(widgetType['packagename'], "racktivity_%s" % Constants.WIDGETTYPE1_NAME)
        assert_equals(widgetType['packageversion'], "1.1")
        assert_equals(widgetType['tags'], Constants.WIDGETTYPE1_TAGS)
        assert_equals(widgetType['description'], Constants.WIDGETTYPE1_DESCRIPTION)