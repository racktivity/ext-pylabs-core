@metadata title=Package Tasklet

####When using a recipe file:
[[code]]
__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesDir = qpackage.getPathFiles()
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    relativePath = q.system.fs.joinPaths("generic", "pyapps", "newapp")
    q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackage.getPathSourceCode(), relativePath), q.system.fs.joinPaths(filesDir, relativePath))
[[/code]]

* getPathFiles: function that retrieves the files directory of a package inside the Q-Packages directory of PyLabs, for example `/opt/qbase5/var/qpackages4/files/<domain>/<package>/<version>`.
* getPathSourceCode: function that retrieves the directory with the source code for the package, for example `/opt/qbase5/var/src/<package>/<version>`


####When manually assembling the package

[[code]]
# -*- coding: utf-8 -*-
__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    
    extractedLocation = q.system.fs.joinPaths(q.dirs.tmpDir, '%s-%s' % (qpackage.name, qpackage.version))
    localInstallDir = q.system.fs.joinPaths(extractedLocation, 'target-pylabs')

    # First copy objinfo & dumpobj to the bin folder
    q.system.fs.copyFile(q.system.fs.joinPaths(extractedLocation, 'tools', 'dumpobj'), q.system.fs.joinPaths(localInstallDir,'bin','ocamldumpobj'))
    q.system.fs.copyFile(q.system.fs.joinPaths(extractedLocation, 'tools', 'dumpapprox'), q.system.fs.joinPaths(localInstallDir,'bin','ocamldumpapprox'))
    q.system.fs.copyFile(q.system.fs.joinPaths(extractedLocation, 'tools', 'objinfo'), q.system.fs.joinPaths(localInstallDir,'bin','ocamlobjinfo'))

    # Putting the egg in var/tmp. See the install tasklet for part 2
    targetLocation = q.system.fs.joinPaths(qpackage.getPathFiles(), q.platform.name)
    q.system.fs.copyDirTree(localInstallDir, targetLocation, keepsymlinks=True)
[[/code]]