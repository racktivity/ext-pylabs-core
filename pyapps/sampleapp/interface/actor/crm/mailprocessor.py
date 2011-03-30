class mailprocessor:
    """
    Mail Processor actions API
    """
 
    def sendMail(self, sender, replyto, to, cc, bcc, subject, message, jobguid="", executionparams=None):
        """
        Create a mailprocessor

        @param sender:  sender address for the email
        @type sender: string

        @param replyto:  replyto address for the email
        @type replyto: string
 
        @param to:  to address for the email
        @type to: string

        @param cc:  cc address for the email
        @type cc: string

        @param bcc: bcc address for the email
        @type bcc: string

        @param subject: subject for the email
        @type subject: string

        @param message: message body for the email
        @type message: string
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """

