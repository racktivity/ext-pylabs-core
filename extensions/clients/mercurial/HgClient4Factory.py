

#import os.path
#import httplib
#from urlparse import urlparse, urlunparse
#import pymonkey
from pymonkey import q
from pymonkey.Shell import *
from HgClient4 import HgClient4

class HgClient4Factory:
        
    def getclient(self,hgbasedir,remoteUrl,branchname="default"):
        """
        return a mercurial tool which you can help to manipulate a hg repository
        @param base dir where local hgrepository will be stored
        @param remote url of hg repository, e.g. https://login:passwd@bitbucket.org/despiegk/ssospecs/  #DO NOT FORGET LOGIN PASSWD
        """
        return HgClient4(hgbasedir,remoteUrl,branchname)
    

