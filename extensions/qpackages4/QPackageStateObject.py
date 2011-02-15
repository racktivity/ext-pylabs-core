from pylabs import q
from pylabs.Shell import *
        
class QPackageStateObject():
    
    def __init__(self,qpackageObject):
        key="%s_%s_%s" % (qpackageObject.domain,qpackageObject.name,qpackageObject.version)
        statefile=q.system.fs.joinPaths(q.dirs.cfgDir,"qpackages4","state",key)+".cfg"
        if not q.system.fs.exists(statefile):
            self._ini=q.tools.inifile.new(statefile)
            self._ini.addSection("main")
            self.lastinstalledbuildnr=-1
            self.lastdownloadedbuildnr=-1
            self.lastexpandedbuildnr=-1
            self.lastaction=""
            self.lasttag=""
            self.lastactiontime=0
            self.currentaction=""
            self.currenttag=""
            self.currentactiontime=0
            #self.state=q.enumerators.QPackageState4.OK
            self.retry=0 #nr of times we tried to repair last broken state
            self.prepared=0
            self.isPendingReconfiguration=0
            self._save()
        else:
            self._ini=q.tools.inifile.open(statefile)
            self.lastinstalledbuildnr=int(self._ini.getValue("main","lastinstalledbuildnr"))
            self.lastexpandedbuildnr=int(self._ini.getValue("main","lastexpandedbuildnr"))
            self.lastdownloadedbuildnr=int(self._ini.getValue("main","lastdownloadedbuildnr"))
            self.lastaction=self._ini.getValue("main","lastaction")
            self.lasttag=self._ini.getValue("main","lasttag")
            self.lastactiontime=int(self._ini.getValue("main","lastactiontime"))
            self.currentaction=self._ini.getValue("main","currentaction")
            self.currenttag=self._ini.getValue("main","currenttag")
            self.currentactiontime=self._ini.getValue("main","currentactiontime")

            #print 'Asking enum : ' + self._ini.getValue("main","state") + ' from ' + str(self._ini)
            #self.state=q.enumerators.QPackageState4.getByName(self._ini.getValue("main","state"))
            self.retry=int(self._ini.getValue("main","retry"))
            self.prepared=int(self._ini.getValue("main","prepared"))
            self.isPendingReconfiguration=int(self._ini.getValue("main","isPendingReconfiguration"))
             
    def _save(self):
        self._ini.setParam("main","lastinstalledbuildnr",self.lastinstalledbuildnr)
        self._ini.setParam("main","lastexpandedbuildnr",self.lastexpandedbuildnr)
        self._ini.setParam("main","lastdownloadedbuildnr",self.lastdownloadedbuildnr)
        self._ini.setParam("main","lastaction",self.lastaction)
        self._ini.setParam("main","lasttag",self.lasttag)
        self._ini.setParam("main","lastactiontime",self.lastactiontime)
        self._ini.setParam("main","currentaction",self.currentaction)
        self._ini.setParam("main","currenttag",self.currenttag)
        self._ini.setParam("main","currentactiontime",self.currentactiontime)
        #print "in QPackageStateObject save: " + str(self.state)
        #self._ini.setParam("main","state",self.state)
        self._ini.setParam("main","retry",self.retry)
        self._ini.setParam("main","prepared",self.prepared)
        self._ini.setParam("main","isPendingReconfiguration",self.isPendingReconfiguration)
        self._ini.write()
        
    def save(self):
        self._save()
        
    def setLastInstalledBuildNr(self, buildNr):
        """
        Sets the last buildnumber to the one given as parameter
        """
        self.lastinstalledbuildnr = buildNr
        self._save()
        
    def setLastExpandedBuildNr(self, buildNr):
        """
        Sets the last expanded build number to the one given as parameter
        """
        self.lastexpandedbuildnr = buildNr
        self._save()
        
    def setLastDownloadedBuildNr(self, buildNr):
        """
        Sets the last downloaded build number to the one given as parameter
        """
        self.lastdownloadedbuildnr = buildNr
        self._save()
        
    def setIsPendingReconfiguration(self, value):
        """
        Changes the qpackage's config file to see whether reconfiguration is required or not depending on the value given as parameter
        """
        value = str(value).lower()
        if value == '1' or value == 'true':
            value=1
        else:
            value=0
        self.isPendingReconfiguration = value
        self.save()

    def getIsPendingReconfiguration(self):
        """
        Returns true is the qpackage needs reconfiguration
        """
        return self.isPendingReconfiguration

    def setCurrentAction(self,tag,action):
        """
        @param tag  e.g. install
        @param action e.g. checkout when tag=codemgmt
        """        
        if self.currenttag<>"":
            self.lasttag=self.currenttag
        if self.currentaction<>"":
            self.lastaction=self.currentaction
        if self.currentactiontime<>0:
            self.lastactiontime=self.currentactiontime
        self.currentactiontime=q.base.time.getTimeEpoch()
        self.currentaction=action
        self.currenttag=tag
        self._save()
        
    def setCurrentActionIsDone(self):
        """
        current action is succesfully completed
        """
        self.setCurrentAction("","")
        self.state=q.enumerators.QPackageState4.OK
        self._save()

    def setPrepared(self, prepared):
        """
        Changes the qpackage config file to whether the package has been prepared or not depending on the parameter given
        """
        self.prepared=prepared
        self._save()
        
    def checkNoCurrentAction():
        """
        if no current action return True
        """
        if self.state==q.enumerators.QPackageState4.OK and self.currentaction=="":
            return True
        return False
    
    def __str__(self):
        string  = "lastinstalledbuildnr:"  + str(self.lastinstalledbuildnr)  + '\n'
        string += "lastdownloadedbuildnr:" + str(self.lastdownloadedbuildnr) + '\n'
        string += "lastexpandedbuildnr:"   + str(self.lastexpandedbuildnr)   + '\n'
        string += "lastaction:"            + str(self.lastaction)            + '\n'
        string += "lasttag:"               + str(self.lasttag)               + '\n'
        string += "lastactiontime:"        + str(self.lastactiontime)        + '\n'
        string += "currentaction:"         + str(self.currentaction)         + '\n'
        string += "currenttag:"            + str(self.currenttag)            + '\n'
        string += "currentactontime:"      + str(self.currentactiontime)     + '\n'
        string += "nrretry:"               + str(self.retry)                 + '\n'
        return string
        
    def __repr__(self):
        return self.__str__()