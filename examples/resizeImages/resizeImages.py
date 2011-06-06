
from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="resizeimages"

q.application.start()

#DIR
##sourcedir="/mnt/disk2/backup"
##sourcedir="/mnt/disk2/test"
sourcedir="/mnt/disk2/backup2/sorted"
##"/mnt/nas/fotos/2011"
destdir="/mnt/disk2/fotosSmall"
##destdir="/media/6535-3766/DCIM"

dedupe={}
dirfiles={} 
maindirs={}
      
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
    return filename.split(".")[-1]=="jpg" and filename.find("__")==-1 and not q.system.fs.isLink(file)

def warning(msg):
    q.console.echo( "%s" % msg)
    q.system.fs.writeFile(q.system.fs.joinPaths(destdir,"WARNING.TXT"),msg+"\n",True)

def error(msg):
    q.console.echo( "%s" % msg)
    q.system.fs.writeFile(q.system.fs.joinPaths(destdir,"ERROR.TXT"),msg+"\n",True)


def duplicate(msg):
    q.console.echo( "Duplicate %s" % msg)
    q.system.fs.writeFile(q.system.fs.joinPaths(destdir,"DUPLICATE.TXT"),msg+"\n",True)

def testYearstrInDirname(dirname):
    found=False
    for t in range(1970,2050):
            if dirname.find("%s"%t)<>-1:
                found=True
    return found

def findMainDirs():
    yearstrings=[]
    for t in range(1970,2050):
        yearstrings.append(str(t))
    years=q.system.fs.listDirsInDir(sourcedir,False)
    for year in years:
        yearname=q.system.fs.getDirName(year+"/",True).strip()
        if yearname not in yearstrings:
            raise RuntimeError("cannot find main dir, should be a year nr like 2001, %s" % year)
        months=q.system.fs.listDirsInDir(year,False)
        for month in months:
            monthname=q.system.fs.getDirName(month+"/",True).strip()
            if testYearstrInDirname(monthname):
                maindirs[month]=[yearname,monthname]

def testFileInMainDir(file):
    if not q.system.fs.isLink(file) and q.system.fs.fileSize(file)>1000:
        found=False
        file=file.replace("\\","/").strip()
        for key in maindirs.keys():   
            if file.find(key)==0:
                found=True
                if key[-1]<>"/":
                    key=key+"/"
                remainder=file.replace(key,"")
                while remainder[-1]=="/":
                    remainder=remainder[:-1]
                if remainder.find("/")<>-1:
                    #is still subdir
                    found=False
        return found    
    return False

def getMainDir(file):
    if not q.system.fs.isLink(file) and q.system.fs.isFile(file) and q.system.fs.fileSize(file)>1000:
        found=False
        file=q.system.fs.getDirName(file,False)
        file=file.replace("\\","/").strip()
        maindir=""
        remainder=""
        for key in maindirs.keys():   
            if file.find(key)==0:                
                if key[-1]<>"/":
                    key=key+"/"
                found=key
                remainder=file.replace(key,"")
                if len(remainder)>0:
                    while remainder[-1]=="/":
                        remainder=remainder[:-1]
                remainder=remainder.replace("/","-")
                maindir=q.system.fs.getDirName(key,True)
                remainder=remainder.lower().strip()
        return maindir,remainder
    return "",""

#thumbnails  
def removeThumbnails():
    dirs=q.system.fs.listDirsInDir(sourcedir,True)
    for dir in dirs:
        dir=dir.replace("\\","/")
        if dir[-1]<>"/":
            dir=dir+"/"
        if q.system.fs.getDirName(dir,True).lower().strip().find("thumbnail")<>-1:
            warning("Delete dir:: %s" % dir)
            q.system.fs.removeDirTree(dir)

def getDirName(file):    
    maindir,remainder=getMainDir(file)
    remainder=remainder.replace(" ","").replace("-","_").replace("__","_").replace("__","_").replace("__","_")
    if maindir=="":
        found=False
    else:
        found=True
    return maindir,remainder,found

def renameFiles():                
    print "rename files"
    files=q.system.fs.listFilesInDir(sourcedir,True)        
    for file in files:
        #check file
        #print file
        if not q.system.fs.isLink(file) and q.system.fs.fileSize(file)<1000:
            warning("File is empty:: %s" % file)
            q.system.fs.remove(file)
        else:
            if checkPath(file) and q.system.fs.fileSize(file)>10000:
                filenr=getNr(file)
                maindir,remainder,found=getDirName(file)
                if found:
                    destpath=q.system.fs.joinPaths(q.system.fs.getDirName(file),"%s__%s__%s.jpg" %(maindir,remainder,filenr))
                #else:
                #    dirpath=q.system.fs.getDirName(file)
                #    for t in range(found-2):
                #        dirpath=q.system.fs.getParent(dirpath)
                #    #print "multiple depths"
                #    destpath=q.system.fs.joinPaths(dirpath,"%s__%s.jpg" %(dirname,filenr))                    
                    print file
                    print " rename to: %s" % destpath
                    q.system.fs.renameFile(file,destpath)

def dedupeFiles():    
    print 'Dedupe files'
    def dedupeFile(file,inmaindir=False):
        md5=q.system.fs.md5sum(file)
        if not dedupe.has_key(md5):
            dedupe[md5]=[file,inmaindir]
        else:
            duplicate("%s :: %s" % (file,dedupe[md5][0]))
            if (inmaindir and dedupe[md5][1]) or (inmaindir==False and dedupe[md5][1]==False):
                #both files are in maindir or both are not in maindir
                print "both files are in maindir or not in maindir"
                if len(dedupe[md5])<len(file):
                    source=dedupe[md5][0]
                    dest=file
                else:
                    dest=dedupe[md5][0]
                    source=file                   
            else:
                if inmaindir:
                    print "file which we are testing is in maindir, other one not"
                    dest=dedupe[md5][0]
                    source=file
                else:
                    source=dedupe[md5][0]
                    dest=file  
                ipshell()
            print "DEDUPE source:%s link:%s"%(source,dest)               
            if dest<>source:
                q.system.fs.remove(dest)  
                q.system.fs.symlink(source, dest)

    def listFiles(filter):
        files=q.system.fs.listFilesInDir(sourcedir,True,filter)        
        for file in files:
            if testFileInMainDir(file):
                dedupeFile(file,True)
        for file in files:            
            if not q.system.fs.isLink(file):
                dedupeFile(file)
    listFiles("*.jpg")
        
def convertImages(conversionstr="-resize 1024x1024 -quality 80"):        
    files=q.system.fs.listFilesInDir(sourcedir,True)        
    for file in files:        
        filename=filename=q.system.fs.getBaseName(file).lower()
        if filename.split(".")[-1]=="jpg" and filename.find("__")<>-1 and not q.system.fs.isLink(file):
            maindir,remainder=getMainDir(file)
            if maindir<>"":                
                dest="%s/%s/%s" % (destdir,maindir,filename)    
                cmd="convert '%s' %s %s" %(file,conversionstr,dest)
                q.system.fs.createDir(q.system.fs.getDirName(dest))            
                #ipshell()
                print cmd
                try:
                    q.system.process.execute(cmd)
                except:
                    error("INVALID JPG FILE:: %s" % file)
            else:
                warning("Image not converted, could not find maindir::%s"%file)
        

##MAIN PROG, ENABLE MODULES YOU WANT
#q.system.fs.convertFileDirnamesUnicodeToAscii(sourcedir)
#q.system.fs.convertFileDirnamesSpaceToUnderscore(sourcedir)
findMainDirs()  #ALWAYS NEEDED!!!
#removeThumbnails()
#renameFiles()
dedupeFiles()
convertImages("-resize 1600x1600 -quality 90")

q.application.stop()