import httplib2
import json
import oauth2 as oauth
import urllib
from nose.tools import *
from pylabs import q, i
from . import Constants, prepare, cleanup

SIGN_METHOD = oauth.SignatureMethod_HMAC_SHA1()

class TestDashboard:
    def setUp(self):
        prepare()

    def tearDown(self):
        cleanup()

    def testDashboard_Get(self):
        TEST_URL_PATH = '/dashboard?guid=%s' % Constants.DASHBOARD1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        parameters = {'guid': Constants.DASHBOARD1_GUID}
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='GET', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='GET', headers=headers)
        jsonDict = json.loads(content)
        
        assert_equals(resp['status'],'200')
        assert_equal(len(jsonDict), 5)
        assert_true(jsonDict.has_key('guid'))
        assert_true(jsonDict.has_key('title'))
        assert_true(jsonDict.has_key('order'))
        assert_true(jsonDict.has_key('url'))
        assert_true(jsonDict.has_key('widgets'))
        assert_equal(jsonDict['guid'], Constants.DASHBOARD1_GUID)
        assert_equal(jsonDict['title'], Constants.DASHBOARD1_NAME)
        assert_equal(jsonDict['order'], 1)
        widgets = jsonDict['widgets']
        assert_equal(len(widgets), 2)
        widget1Found = False
        widget2Found = False
        for widget in widgets:
            assert_equal(len(widget), 9)
            assert_true(widget.has_key('collapsed'))
            assert_true(widget.has_key('column'))
            assert_true(widget.has_key('guid'))
            assert_true(widget.has_key('height'))
            assert_true(widget.has_key('order'))
            assert_true(widget.has_key('title'))
            assert_true(widget.has_key('url'))
            assert_true(widget.has_key('widgettype'))
            assert_true(widget.has_key('width'))
            if widget['guid'] == Constants.WIDGET1_GUID:
                assert_equal(widget['collapsed'], False)
                assert_equal(widget['column'], 2)
                assert_equal(widget['guid'], Constants.WIDGET1_GUID)
                assert_equal(widget['height'], 500)
                assert_equal(widget['order'], 2)
                assert_equal(widget['title'], Constants.WIDGET1_NAME)
                assert_equal(widget['width'], 1)
                widgetType = widget['widgettype']
                assert_equal(len(widgetType), 5)
                assert_true(widgetType.has_key('guid'))
                assert_true(widgetType.has_key('icon'))
                assert_true(widgetType.has_key('name'))
                assert_true(widgetType.has_key('packagename'))
                assert_true(widgetType.has_key('packageversion'))
                assert_equal(widgetType['guid'], Constants.WIDGETTYPE1_GUID)
                assert_equal(widgetType['name'], Constants.WIDGETTYPE1_NAME)
                assert_equal(widgetType['icon'], "%s.png" % Constants.WIDGETTYPE1_NAME)
                assert_equal(widgetType['packagename'], "racktivity_%s" % Constants.WIDGETTYPE1_NAME)
                assert_equal(widgetType['packageversion'], '1.1')
                widget1Found = True
            elif widget['guid'] == Constants.WIDGET2_GUID:
                assert_equal(widget['collapsed'], False)
                assert_equal(widget['column'], 3)
                assert_equal(widget['guid'], Constants.WIDGET2_GUID)
                assert_equal(widget['height'], 500)
                assert_equal(widget['order'], 1)
                assert_equal(widget['title'], Constants.WIDGET2_NAME)
                assert_equal(widget['width'], 1)
                widgetType = widget['widgettype']
                assert_equal(len(widgetType), 5)
                assert_true(widgetType.has_key('guid'))
                assert_true(widgetType.has_key('icon'))
                assert_true(widgetType.has_key('name'))
                assert_true(widgetType.has_key('packagename'))
                assert_true(widgetType.has_key('packageversion'))
                assert_equal(widgetType['guid'], Constants.WIDGETTYPE2_GUID)
                assert_equal(widgetType['name'], Constants.WIDGETTYPE2_NAME)
                assert_equal(widgetType['icon'], "%s.png" % Constants.WIDGETTYPE2_NAME)
                assert_equal(widgetType['packagename'], "racktivity_%s" % Constants.WIDGETTYPE2_NAME)
                assert_equal(widgetType['packageversion'], '1.1')
                widget2Found = True
            else:
                raise AssertionError("Unexpected widget found")
        assert_true(widget1Found)
        assert_true(widget2Found)

    def testDashboard_Put(self):
        NEW_TITLE = "Updated"
        TEST_URL_PATH = '/dashboard?guid=%s' % Constants.DASHBOARD1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        parameters = {'guid': Constants.DASHBOARD1_GUID, 'order': 3, 'title': NEW_TITLE}
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
        dashboard = osis.dashboard.get(Constants.DASHBOARD1_GUID)
        assert_equals(dashboard.title, NEW_TITLE)
        assert_equals(dashboard.order, 3)

    def testDashboard_Delete(self):
        TEST_URL_PATH = '/dashboard?guid=%s' % Constants.DASHBOARD1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        parameters = {'guid': Constants.DASHBOARD1_GUID}
        body = urllib.urlencode(parameters)
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='DELETE', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        headers['Content-type'] = 'application/x-www-form-urlencoded'
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='DELETE', body=body, headers=headers)
        assert_equals(resp['status'],'200')

        osis = i.config.osisconnection.find('ecm_persist')
        filter = osis.dashboard.getFilterObject()
        filter.add('view_dashboard_list', 'guid', Constants.DASHBOARD1_GUID)
        dashboards = osis.dashboard.find(filter)
        assert_equals(len(dashboards), 0)

    def testDashboard_Post(self):
        NEW_WIDGET_NAME = "New Widget"
        TEST_URL_PATH = '/dashboard?guid=%s' % Constants.DASHBOARD1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        parameters = {'guid': Constants.DASHBOARD1_GUID, 'title': NEW_WIDGET_NAME, 'column': 1, 'order': 2, 'width': 1, 'height':100, 'collapsed': True, 'typeguid': Constants.WIDGETTYPE1_GUID}
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
        widgetGuid = jsonDict['guid']

        osis = i.config.osisconnection.find('ecm_persist')
        widget = osis.widget.get(widgetGuid)
        assert_equals(widget.title, NEW_WIDGET_NAME)
        assert_equals(widget.column, 1)
        assert_equals(widget.order, 2)
        assert_equals(widget.width, 1)
        assert_equals(widget.height, 100)
        assert_equals(widget.collapsed, True)
        assert_equals(widget.widgettypeguid, Constants.WIDGETTYPE1_GUID)