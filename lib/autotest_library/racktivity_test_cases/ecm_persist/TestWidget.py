import httplib2
import json
import oauth2 as oauth
import urllib
from nose.tools import *
from pylabs import q, i
from . import Constants, prepare, cleanup

SIGN_METHOD = oauth.SignatureMethod_HMAC_SHA1()

class TestWidget:
    def setUp(self):
        prepare()

    def tearDown(self):
        cleanup()

    def testWidget_Get(self):
        TEST_URL_PATH = '/widget?guid=%s' % Constants.WIDGET1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        consumer = oauth.Consumer(Constants.CONSUMER_KEY, '')
        token = oauth.Token("token_$(%s)" % Constants.TOKEN_KEY, Constants.TOKEN_SECRET)
        parameters = {'guid': Constants.WIDGET1_GUID}
        req = oauth.Request.from_consumer_and_token(consumer, token, http_method='GET', http_url='http://racktivity%s' % TEST_URL_PATH, parameters=parameters)
        req.sign_request(SIGN_METHOD, consumer, token)
        headers = req.to_header()
        http = httplib2.Http()
        resp, content = http.request(TEST_URL, method='GET', headers=headers)
        widget = json.loads(content)
        assert_equals(resp['status'],'200')
        assert_equal(len(widget), 10)
        assert_true(widget.has_key('collapsed'))
        assert_true(widget.has_key('column'))
        assert_true(widget.has_key('guid'))
        assert_true(widget.has_key('height'))
        assert_true(widget.has_key('order'))
        assert_true(widget.has_key('title'))
        assert_true(widget.has_key('url'))
        assert_true(widget.has_key('widgetsettings'))
        assert_true(widget.has_key('widgettype'))
        assert_true(widget.has_key('width'))
        
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

        widgetsettings = widget['widgetsettings']
        assert_equal(len(widgetsettings), 2)
        assert_true(widgetsettings.has_key('wt1_setting1'))
        assert_true(widgetsettings.has_key('wt1_setting2'))
        assert_equal(widgetsettings['wt1_setting1'], 'wt1_value1')
        assert_equal(widgetsettings['wt1_setting2'], 'wt1_value2')

    def testWidget_Put(self):
        NEW_TITLE = "Updated widget"
        NEW_ORDER = 1
        NEW_COLUMN = 1
        NEW_HEIGHT = 20
        NEW_WIDTH = 2
        NEW_SETTING_VALUE1 = "wt1_updated value1"
        NEW_SETTING_VALUE2 = "wt1_updated value2"
        TEST_URL_PATH = '/widget?guid=%s' % Constants.WIDGET1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        parameters = {'guid': Constants.WIDGET1_GUID, 
                      'order': NEW_ORDER,
                      'title': NEW_TITLE,
                      'column': NEW_COLUMN,
                      'height': NEW_HEIGHT,
                      'width': NEW_WIDTH,
                      'collapsed': 'True',
                      'widgetsettings': '{"wt1_setting1": "%s", "wt1_setting2": "%s"}' % (NEW_SETTING_VALUE1, NEW_SETTING_VALUE2)
                      }
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
        widget = osis.widget.get(Constants.WIDGET1_GUID)
        assert_equals(widget.title, NEW_TITLE)
        assert_equals(widget.order, NEW_ORDER)
        assert_equals(widget.column, NEW_COLUMN)
        assert_true(widget.collapsed)
        assert_equals(widget.width, NEW_WIDTH)
        assert_equals(widget.height, NEW_HEIGHT)
        setting1found = False
        setting2found = False
        for setting in widget.widgetsettings:
            if setting.key == 'wt1_setting1':
                setting1found = True
                assert_equals(setting.value, NEW_SETTING_VALUE1)
            elif setting.key == 'wt1_setting2':
                setting2found = True
                assert_equals(setting.value, NEW_SETTING_VALUE2)
            else:
                raise AssertionError("Unexpected setting found")
        assert_true(setting1found)
        assert_true(setting2found)

    def testWidget_Delete(self):
        TEST_URL_PATH = '/widget?guid=%s' % Constants.WIDGET1_GUID
        TEST_URL = 'http://127.0.0.1:8999/ecm_persist%s' % TEST_URL_PATH
        parameters = {'guid': Constants.WIDGET1_GUID}
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
        filter = osis.widget.getFilterObject()
        filter.add('view_widget_list', 'guid', Constants.WIDGET1_GUID)
        widgets = osis.widget.find(filter)
        assert_equals(len(widgets), 0)