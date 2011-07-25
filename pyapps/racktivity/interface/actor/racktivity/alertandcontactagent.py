class AlertAndContactAgent():
        
        
    def sendMail(self, smtpserver, subject ,body="", sender ="", to ="",smtplogin ="", smtppassword="", request="", jobguid="", executionparams=dict() ):
        """
        Sends a mail using smtp 
    
        @param smtpserver:        Smtp server for sending the email 
        @type smtpserver:         string
    
        @param subject:           Subject for the email 
        @type subject:            string
    
        @param body:              Body of the mail
        @type body:               string
            
        @param sender:            The email address of the sender
        @type sender:             string
            
        @param to:                The email address of the receiver
        @type to:                 string
    
        @param smtplogin:         Login for the smtp server
        @type smtplogin:          string
            
        @param smtppassword:      Password for the smtp server
        @type smtppassword:       string
    
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid
    
        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
    
        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        """
  