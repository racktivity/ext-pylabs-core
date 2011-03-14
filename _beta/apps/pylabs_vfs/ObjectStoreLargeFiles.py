   class ObjectStoreLargeFiles(object):
       #original code from http://stuff.mit.edu/iap/2009/fuse/examples/xmp.py

        def __init__(self, path, flags, *mode):
            #file is stored in /mnt/largefilestore/$first2lettersmd5Hash/$next2lettermd5Hash/$remaininglettersmd5Hash
            ## e.g. /mnt/largefilestore/aa/bb/ccddeeff
            #each file larger than 1 MB
            
            self.file = os.fdopen(os.open("." + path, flags, *mode), flag2mode(flags))
            self.fd = self.file.fileno()
            
            ##when opened for write or RW
            #when existing file, rename file to /mnt/largefilestore/$first2lettersmd5Hash/$next2lettermd5Hash/$remaininglettersmd5Hash_  #note the _ at end
            
            ##when opened for write or RW and file does only exist as /mnt/largefilestore/$first2lettersmd5Hash/$next2lettermd5Hash/$remaininglettersmd5Hash_  means that there is locking error
            ##this can happen for RO
        

        def read(self, length, offset):
            self.file.seek(offset)
            return self.file.read(length)

        def write(self, buf, offset):            
            #write to the file with _ at end
            self.file.seek(offset)
            self.file.write(buf)
            return len(buf)

        def release(self, flags):
            self.file.close()
            #rename back to name without _ at end

        def _fflush(self):
            if 'w' in self.file.mode or 'a' in self.file.mode:
                self.file.flush()

        def fsync(self, isfsyncfile):
            self._fflush()
            if isfsyncfile and hasattr(os, 'fdatasync'):
                os.fdatasync(self.fd)
            else:
                os.fsync(self.fd)

        def flush(self):
            self._fflush()
            # cf. xmp_flush() in fusexmp_fh.c
            os.close(os.dup(self.fd))

        def fgetattr(self):
            return os.fstat(self.fd)

        def ftruncate(self, len):
            self.file.truncate(len)

        def lock(self, cmd, owner, **kw):
            # The code here is much rather just a demonstration of the locking
            # API than something which actually was seen to be useful.

            # Advisory file locking is pretty messy in Unix, and the Python
            # interface to this doesn't make it better.
            # We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
            # way. The following implementation *might* work under Linux. 
            #
            # if cmd == fcntl.F_GETLK:
            #     import struct
            # 
            #     lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
            #                            kw['l_start'], kw['l_len'], kw['l_pid'])
            #     ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
            #     flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
            #     uld2 = struct.unpack('hhQQi', ld2)
            #     res = {}
            #     for i in xrange(len(uld2)):
            #          res[flockfields[i]] = uld2[i]
            #  
            #     return fuse.Flock(**res)

            # Convert fcntl-ish lock parameters to Python's weird
            # lockf(3)/flock(2) medley locking API...
            op = { fcntl.F_UNLCK : fcntl.LOCK_UN,
                   fcntl.F_RDLCK : fcntl.LOCK_SH,
                   fcntl.F_WRLCK : fcntl.LOCK_EX }[kw['l_type']]
            if cmd == fcntl.F_GETLK:
                return -EOPNOTSUPP
            elif cmd == fcntl.F_SETLK:
                if op != fcntl.LOCK_UN:
                    op |= fcntl.LOCK_NB
            elif cmd == fcntl.F_SETLKW:
                pass
            else:
                return -EINVAL

            fcntl.lockf(self.fd, op, kw['l_start'], kw['l_len'])

