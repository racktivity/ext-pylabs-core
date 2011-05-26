from pylabs import q

    
class QPackageDefaultFilesGenerator:
    
    def __init__(self,qpackage):
        self.qpackage=qpackage

    def generateDefaultStartStopTasklet(self):
        filePath = q.system.fs.joinPaths(self.qpackage.getPathMetadata(), 'tasklets', 'startstop.py')
        content = '''
__author__ = 'aserver'
__tags__ = 'startstop',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    def startmethod():
        pass

    def stopmethod():
        pass



    #GENERATED###################################################################
    if params['action']=="start":
        startmethod()
    if params['action']=="stop":
        stopmethod()
    if params['action']=="restart":
        stopmethod()
        startmethod()
'''
        q.system.fs.createDir(q.system.fs.getDirName(filePath))
        if not q.system.fs.exists(filePath):
            q.system.fs.writeFile(filePath, content)


    def generateDefaultBackupTasklet(self):
        filePath = q.system.fs.joinPaths(self.qpackage.getPathMetadata(), 'tasklets', 'backup.py')
        content = '''
__author__ = 'aserver'
__tags__ = 'backup',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    backupurl=params['backupurl'] #e.g. ftp://login:passwd@10.10.1.1/myroot/ @point to doc about cloudfilesystem
    if params['action']=="backup":
        pass

    if params['action']=="restore":
        pass

    if params['action']=="backupconfig":
        pass

    if params['action']=="restoreconfig":
        pass
'''
        q.system.fs.createDir(q.system.fs.getDirName(filePath))
        if not q.system.fs.exists(filePath):
            q.system.fs.writeFile(filePath, content)


    # Creating a new extension should be easy
    def generateDefaultCodeManagementTasklet(self):
        # Dont know iw we should do this..
        # First make a working version
        
        
        #content = ''
        #if repo:
            ## Todo threat extensions differently? 
            #content = '''
            #__author__ = 'aserver'
            #__tags__   = 'configure',

            #def main(q, i, params, tags):
                #qpackage = params['qpackage']
                #url = $url$
                #q.clients.hgcmd.checkout(askCredenctials("%spylabs-core/"%baseurl, 'spylabs-core'), codedir)
            #''' 
            #url = 'https://$username$:$password$@bitbucket.org/despiegk/$packageName$/'
            #url = url.replace('$packageName$', name)
            #url = url.replace('$username$',    q.gui.dialog.askString('bitbucket username'))
            #url = url.replace('$password$',    q.gui.dialog.askString('bitbucket password'))
            #content.replace('$url$', url)
            ## Please make sure the repository: exists and that you have the credential to write to it
            #q.gui.dialog.message('A codemanagement tasklet )
            #q.gui.dialog.message('Please make sure the repository: %s exists and that you have the credential to write to it.' % url)
        #else:
        
        filePath = q.system.fs.joinPaths(self.qpackage.getPathMetadata(), 'tasklets', 'codemanagement.py')
        content = '''
__author__ = 'aserver'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    qpackage.checkoutRecipe()
'''
        q.system.fs.createDir(q.system.fs.getDirName(filePath))
        if not q.system.fs.exists(filePath):
            q.system.fs.writeFile(filePath, content)
    
    def generateDefaultInstallTasklet(self):
        filePath = q.system.fs.joinPaths(self.qpackage.getPathMetadata(), 'tasklets',  'install.py')
        content = '''
__author__ = 'aserver'
__tags__   = 'install',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    qpackage.copyFiles()
    #q.platform.ubuntu.check()
    #from pylabs.Shell import *
    #ipshell()
    #q.platform.ubuntu.updatePackageMetadata()
    #q.platform.ubuntu.checkInstall("eric","eric")
    #q.platform.ubuntu.install("python-qt4-sql")
    #path=qpackage.getPathFiles()
    #path=q.system.fs.joinPaths(path,"rootfs")
    #q.system.fs.copyDirTree(path, "/")

'''
        q.system.fs.createDir(q.system.fs.getDirName(filePath))
        if not q.system.fs.exists(filePath):
            q.system.fs.writeFile(filePath, content)
    
    def generateDefaultPackageTasklet(self):
        filePath = q.system.fs.joinPaths(self.qpackage.getPathMetadata(), 'tasklets', 'package.py')
        content = '''
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    q.system.fs.removeDirTree(qpackage.getPathFiles())
    q.system.fs.copyDirTree(qpackage.getPathSourceCode(), qpackage.getPathFiles())
    
'''
        q.system.fs.createDir(q.system.fs.getDirName(filePath))
        if not q.system.fs.exists(filePath):
            q.system.fs.writeFile(filePath, content)
    
    def generateDefaultConfigureTasklet(self):
        filePath = q.system.fs.joinPaths(self.qpackage.getPathMetadata(), 'tasklets' , 'configure.py')
        content = '''
__author__ = 'aserver'
__tags__   = 'configure',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    
'''
        q.system.fs.createDir(q.system.fs.getDirName(filePath))
        if not q.system.fs.exists(filePath):
            q.system.fs.writeFile(filePath, content)
    
    # Called when this qpackage is newly created and does not have any files yet
    def createDefaultFiles(self):
        ##self.assertAccessable()
        self.generateDefaultInstallTasklet()
        self.generateDefaultPackageTasklet()
        self.generateDefaultConfigureTasklet()
        self.generateDefaultCodeManagementTasklet()
        self.generateDefaultBackupTasklet()
        self.generateDefaultStartStopTasklet()
