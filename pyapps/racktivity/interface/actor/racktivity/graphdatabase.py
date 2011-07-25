class GraphDatabase():
    
    def createStore(self, storeid, jobguid="", executionparams=dict()):
      """
      Create a store which can be used for creating graphs 

      @param storeid: name for the store
      @type storeid: string
    
      @param jobguid:          Guid of the job
      @type jobguid:           guid

      @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
      @type executionparams:   dictionary

      @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
      @rtype:                  dictionary
       """
    
    def createStores(self, storeids, jobguid="", executionparams=dict()):
        """
        Create a bunch of stores using the provided store ids data

        
        @param storeids: list of store names
        @type storeids: list
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
      
        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        """
        
    def destroyStore(self, storeid, jobguid="", executionparams=dict()):
        """
        Delete a store

        
        @param storeid: name for the store
        @type storeid: string
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
      """
      
    def destroyStores(self, storeids, jobguid="", executionparams=dict()):
        """
        Delete stores

        @param storeids: list of store names
        @type storeids: list
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        """
        
    def  getRanges(self, storeids, aggregationtype, resolution, start, stop, jobguid="", executionparams=dict()):
        """
        Fetch data from a stores based on aggragationtype and resolution

        @param storeids: list of store names
        @type storeids: list
        
        @param aggregationtype: aggregation type used (AVG, MAX, MIN)
        @type aggregationtype: string
        
        @param resolution: resolution,needed to select the correct archive
        @type resolution: integer
        
        @param start: start time of the ranges of data
        @type start: string
        
        @param stop: stop time of the range of data
        @type stop: string
    
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True and the a dict with the data as result and jobguid: {'result': {returncode:True, data:{db1:[(t1, v1), (t2, v2)]}}}
, 'jobguid': guid}
        @rtype:                  dictionary
        """
        
    def  getLatest(self, storeid, jobguid="", executionparams=dict()):
        """
        Get the latest value from store

        @param storeid: name for the store
        @type storeid: string
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True and the a dict with the data as result and jobguid: {'result': {returncode:True, value: <value>}}
        @rtype:                  dictionary
        """

    def  getLatests(self, stores, jobguid="", executionparams=dict()):
        """
        Get the latest value from stores

        @param stores: A dict in the form {valuekey: storeid, ...}
        @type databases: dict
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True and the a dict with the data as result and jobguid: {'result': {returncode: True, values:{'valuekey1': <value>, 'valuekey2': <value>}}}
        @rtype:                  dictionary
        """
        
    def  getAverageValues(self, stores, jobguid="", executionparams=dict()):
        """
        Get the historical average values from rrd databases based on aggregation type

        @param stores: A dict in the form {valuekey: storeid, ...}
        @type databases: dict
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True and the a dict with the data as result and jobguid: {'result': {returncode: True, values:{'valuekey1': (lastday, lastweek, lastmonth, lastyear)}}}
        @rtype:                  dictionary
        """