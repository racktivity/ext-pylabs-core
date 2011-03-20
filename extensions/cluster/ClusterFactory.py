from pylabs import q,i
from pylabs.Shell import *
from Replicator import Replicator
from Cluster import Cluster

import string

class ClusterFactory():

    def __init__(self):
        #self._lastSuperadminPassword=""
        self.clusters={}
        self.replicator=Replicator()
        i.cluster=self
        config=q.config.getInifile("clusterconfig") 
        if len(config.getSections())==0:
            return
        for clustername in config.getSections():
            ipaddresses=str(config.getValue(clustername,"ip")).strip()
            domainname=str(config.getValue(clustername,"domain")).strip()
            masteripaddress=str(config.getValue(clustername,"master")).strip()
            superadminpassword=config.getValue(clustername,"rootpasswd").strip()
            cl=Cluster(clustername=clustername,domainname=domainname,ipaddresses=ipaddresses.split(","),superadminpassword=superadminpassword,masteripaddress=masteripaddress)
            self.clusters[clustername]=cl
    
    def get(self,clustername="",domainname=""):
        """
        return cluster for specified domain or shortname, 
        there needs to be a cluster defined already before otherwise no nodes will be found
        config file which stores this info is at $qbasedir/cfg/qconfig/clusterconfig.cfg
        only one of th 2 params is required
        """        
        if clustername=="" and domainname=="":
            clustername=q.console.askChoice(self.list(),"select cluster")
        if self.clusters.has_key(clustername):
            return self.clusters[clustername]
        for clustername in self.clusters.keys():
            cl=self.clusters[clustername]
            if cl.domainname==domainname:
                return cl
        raise RuntimeError("Could not find cluster with domainname %s" % domainname)
    
    def create(self,clustername="",domainname="",ipaddresses=[],superadminpassword="",superadminpasswords=[],masteripaddress=""):
        # TODO
        # q.console.echo("*** Ignore master for now, it's not yet implemented yet, just pick any node of the cluster.. ***")
        # q.console.echo("*** After specifying the information for a cluster, the information gets written to disk but is not used by the program, instead it tries to guess the information by probing the network (mostly wrong), in case of problems just restart the shell, your cluster will be there. .. ***")
        
        """
        domainname needs to be unique
        clustername is only a name which makes it easy for you to remember and used to store in config file
        """
        if superadminpasswords==[]:
            superadminpasswords=[superadminpassword]
        if clustername<>"":
            #fill in cluster configuration file with information already known
            ipaddresses2=string.join([str(ipaddr).strip() for ipaddr in ipaddresses],",")
            if clustername not in q.cluster.config.list():
                i.cluster.config.add(clustername,{'domain': domainname, 'ip': ipaddresses2, 'master': str(masteripaddress), 'rootpasswd': superadminpassword})
            else:
                i.cluster.config.configure(clustername,{'domain': domainname, 'ip': ipaddresses2, 'master': str(masteripaddress), 'rootpasswd': superadminpassword})
        if q.qshellconfig.interactive:
            if domainname=="" or ipaddresses==[] or superadminpassword=="":
                if clustername=="":
                    #import pdb
                    #pdb.set_trace()
                    # How do I get the IP adresses?
                    # Get the ip adresses and put them in ipaddresses
                    # so the constructor of Cluster does not use avahi, because its results or wrong!
                    clustername = q.gui.dialog.askString('Name for the cluster', 'myCluster')
                    i.cluster.config.add(itemname=clustername)
                else:
                    i.cluster.config.review(clustername)
                self.__init__()
                return self.clusters[clustername]
            
        else:
            if ipaddresses==[]:
                raise RuntimeError("Please specify ipaddresses of nodes you would like to add to cluster")
            if superadminpasswords==[]:
                raise RuntimeError("Please specify password(s) of nodes you would like to add to cluster")
            if masteripaddress=="":
                raise RuntimeError("Please specify ip address of node which is master of cluster")
            if domainname=="":
                raise RuntimeError("Please specify domainname for cluster")
            if clustername=="":
                raise RuntimeError("Please specify short name for cluster")
                
                    
        #at this point we know ipaddresses & possible superadminpasswords
        cl=Cluster(clustername=clustername,domainname=domainname,ipaddresses=ipaddresses,superadminpasswords=superadminpasswords\
                   ,superadminpassword=superadminpassword,masteripaddress=masteripaddress)
        self.clusters[clustername]=cl
        return cl
    
    def delete(self,clustername=""):
        """
        Delete a cluster with clustername from the configuration
        """
        if clustername=="":
            if q.qshellconfig.interactive:
                ask = True
                if len(self.clusters.keys()) == 1:
                    ask = q.gui.dialog.askYesNo('Are you sure you want to delete cluster %s'%q.cluster.get())
                if ask:
                    clustername = q.gui.dialog.askChoice('Select cluster to remove', self.clusters.keys())
                else:
                    return
            else:
                raise ValueError("In non-interactive mode please specify clustername to be removed")
        if clustername in self.clusters.keys():
            q.cluster.config.remove(clustername)
        else:
            raise ValueError("Cluster %s not found"%clustername)
        self.__init__()
        
    def listAvahiEnabledMachines(self):
        q.transaction.start("Investigate network, try to find potential nodes (using avahi).")            
        services=q.cmdtools.avahi.getServices()
        result=[]
        ipaddresses=[]
        for service in services.services:
            if service.address not in ipaddresses:
                result.append(service)
                ipaddresses.append(service.address)
        q.transaction.stop()        
        return result

    def list(self):
        """
        return list of clusternames
        """
        return self.clusters.keys()
            
    ##def _removeRedundantFiles(self):
        ##path="/opt/qbase3"
        ##q.logger.log("removeredundantfiles %s" % (path))
        ##files=q.system.fs.listFilesInDir(path,True,filter="*.pyc")
        ##files.extend(q.system.fs.listFilesInDir(path,True,filter="*.pyo")) #@todo remove other files
        ##for item in files:
            ##q.system.fs.removeFile(item) 
        ##q.system.fs.removeDirTree(q.system.fs.joinPaths(q.dirs.logDir))
        ##q.system.fs.removeDirTree(q.system.fs.joinPaths(q.dirs.tmpDir))
        ##q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.tmpDir))
        ##q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.logDir))
        ##q.system.fs.removeDirTree(q.system.fs.joinPaths(q.dirs.varDir,"qpackages"))
