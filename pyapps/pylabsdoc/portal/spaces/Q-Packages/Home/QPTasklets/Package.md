@metadata title=Package Tasklet

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