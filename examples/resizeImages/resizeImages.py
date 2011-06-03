
from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="resizeimages"

q.application.start()

#DIR
sourcedir="/mnt/disk2/backup"
#"/mnt/nas/fotos/2011"
destdir="/mnt/disk2/fotosSmall"
#destdir="/media/6535-3766/DCIM"

dedupe={}
dirfiles={} 
      
def getNr(file):
    def findMaxNrPlus1(array):
        highest=1
        for item in array:
            if item>highest:
                highest=item
        return highest+1
    name=q.system.fs.getBaseName(file).lower()
    dirname=q.system.fs.getDirName(file,1)
    if name.find("_")<>-1:
        name=name.split("_")[-1]
    clean="".join([char for char in name if char in "0123456789"])
    if clean=="":
        clean=1
    nr=int(clean)+0
    if not dirfiles.has_key(dirname):
        dirfiles[dirname]={}
    if dirfiles[dirname].has_key(nr):
        q.console.echo("file %s does already exist in dir %s with same nr" % (name,dirname))
        nr=findMaxNrPlus1(dirfiles[dirname])
    dirfiles[dirname][nr]=file
    return nr
        

def checkPath(file):
    filename=q.system.fs.getBaseName(file).lower()
    return filename.split(".")[-1]=="jpg" and filename.find("____")==-1 and not q.system.fs.isLink(file)

def warning(msg):
    q.console.echo( "%s" % msg)
    q.system.fs.writeFile(q.system.fs.joinPaths(destdir,"WARNING.TXT"),msg+"\n",True)

def duplicate(msg):
    q.console.echo( "Duplicate %s" % msg)
    q.system.fs.writeFile(q.system.fs.joinPaths(destdir,"DUPLICATE.TXT"),msg+"\n",True)

#thumbnails  
def removeThumbnails():
    dirs=q.system.fs.listDirsInDir(sourcedir,True)
    for dir in dirs:
        dir=dir.replace("\\","/")
        if dir[-1]<>"/":
            dir=dir+"/"
        if q.system.fs.getDirName(dir,True).lower().strip().find("thumbnail")<>-1:
            warning("Delete dir %s" % dir)
            q.system.fs.removeDirTree(dir)

def renameFiles():    
    def getDirName(file):
        dirname=q.system.fs.getDirName(file,True).replace(" ","").replace("-","_").replace("__","_").replace("__","_").replace("__","_")
        found=False
        for t in range(1970,2050):
            if dirname.find("%s"%t)<>-1:
                found=1
        if found==False:            
            dirname2=q.system.fs.getDirName(file,False,1).replace(" ","").replace("__","_").replace("__","_").replace("__","_")
            dirname="%s-%s"%(dirname2,dirname)
            for t in range(1970,2050):
                if dirname.find("%s"%t)<>-1:
                    found=2
            if found==False:
                dirname3=q.system.fs.getDirName(file,False,2).replace(" ","").replace("__","_").replace("__","_").replace("__","_")
                dirname="%s-%s"%(dirname3,dirname)
                for t in range(1970,2050):
                    if dirname.find("%s"%t)<>-1:
                        found=3
                if found==False:
                    dirname4=q.system.fs.getDirName(file,False,3).replace(" ","").replace("__","_").replace("__","_").replace("__","_")
                    dirname="%s-%s"%(dirname4,dirname)
                    for t in range(1970,2050):
                        if dirname.find("%s"%t)<>-1:
                            found=4
                    if found==False:
                        raise RuntimeError("Could not find applicable dir name for file %s" % file)                    
        return dirname,found
            
    files=q.system.fs.listFilesInDir(sourcedir,True)        
    for file in files:
        #check file
        print file
        if not q.system.fs.isLink(file) and q.system.fs.fileSize(file)<1000:
            warning("File is empty:: %s" % file)
            q.system.fs.remove(file)
        else:
            if checkPath(file) and q.system.fs.fileSize(file)>10000:
                filenr=getNr(file)
                dirname,found=getDirName(file)
                if found <3:
                    destpath=q.system.fs.joinPaths(q.system.fs.getDirName(file),"%s__%s.jpg" %(dirname,filenr))
                else:
                    dirpath=q.system.fs.getDirName(file)
                    for t in range(found-2):
                        dirpath=q.system.fs.getParent(dirpath)
                    #print "multiple depths"
                    destpath=q.system.fs.joinPaths(dirpath,"%s__%s.jpg" %(dirname,filenr))                    
                print " rename to: %s" % destpath
                q.system.fs.renameFile(file,destpath)

def dedupeFiles():    
    files=q.system.fs.listFilesInDir(sourcedir,True)        
    for file in files:
        if not q.system.fs.isLink(file):
            md5=q.system.fs.md5sum(file)
            if not dedupe.has_key(md5):
                dedupe[md5]=file
            else:
                duplicate("%s :: %s" % (file,dedupe[md5]))
                if len(dedupe[md5])<len(file):
                    source=dedupe[md5]
                    dest=file
                else:
                    dest=dedupe[md5]
                    source=file                    
                print "DEDUPE"               
                q.system.fs.remove(dest)  
                q.system.fs.symlink(source, dest)
        
def convertImages():        
    files=q.system.fs.listFilesInDir(sourcedir,True)        
    for file in files:        
        filename=q.system.fs.getBaseName(file).lower()
        dirname=q.system.fs.getDirName(file,1)
        #year=q.system.fs.getDirName(file,2)
        dest="%s/%s/%s" % (destdir,dirname,filename)        
        if filename.split(".")[-1]=="jpg" and filename.find("__")<>-1 and not q.system.fs.isLink(file):
            cmd="convert %s -resize 1024x1024 -quality 80 %s" %(file,dest)
            q.system.fs.createDir(q.system.fs.getDirName(dest))            
            #ipshell()
            print cmd
            q.system.process.execute(cmd)

#renameFiles()
convertImages()

q.application.stop()