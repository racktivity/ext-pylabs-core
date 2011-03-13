   class ObjectStoreSmallFiles(object):
       #original code from http://stuff.mit.edu/iap/2009/fuse/examples/xmp.py
       #this is for files < 1 MB
       #store immediately in kevalue store use q.db.getConnection(pathForFileStorSmallFiles)
       #when open for RW or W use locking implemented on keyvalue store
       #key = md5 of file in category filedata
       #locking key = $md5 but in category lock

        def __init__(self, path, flags, *mode):
            #file is stored in keyvaluestor
                        
            ##when opened for write or RW put lock, get file from filestor, keep in memory
            ##when opened for write or RW and file is locked -> error
        

        def read(self, length, offset):
            #get file from filestore or cache and read, cache in mem
            self.file.seek(offset)
            return self.file.read(length)

        def write(self, buf, offset):            
            #write to file in mem
            self.file.seek(offset)
            self.file.write(buf)
            return len(buf)

        def release(self, flags):
            #write file from mem back to keyvaluestor
            #remove lock

        def _fflush(self):
            if 'w' in self.file.mode or 'a' in self.file.mode:
                #write back to keyvalyestor

        def fsync(self, isfsyncfile):
            #write back to keyvalyestor

        def flush(self):
            #write back to keyvalyestor

        def fgetattr(self):

        def ftruncate(self, len):

        def lock(self, cmd, owner, **kw):
