from cloud_api_client.Exceptions import CloudApiException

class capacityplanning:
    def __init__(self, proxy):
        self._proxy = proxy


    def listCapacityUnitTypes (self, jobguid = "", executionparams = {}):
        """
        
        Returns a list of possible capacity unit types.

        @execution_method = sync
        
        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        e.g. ["machine","sdsd-2323232-fsfd","machine_kds1",]
        the names of the filenames will be $destUncPath/$the3eArrayElement.rootobject.7z
            e.g. dss://login:passwd@backup_machinex/myroot/backups/rootobjects/10-10-2009/machine_kds1.rootobject.7z

        @return:                  Dictionary of array of capacity types.
        @rtype:                   dictionary
        @note:                    Example return value:
        @note:                    {'result': '["CU", "LV", "MU", "NBU", "NUIPPORTS", "NUM", "SUA", "SUP", "WV"]',
        @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                 In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_capacityplanning.listCapacityUnitTypes(jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



