# <License type="Qlayer BSD" version="2.0">
# 
# Copyright (c) 2005-2008, Qlayer NV.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# 
# * Neither the name Qlayer nor the names of other contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY QLAYER "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL QLAYER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# </License>
 
import os
import os.path
import sys
import time

def daemonize(stdout, stderr, chdir='/', umask=0):
    '''Daemonize a process using a double fork

    This method will fork the current process to create a daemon process.
    It will perform a double fork(2), chdir(2) to the given folder (or not
    chdir at all if the C{chdir} argument is C{None}), and set the new
    process umask(2) to the value of the C{umask} argument, or not reset
    it if this argument is -1.

    The stdout and stderr arguments can be used to output the output to the
    corresponding streams of the daemon process to files at the provided
    location. Make sure the parent folder of these files already exists. When
    set to None, all output will vanish.

    While forking, a setsid(2) call will be done to become session leader
    and detach from the controlling TTY.

    In the child process, all existing file descriptors will be closed,
    including stdin, stdout and stderr, which will be re-opened to
    /dev/null, unless a corresponding parameter is provided as an argument to
    this function.

    The method returns a tuple<bool, number>. If the first item is True,
    the current process is the daemonized process. If it is False,
    the current process is the process which called the C{daemonize}
    method, which can most likely be closed now. The second item is the
    PID of the current process.

    @attention: Make sure you know really well what fork(2) does before using this method

    @param stdout: Path to file to dump stdout output of daemon process to
    @type stdout: string
    @param stderr: Path to file to dump stderr output of daemon process to
    @type stderr: string
    @param chdir: Path to chdir(2) to after forking. Set to None to disable chdir'ing
    @type chdir: string or None
    @param umask: Umask to set after forking. Set to -1 not to set umask
    @type umask: number

    @returns: Daemon status and PID
    @rtype: tuple<bool, number>

    @raise RuntimeError: System does not support fork(2)
    '''
    if not hasattr(os, 'fork'):
        raise RuntimeError(
                'os.fork not found, daemon mode not supported on your system')

    pid = os.fork()
    if pid == 0:
        #First child
        #Become session leader...
        os.setsid()

        #Double fork
        pid = os.fork()
        if pid == 0:
            #Second child
            if umask >= 0:
                os.umask(umask)
            if chdir:
                os.chdir(chdir)
        else:
            #First child is useless now
            print 'CHILDPID=%d' % pid
            sys.exit()
    else:
        return False, os.getpid()

    #Close all FDs
    import resource
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if maxfd == resource.RLIM_INFINITY:
        maxfd = 1024

    sys.stdin.close()
    if not stdout:
        sys.stdout.close()
    if not stderr:
        sys.stderr.close()

    def close_safe(fd):
        try:
            os.close(fd)
        except OSError:
            pass

    close_safe(0)
    if not stdout:
        close_safe(1)
    if not stderr:
        close_safe(2)

    for fd in xrange(3, maxfd):
        close_safe(fd)

    #Open fd0 to /dev/null
    redirect = getattr(os, 'devnull', '/dev/null')
    os.open(redirect, os.O_RDWR)

    #dup to stdout and stderr
    if not stdout:
        os.dup2(0, 1)
    else:
        fd = os.open(stdout, os.O_CREAT | os.O_WRONLY)
        os.dup2(fd, 1)
        close_safe(fd)
    if not stderr:
        os.dup2(0, 2)
    else:
        fd = os.open(stderr, os.O_CREAT | os.O_WRONLY)
        os.dup2(fd, 2)
        close_safe(fd)

    return True, os.getpid()

def main():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-o', '--stdout', dest='stdout',
            help='file to redirect stdout output', metavar='FILE')
    parser.add_option('-e', '--stderr', dest='stderr',
            help='file to redirect stderr output', metavar='FILE')

    #Only parse until a '--' argument
    if not '--' in sys.argv:
        raise RuntimeError('No -- argument found')
    options, args = parser.parse_args(args=sys.argv[:sys.argv.index('--')])

    if not args:
        raise ValueError('No arguments provided')

    if options.stdout and not os.path.isdir(os.path.dirname(options.stdout)):
        raise ValueError('Folder of stdout file does not exist')
    if options.stderr and not os.path.isdir(os.path.dirname(options.stderr)):
        raise ValueError('Folder of stderr file does not exist')

    daemon, _ = daemonize(options.stdout, options.stderr)

    if not daemon:
        #Give first fork time to print daemon info
        time.sleep(0.2)
        return
    else:
        #We're the daemon now, execlp to replace ourself with the application
        #our consumer actually wants to run
        args = sys.argv[sys.argv.index('--') + 1:]
        os.execlp(args[0], *args)

if __name__ == '__main__':
    main()