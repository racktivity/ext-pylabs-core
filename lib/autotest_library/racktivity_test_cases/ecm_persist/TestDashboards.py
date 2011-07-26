import httplib2
import json
import oauth2 as oauth
import urllib
from nose.tools import *
from pylabs import q, i

from . import Constants, prepare, cleanup

TEST_URL_PATH = '/dashboards'
TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
SIGN_METHOD = oauth.SignatureMethod_HMAC_SHA1()

class TestDashboards:
    def setUp(self):
        prepare()

    def tearDown(self):
        cleanup()

    def testDashboards_Get(self):
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='GET', http_url='http://racktivity%s' % TEST_URL_PATH)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='GET', headers=headers)
        jsonDict = json.loads(content)
        
        assert_equals(resp['status'],'200')
        assert_equal(len(jsonDict), 2)
        assert_true(jsonDict.has_key('dashboards'))
        assert_true(jsonDict.has_key('selecteddashboardguid'))
        assert_equal(jsonDict['selecteddashboardguid'], Constants.DASHBOARD1_GUID)
        dashboards = jsonDict['dashboards']
        assert_equal(len(dashboards), 2)
        dashboard1Found = False
        dashboard2Found = False
        for dashboard in dashboards:
            assert_equal(len(dashboard), 4)
            assert_true(dashboard.has_key('guid'))
            assert_true(dashboard.has_key('title'))
            assert_true(dashboard.has_key('order'))
            assert_true(dashboard.has_key('url'))
            if dashboard['guid'] == Constants.DASHBOARD1_GUID:
                assert_equal(dashboard['title'], Constants.DASHBOARD1_NAME)
                assert_equal(dashboard['order'], 1)
                dashboard1Found = True
            elif dashboard['guid'] == Constants.DASHBOARD2_GUID:
                assert_equal(dashboard['title'], Constants.DASHBOARD2_NAME)
                assert_equal(dashboard['order'], 2)
                dashboard2Found = True
            else:
                raise AssertionError("Unexpected dashboard found")
        assert_true(dashboard1Found)
        assert_true(dashboard2Found)

    def testDashboards_Put(self):
        parameters = {'selecteddashboardguid': Constants.DASHBOARD2_GUID}
        body = urllib.urlencode(parameters)
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='PUT', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        headers['Content-type'] = 'application/x-www-form-urlencoded'
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='PUT', body=body, headers=headers)
        assert_equals(resp['status'],'200')
        
        osis = i.config.osisconnection.find('ecm_persist')
        userFilter = osis.uiuser.getFilterObject()
        userFilter.add('view_uiuser_list', 'name', Constants.USER_NAME)
        userGuids = osis.uiuser.find(userFilter)
        assert_equal(len(userGuids), 1)
        userGuid= userGuids[0]
        user = osis.uiuser.get(userGuid)
        assert_equal(user.selecteddashboardguid, Constants.DASHBOARD2_GUID)

    def testDashboards_Post(self):
        NEW_DASHBOARD_NAME = "New Dashboard"
        parameters = {'guid': Constants.DASHBOARD1_GUID, 'title': NEW_DASHBOARD_NAME, 'order': 3}
        body = urllib.urlencode(parameters)
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='POST', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        headers['Content-type'] = 'application/x-www-form-urlencoded'
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='POST', body=body, headers=headers)
        assert_equals(resp['status'],'200')
        jsonDict = json.loads(content)
        dashboardGuid = jsonDict['guid']

        osis = i.config.osisconnection.find('ecm_persist')
        dashboard = osis.dashboard.get(dashboardGuid)
        assert_equals(dashboard.title, NEW_DASHBOARD_NAME)
        assert_equals(dashboard.order, 3)