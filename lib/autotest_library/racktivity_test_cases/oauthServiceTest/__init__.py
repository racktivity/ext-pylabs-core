import httplib
import oauth2 as oauth
import time

import urlparse
import ConfigParser
import os
import json
import ast
from pylabs import q

def setup():
    pass


def teardown():
    pass

class DistibutedLoginClient:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), "dist_auth.conf"))
        self.__con = httplib.HTTPConnection(self.config.get("ecs", "IP"), self.config.get("ecs", "PORT"))

    def callECS(self, method="useraccess", **args):
        data = json.dumps(args)
        headers = {'Content-Type': "application/vap.racktivity.com.%s+json" % (method),
                   'Content-Length': len(data)}
        self.__con.request("POST", "/%s" % method, body=data, headers=headers)
        res = self.__con.getresponse()
        if res.status == 200:
            return json.loads(res.read())
        else:
            raise Exception(res.reason, res.status)
        self.__con = httplib.HTTPConnection(self.config.get('ecs','IP'), self.config.get('ecs','PORT'))
    
    def getToken(self):
        consumer = oauth.Consumer(self.config.get('main', 'CONSUMER_KEY'), self.config.get('main', 'CONSUMER_SECRET'))
        client = oauth.Client(consumer)
        access_token_url = self.config.get('main', 'ACCESS_TOKEN_URL')
        self._pause()
        token = oauth.Token('','')
        token.set_verifier('')
        client = oauth.Client(consumer, token)
        client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1()) 
        resp, content = client.request(access_token_url, "POST", 'user='+self.config.get('main', 'CONSUMER_KEY')+'&password='+self.config.get('main', 'CONSUMER_SECRET'))
        print content
        access_token = dict(urlparse.parse_qsl(content))
        print access_token
        return access_token
        
    
    def send_request(self, headers):
        conn = httplib.HTTPConnection('localhost','80')
        
        conn.request("GET", self.config.get('main', 'URL'), body='', headers=headers)
        response = conn.getresponse()
        return response.read()
        
    
    def tamperData(self, access_token, action):
        print 'tamperData', action
        client = q.clients.arakoon.getClient(self.config.get('arakoon', 'cluster_name'))
        token_attributes = ast.literal_eval(client.get('token_$(%s)'%access_token['oauth_token']))
        
        if action == 'EXPIRED':
            print 'before ', str(token_attributes)
            token_attributes['validuntil'] = str(time.time())
            client.set(key='token_$(%s)'%access_token['oauth_token'], value=str(token_attributes))
            return access_token
        if action == 'INVALIDATE_KEY':
            access_token['oauth_token'] = "token_XYZ"
            return access_token
        if action == 'INVALIDATE_SECRET':
            access_token['oauth_token_secret'] = "token_XYZ"
            return access_token
        

    def _pause(self):
        print ''
        time.sleep(1)
