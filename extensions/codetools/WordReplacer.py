# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

from pymonkey import q
from pymonkey.Shell import *
import re,random


class Synonym():
    def __init__(self,name='',replaceWith='', simpleSearch="", addConfluenceLinkTags=False, replaceExclude=''):
        """
        @param name: Name of the sysnoym
        @param replaceWith: The replacement of simpleSearch
        @param simpleSearch: Search string that'll be replaced with replaceWith
        @addConfluenceLinkTags: True to add confluence tags around the synonym
        @defSynonym: If True then this is a definition synonym, which can be used in spectools
        """
        self.simpleSearch=simpleSearch
        self.regexFind=""
        self.regexFindForReplace=""
        self.name = name
        self.replaceWith=replaceWith
        self.addConfluenceLinkTags=addConfluenceLinkTags
        self.replaceExclude = replaceExclude
        self._markers=dict()
        if simpleSearch<>"":
            search=simpleSearch.replace("?","[ -_]?")  #match " " or "-" or "_"  one or 0 time  
            if addConfluenceLinkTags:
                bracketMatchStart="(\[ *|)"
                bracketMatchStop="( *\]|)"
            else:
                bracketMatchStart=""
                bracketMatchStop=""                                
            self.regexFind=r"(?i)%s\b%s\b%s" % (bracketMatchStart,search.lower(),bracketMatchStop)
            #self.regexFind=r"%s\b%s\b%s" % (bracketMatchStart,search.lower(),bracketMatchStop)
            self.regexFindForReplace=self.regexFind
        
    def setRegexSearch(self,regexFind,regexFindForReplace):
        self.regexFind=regexFind
        if regexFindForReplace=="":
            regexFindForReplace=regexFind
        self.regexFindForReplace=regexFindForReplace
        self.simpleSearch=""

    def replace(self,text):
        if self.replaceExclude:
            # Check for any def tag that contains name "e.g: [ Q-Layer ]", remove them and put markers in place
            text=self._replaceDefsWithMarkers(text)
        text=q.codetools.regex.replace(regexFind=self.regexFind,regexFindsubsetToReplace=self.regexFindForReplace\
                                       ,replaceWith=self.replaceWith,text=text)
        if self.replaceExclude:
            # Remove the markers and put the original def tags back
            text=self._replaceMarkersWithDefs(text)
        return text

    def _replaceDefsWithMarkers(self,text):
        """
        Search for any def tags that contains the name of this synonym  "e.g [Q-layer]" in text and replace that with a special marker. Also it stores markers and replaced string into the dict _markers
        """
        # patterns you don't want to be replaced
        pat=self.replaceExclude

        matches = q.codetools.regex.findAll(pat,text)

        for match in matches:
            mark = "$$MARKER$$%s$$"%random.randint(0,1000)
            self._markers[mark] = match
            match = re.escape(match)
            text=q.codetools.regex.replace(regexFind=match,regexFindsubsetToReplace=match,replaceWith=mark,text=text)
        return text

    def _replaceMarkersWithDefs(self,text):
        """
        Removes markers out of text and puts the original strings back
        """
        for marker,replacement in self._markers.iteritems():
            marker = re.escape(marker)
            text=q.codetools.regex.replace(regexFind=marker,regexFindsubsetToReplace=marker,replaceWith=replacement,text=text)
        return text

    def __str__(self):
        out="name:%s simple:%s regex:%s regereplace:%s replacewith:%s\n" % (self.name,self.simpleSearch,self.regexFind,self.regexFindForReplace,self.replaceWith)
        return out

    def __repr__(self):
        return self.__str__()
    
class WordReplacer():
    
    def __init__(self):
        self.synonyms=[] #array Synonym()
            
    def synonymsPrint(self):
        for syn in self.synonyms:
            print syn

    def synonymAdd(self,name='', simpleSearch='', regexFind='', regexFindForReplace='', replaceWith='',replaceExclude='', addConfluenceLinkTags =False):
        """
        Adds a new synonym to this replacer
        @param name: Synonym name
        @param simpleSearch: Search text for sysnonym, if you supply this, then the synonym will automatically generate a matching regex pattern that'll be used to search for this string, if you want to specificy the regex explicitly then use regexFind instead.
        @param regexFind: Provide this regex only if you didn't provide simpleSearch, it represents the regex that'll be used in search for this synonym . It overrides the default synonym search pattern
        @param regexFindForReplace: The subset within regexFind that'll be replaced for this synonym
        """
        synonym = Synonym(name,replaceWith, simpleSearch, addConfluenceLinkTags, replaceExclude)
        if regexFind:
            synonym.setRegexSearch(regexFind, regexFindForReplace)
        self.synonyms.append(synonym)

    def reset(self):
        self.synonyms=[]
                    
    def synonymsAddFromFile(self,path,addConfluenceLinkTags=False):
        """
        load synonym satements from a file in the following format
        [searchStatement]:[replaceto]
        or
        '[regexFind]':'[regexReplace]':replaceto
        note: delimiter is :
        note: '' around regex statements
        e.g.
        ******
        master?daemon:ApplicationServer
        application?server:ApplicationServer
        'application[ -_]+server':'application[ -_]+server':ApplicationServer
        '\[application[ -_]+server\]':'application[ -_]+server':ApplicationServer        
        ******
        @param addConfluenceLinkTags id True then replaced items will be surrounded by [] (Boolean)
        """
        txt=q.system.fs.fileGetContents(path)
        for line in txt.split("\n"):
            line=line.strip()
            if line<>"" and line.find(":")<>-1:
                if q.codetools.regex.match("^'",line):
                    #found line which is regex format
                    splitted=line.split("'")
                    if len(splitted)<>4:
                        raise RuntimeError("syntax error in synonym line (has to be 2 'regex' statements" % line)
                    syn=Synonym(replaceWith=splitted[2])
                    syn.setRegexSearch(regexFind=splitted[0],regexFindForReplace=splitted[1])
                else:    
                    find=line.split(":")[0]
                    replace=line.split(":")[1].strip()
                    syn=Synonym(replaceWith=replace,simpleSearch=find,addConfluenceLinkTags=addConfluenceLinkTags)
                self.synonyms.append(syn)

    def removeConfluenceLinks(self,text):
        """
        find [...] and remove the [ and the ]
        @todo 2
        """
        raise RuntimeError("@todo needs to be done, is not working now")
        def replaceinside(matchobj):
            match=matchobj.group()
            #we found a match now
            #print "regex:%s match:%s replace:%s" % (searchitem[1],match,searchitem[2])
            if match.find("|")==-1:
                match=re.sub("( *\])|(\[ *)","",match)
                toreplace=searchitem[2]
                searchregexReplace=searchitem[1]
                match = re.sub(searchregexReplace, toreplace,match)  
                return match
            else:
                return match
        for searchitem in self.synonyms:
            #text = re.sub(searchitem[0],searchitem[1], text)               
            text = re.sub(searchitem[0], replaceinside, text)
        return text        
        
    def replace(self,text):        
        for syn in self.synonyms:
            text=syn.replace(text)
        return text        
        
    def replaceInConfluence(self, text):
        """
        @[..|.] will also be looked for and replaced
        """
        def replaceinside(matchobj):
            match=matchobj.group()
            #we found a match now
            #print "regex:%s match:%s replace:%s" % (searchitem[1],match,searchitem[2])
            if match.find("|")==-1:
                match=re.sub("( *\])|(\[ *)","",match)
                match = re.sub(syn.regexFind, syn.replaceWith,match)  
                return match
            else:
                return match
        for syn in self.synonyms:       
            #call function replaceinside when match
            text = re.sub(syn.regexFind, replaceinside, text)
        return text
        
    def _addConfluenceLinkTags(self,word):
        """
        add [ & ] to word
        """
        if word.find("[")==-1 and word.find("]")==-1:
            word="[%s]" % word
        return word