__tags__ = 'schedule'
__author__ = 'incubaid'

def _extractMessage(q, mail_elements):
    """
    A helper method to retrieve the message text from an e-mail message
    """
    # TODO - MNOUR: We should provide another way of parsing data out of a mail message which is not dependent on finding boundaries.
    #               I know it but I need to finish the full cycle first and then I will get back to it.
    import os
    if not mail_elements:
        q.errorconditionhandler.raiseError('Ivalid value %s.' %mail_elements)

    boundry_headers = list()
    for header in mail_elements:
        if header.find('Content-Type') != -1 and header.find('boundary') != -1:
            boundry_headers.append(header)
    
    if not boundry_headers:
        q.errorconditionhandler.raiseError('Could not find boundary to extract and read e-mail message.')

    if len(boundry_headers) > 1:
        q.errorconditionhanlder.raiseError('Found more than one boundary header.')

    boundary = boundry_headers[0].split('=')[1]
    start = mail_elements.index('--%s' %boundary) + 3
    end = mail_elements.index('--%s' %boundary, start + 1)
    if start == -1 or end == -1:
        q.errorconditionhandler.raiseError('Could not find boundary to extract and read e-mail message.')
    
    massage_lines = list()
    for index in range(start, end):
        if mail_elements[index]:
            massage_lines.append(mail_elements[index])

    return os.linesep.join(massage_lines)

def main(q, i, p, params, tags):
    import base64
    import os
    import poplib
    view = '%s_view_%s_list' %('mail', 'pop3')
    filter = p.api.config.mail.pop3.getFilterObject()
    filter.add(view, 'server', 'pop.gmail.com')
    filter.add(view, 'login', 'analytics@incubaid.com')
    pop3guids = p.api.config.mail.pop3.find(filter)
    if len(pop3guids) > 1:
        q.errorconditionhandler.raiseError("Found more than one POP3 mailbox configured for '%s' on '%s' server." %('nourm@incubaid.com', 'pop.gmail.com'))

    if len(pop3guids) < 1:
        q.errorconditionhandler.raiseError('Could not find configured POP3 mailbox.')

    pop3guid = pop3guids[0]
    pop3 = p.api.config.mail.pop3.get(pop3guid)
    mailbox = poplib.POP3_SSL(pop3.server)
    mailbox.user(pop3.login)
    mailbox.pass_(pop3.password)
    numMessages = len(mailbox.list()[1])
    q.logger.log('[DEBUG] - Found %d message(s).' %numMessages, level=3)
    for i in range(numMessages):
        mail_elements = mailbox.retr(i+1)[1]
        mail = _extractMessage(q, mail_elements)
        q.logger.log('[DEBUG] - Extracted message nr#%d: %s' %((i+1), mail), level=3)
        # TODO - MNOUR: Why we should tigh events to its source. The event processor should be able to receive events
        #               from different sources. I would change that later.
        p.events.publish('pylabs.event.sampleapp.email', 'mail:%s' %base64.encodestring(mail).replace(os.linesep, ''))
        # Mark message for deletion, otherwise it would be read on next execution.
        mailbox.dele(i+1)

    # Signoff: commit changes, unlock mailbox, drop connection
    mailbox.quit()

def match(q, i, params, tags):
    import time
    # if the last execution time +300 sec less than current time (which the current time is after the last execution time with 5 min passed since last execution ) we run the tasklet , 
    #this ensure minimum 5 min between every run of tasklet       
    return (params['taskletlastexecutiontime']  + 300 <= time.time())
    #return True
