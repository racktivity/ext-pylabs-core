class user:
    """
    Activity actions API
    """
    
    def create(self, name, password , groups, jobguid="", executionparams=dict()):
        """
        Create an activity
        
        @param name: name for the activity
        @type name: string
        
        @param description: description of the activity
        @type description: string
        
        @param location: location where the activity will be held
        @param location: string
        
        @param type: type of the activity
        @type type: string
        
        @param priority: priority of the activity
        @type priority: string
        
        @param status: status of the activity
        @type status: string
        
        @param customerguid: guid of the customer with whom the activity is held, if not available this is an empty string
        @type customerguid: guid
        
        @param leadguid: guid of the lead with whom the activity is held, if not available this is an empty string
        @type leadguid: guid
        
        @param starttime: start time of activity, in format 'DD/MM/YYYY hh-mm'
        @type starttime: string
        
        @param endtime: end time of activity, in format 'DD/MM/YYYY hh-mm'
        @type endtime: string
        
        @param jobguid: guid of the job if available, else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       dictionary with activity guid and jobguid {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
        
        @raise e:                      in case of an error, raise an exception
        """
        
    def delete(self, userguid, jobguid="", executionparams=dict()):
        """
        Delete activity, actually remove activity from database
        
        @param activityguid: guid of the activity
        @type activityguid: guid
        
        @param jobguid: guid of the job if available, else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       dictionary with result True and jobguid {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
        
        @raise e:                      in case of an error, raise an exception
        """
        
    def cancel(self, userguid, jobguid="", executionparams=dict()):
        """
        Cancel activity
        
        @param activityguid: guid of the activity
        @type activityguid: guid
        
        @param jobguid: guid of the job if available, else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       dictionary with result True and jobguid {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
        
        @raise e:                      in case of an error, raise an exception
        """
        
    def list(self, jobguid="", executionparams=dict()):
        """
        Get list of activities
        
        @execution_method = sync
        @security administrators
        
        @param jobguid: guid of the job if available, else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                      dictionary with array of activity info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary
        
        @note:     {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:      'result': [{ 'guid': '75416B07-9665-69D1-0874-BB6520DC1434',
        @note:                  'customerguid': '378dd50c-5491-11e0-97a0-f04da266f098'
        @note:                  'name': 'My Activity'
        @note:                  'description': 'This is a sample activity'
        @note:                  'type': 'MEETING'
        @note:                  'startdate': '06-06-2006'
        @note:                  'starttime': '14:00'
        @note:                  'enddate': '06-06-2006'
        @note:                  'endtime': '18:00'
        @note:                  'status': 'HELD'
        @note:                  'priority': 'MEDIUM'
        @note:                  'location': 'IT-Valley Lochristi'}]}
        
        @raise e:                      in case of an error, raise an exception
        """
        
    def find(self, userguid=None, name =None, password=None , groups=None, jobguid=None, executionparams=dict()):
        """
        Find activities by using find criteria
        
        @execution_method = sync
        @security administrators
        
        @param activityguid: guid of the activity
        @type activityguid: guid
        
        @param customerguid: guid of the customer with whom the activity is held, if not available this is an empty string
        @type customerguid: guid
        
        @param leadguid: guid of the lead with whom the activity is held, if not available this is an empty string
        @type leadguid: guid
        
        @param name: name for the activity
        @type name: string
        
        @param type: type of the activity
        @type type: string
        
        @param status: status of the activity
        @type status: string
        
        @param priority: priority of the activity
        @type priority: string
        
        @param jobguid: guid of the job if available, else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       A list of guids as result and jobguid: {'result': [], 'jobguid': guid}
        @rtype:                        list
        
        @note:                         Example return value:
        @note:                         {'result': '["7f1d44f8-5495-11e0-97a0-f04da266f098","8bea971c-5495-11e0-97a0-f04da266f098"]',
        @note:                          'jobguid':'95d14578-5495-11e0-97a0-f04da266f098'}
        
        @raise e:                      in case of an error, raise an exception
        """
        
    def getObject(self, userguid, jobguid="",executionparams=dict()):
        """
        Get activity object by using its guid
        
        @execution_method = sync
        
        @param activityguid: guid of the activity
        @type activityguid: guid
        
        @return:                    PyModel object
        @rtype:                     Object
        
        @warning:                   Only usable using the python client.
        """
    
    def update (self, userguid, name, password , groups, jobguid=None, executionparams={}):
        """
        Update an activity
        
        @param activityguid: guid for the activity
        @type activityguid: guid
        
        @param name: name for the activity
        @type name: string
        
        @param description: description of the activity
        @type description: string
        
        @param location: location where the activity will be held
        @param location: string
        
        @param type: type of the activity
        @type type: string
        
        @param priority: priority of the activity
        @type priority: string
        
        @param status: status of the activity
        @type status: string
        
        @param customerguid: guid of the customer with whom the activity is held, if not available this is an empty string
        @type customerguid: guid
        
        @param leadguid: guid of the lead with whom the activity is held, if not available this is an empty string
        @type leadguid: guid
        
        @param starttime: start time of activity, in format 'DD/MM/YYYY hh-mm'
        @type starttime: string
        
        @param endtime: end time of activity, in format 'DD/MM/YYYY hh-mm'
        @type endtime: string
        
        @param jobguid: guid of the job if available, else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       dictionary with activity guid and jobguid {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
        
        @raise e:                      in case of an error, raise an exception
        """
        
