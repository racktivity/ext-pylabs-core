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

from pylabs.InitBase import q
from pylabs.clients.svn.SvnRecipe import SvnRecipe
from pylabs.clients.svn.SvnConnection import SvnConnection
import pysvn, re, random
import unittest

class TestSvnRecipe(unittest.TestCase):
    
    def setUp(self):
        self.SVN_URL = "http://svn.pylabs.org/svn/code/trunk"
        # Change to the svn dir that will be used in the test "ie. checked out, checked in..etc" 
        # NOTE: During the test some files of that directory will be modified, please make sure to provide a directory that nobody uses
        self.SVN_TEST_MODULE = ""
        self.SVN_SOURCE = self.SVN_URL + self.SVN_TEST_MODULE
        self.SVN_CLIENT_DEST = q.system.fs.joinPaths(q.dirs.baseDir,"tmp","svn_client_test_" + str(random.randint(1,10000)))
        self.SVN_RECIPE_DEST = q.system.fs.joinPaths(q.dirs.baseDir,"tmp","svn_recipe_test_" + str(random.randint(1,10000)))
        # Change to your svn username
        self.SVN_LOGIN = ""
        # Change to your svn password
        self.SVN_PASS = ""
        self.CHECKIN_LOG_MESSAGE = 'STAL-0000\nReviewer: abdallaa\nThis is a commit made by the svn unit test'
        # Prepare local svn client
        self.svnClient = pysvn.Client()
        self.svnClient.set_default_username(self.SVN_LOGIN)
        self.svnClient.set_default_password(self.SVN_PASS)
        self.svnConnection = SvnConnection(self.SVN_URL, self.SVN_LOGIN, self.SVN_PASS)

    def test_checkout(self):                
        recipe = SvnRecipe()
        self.svnClient.checkout(self.SVN_SOURCE, self.SVN_CLIENT_DEST)
        recipe.addSource(self.svnConnection, self.SVN_TEST_MODULE, self.SVN_RECIPE_DEST)
        recipe.executeTaskletAction("checkout")
        if not self.assertEqualDirs(self.SVN_CLIENT_DEST, self.SVN_RECIPE_DEST):
            raise AssertionError("Checkout test failed, the two checkedouts are not the same")

    def test_export(self):        
        recipe = SvnRecipe()
        self.svnClient.export(self.SVN_SOURCE, self.SVN_CLIENT_DEST)
        recipe.addSource(self.svnConnection, self.SVN_TEST_MODULE, self.SVN_RECIPE_DEST)
        recipe.executeTaskletAction("export")
        if not self.assertEqualDirs(self.SVN_CLIENT_DEST, self.SVN_RECIPE_DEST):
            raise AssertionError("Export test failed, the two checkouts are not the same")
    
    def test_update(self):
        SVN_ORIGINAL_DIR = self.SVN_CLIENT_DEST+ "_original_" + str(random.randint(0,1000))        
        self.svnClient.checkout(self.SVN_SOURCE, self.SVN_CLIENT_DEST)
        # Make a copy of the current version to update it later
        q.system.fs.copyDirTree(self.SVN_CLIENT_DEST, SVN_ORIGINAL_DIR)
        # Now choose a file in the original directory, change it and commit it
        randomFilePath = self.getRandomFileFromDir(self.SVN_CLIENT_DEST)
        randomFile = open(randomFilePath, 'a')
        randomFile.write('This is a new test line\n')
        randomFile.close()
        if self.svnClient.checkin(self.SVN_CLIENT_DEST, self.CHECKIN_LOG_MESSAGE):
            
            #Now try to update the old version, and check if the directory is equal to the checkedin one
            recipe = SvnRecipe()
            recipe.addSource(self.svnConnection, self.SVN_SOURCE, SVN_ORIGINAL_DIR)
            recipe.executeTaskletAction("update")
            
            if not self.assertEqualDirs(self.SVN_CLIENT_DEST, SVN_ORIGINAL_DIR):
                raise AssertionError("Update test failed")
        else:
            raise RuntimeError("Checkin step failed while running the update test case")
    
    def test_checkin(self):
        SVN_ORIGINAL_DIR = self.SVN_CLIENT_DEST+ "_original_" + str(random.randint(0,1000))        
        self.svnClient.checkout(self.SVN_SOURCE, self.SVN_CLIENT_DEST)
        
        # Now choose a file, change it and commit it
        randomFilePath = self.getRandomFileFromDir(self.SVN_CLIENT_DEST)
        randomFile = open(randomFilePath, 'a')
        randomFile.write('This is a new test line\n')
        randomFile.close()        
        
        recipe = SvnRecipe()
        recipe.addSource(self.svnConnection, self.SVN_SOURCE,self.SVN_CLIENT_DEST)
        recipe.executeTaskletAction("checkin")
        
        #Now checkout again the new version in a new location, and check if the directory is equal to the checkedin one
        if self.svnClient.checkout(SVN_ORIGINAL_DIR, self.CHECKIN_LOG_MESSAGE):
            if not self.assertEqualDirs(self.SVN_CLIENT_DEST, SVN_ORIGINAL_DIR):
                raise AssertionError("Checkin test failed")
        else:
            raise RuntimeError("Checkout step failed while running the checkin test case")
    
    def test_remove(self):
        self.svnClient.checkout(self.SVN_SOURCE, self.SVN_CLIENT_DEST)
        recipe = SvnRecipe()
        recipe.addSource(self.svnConnection, self.SVN_SOURCE,self.SVN_CLIENT_DEST)
        recipe.executeTaskletAction("remove")
        self.assertFalse(q.system.fs.exists(self.SVN_CLIENT_DEST))                
        
    def assertEqualDirs(self,firstPath,secondPath):
        # get content
        firstTree = q.system.fs.Walk(firstPath,1)
        # strip away the basedir
        firstTree = [ q.system.fs.pathRemoveDirPart(x,firstPath) for x in firstTree]        
        secondTree = q.system.fs.Walk(secondPath,1)
        secondTree = [ q.system.fs.pathRemoveDirPart(x,secondPath) for x in secondTree]
        if not firstTree == secondTree :
            return False
        return self.assertEqualDirsContent(firstPath,secondPath)
        
    def assertEqualDirsContent(self,firstPath,secondPath):        
        # get files in each path
        firstFiles = q.system.fs.listFilesInDir(firstPath,True)
        secondFiles = q.system.fs.listFilesInDir(secondPath,True)
        # sort them
        firstFiles.sort()
        secondFiles.sort()
        
        # get checksum of each file from first and compare to the same from second
        for file1,file2 in zip(firstFiles,secondFiles):
            file1Checksum = q.system.fs.md5sum(file1)
            file2Checksum = q.system.fs.md5sum(file2)
            if not ( re.search('\.svn',file1) or re.search('\.svn',file2) ) and not file1Checksum == file2Checksum:
                q.logger.log("files %s and %s don't have same checksum" % (file1,file2),3)
                return False
        # Files are equal
        return True        
                
    def getRandomFileFromDir(self, dirPath):
        allFiles = q.system.fs.listFilesInDir(dirPath,True)
        filesWithoutSvnFiles = [ x for x in allFiles if not re.search('\.svn',x) ]
        randomIndex = random.randint(0, len(filesWithoutSvnFiles)-1)                
        if filesWithoutSvnFiles:
            return filesWithoutSvnFiles[randomIndex]
        return None