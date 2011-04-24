#!/usr/bin/evn python

import urllib2, urllib
import base64
import json

class Hudson(object):

    def getClient(self, baseurl="http://cimaster.incubaid.com", username=None, password=None):
        return HudsonClient(baseurl, username, password)


class HudsonClient(object):
    def __init__(self, baseurl, username=None, password=None):
        self.baseurl = baseurl
        self.headers = dict()
        if username and password:
            raw = "%s:%s" % (username, password)
            basepass = base64.b64encode(raw).strip()
            self.headers['Authorization'] = "Basic %s" % basepass
        self.username = username
        self.password = password
        self._api = None

    def _get_data(self, url):
        req = urllib2.Request(url, headers=self.headers)
        urlinfo = urllib2.urlopen(req)
        rawdata = urlinfo.read()
        urlinfo.close()
        return rawdata

    def _load_api(self, reload=False):
        if not self._api or reload:
            apiurl = self.baseurl + "/api/json"
            self._api = json.loads(self._get_data(apiurl))
        return self._api

    api = property(fget=_load_api)

    def listJobs(self):
        jobs = [ d['name'] for d in self.api['jobs'] ]
        return jobs

    def build(self, jobname, **kwargs):
        buildtype = "build"
        extra = ""
        if len(kwargs) > 0:
            buildtype = "buildWithParameters"
            extra = "?%s" % urllib.urlencode(kwargs)
        url = "%s/job/%s/%s%s" % (self.baseurl, jobname, buildtype, extra)
        self._get_data(url)



