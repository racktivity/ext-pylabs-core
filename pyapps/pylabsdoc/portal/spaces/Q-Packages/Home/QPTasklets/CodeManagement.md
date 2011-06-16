@metadata title=CodeManagement Tasklet

[[code]]
# -*- coding: utf-8 -*-
__author__ = 'incubaid'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    
    # Download the ocaml sources from http://caml.inria.fr
    downloadSource = 'http://caml.inria.fr/pub/distrib/ocaml-3.11/'

    # QPackage version number should match the upstream version
    targetFolder = '%s-%s' % (qpackage.name, qpackage.version)
    fileName = '%s.tar.gz' % targetFolder

    remoteArchive = q.system.fs.joinPaths(downloadSource, fileName)
    localArchive = 'file://%s' % q.system.fs.joinPaths(q.dirs.tmpDir, fileName)
    q.cloud.system.fs.copyFile(remoteArchive, localArchive)
    q.system.fs.targzUncompress(q.system.fs.joinPaths(q.dirs.tmpDir, fileName), q.system.fs.joinPaths(q.dirs.tmpDir), False)
    
[[/code]]