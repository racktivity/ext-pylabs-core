@metadata title=Compile Tasklet

[[code]]
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

__author__ = 'amplidata'
__tags__   = 'compile',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    targetFolderName = '%s-%s' % (qpackage.name, qpackage.version)
    extractedLocation = q.system.fs.joinPaths(q.dirs.tmpDir, targetFolderName)
    # If yo change the path below, also adapt the PREFIX variable in the Makefile included in the tasklets folder
    localInstallDir = q.system.fs.joinPaths(extractedLocation, 'target-pylabs')

    # Calculate the required options and environment variables
    additionalPaths = [q.system.fs.joinPaths(q.dirs.baseDir, 'sbin'),
                       q.system.fs.joinPaths(q.dirs.appDir, 'gcc', 'bin'),
                       q.system.fs.joinPaths(q.dirs.appDir, 'gcc', 'sbin')]
    buildEnv = os.environ.copy()
    additionalPaths.append(buildEnv['PATH'])
    buildEnv['PATH'] = os.path.pathsep.join(additionalPaths)
    
    options = ['--no-tk', '--with-pthread', '--prefix', '%s' % q.dirs.baseDir]

    # Run the configure script with the appropriate options
    args = ['./configure']
    args.extend(options)

    # Can't use q.system.process because several environment variables needed to be set on the environment
    configureProcess = subprocess.Popen(args, stdout=sys.stdout, cwd=extractedLocation, env=buildEnv)
    configureProcess.wait()

    # First copy the customised Makefile into the extracted folder
    makeFile = q.system.fs.joinPaths(qpackage.getPathMetadata(), 'tasklets','Makefile')
    q.system.fs.copyFile(makeFile, q.system.fs.joinPaths(extractedLocation,'config'))
    
    # make world
    args = ['make', 'world']
    makeWorldProcess = subprocess.Popen(args, stdout=sys.stdout, cwd=extractedLocation, env=buildEnv)
    makeWorldProcess.wait()

    # make opt
    args = ['make', 'opt']
    makeOptProcess = subprocess.Popen(args, stdout=sys.stdout, cwd=extractedLocation, env=buildEnv)
    makeOptProcess.wait()

    # make opt.opt
    args = ['make', 'opt.opt']
    makeOptOptProcess = subprocess.Popen(args, stdout=sys.stdout, cwd=extractedLocation, env=buildEnv)
    makeOptOptProcess.wait()

    # make -C tools objinfo dumpobj dumpapprox
    args = ['make', '-C', 'tools', 'objinfo', 'dumpobj', 'dumpapprox']
    makeToolsProcess = subprocess.Popen(args, stdout=sys.stdout, cwd=extractedLocation, env=buildEnv)
    makeToolsProcess.wait()

    # make install
    args = ['make', 'install', 'PREFIX=%s' % localInstallDir, 'LIBDIR=%s' % q.system.fs.joinPaths(localInstallDir,'lib','ocaml')]
    makeInstallProcess = subprocess.Popen(args, stdout=sys.stdout, cwd=extractedLocation, env=buildEnv)
    makeInstallProcess.wait()
[[/code]]