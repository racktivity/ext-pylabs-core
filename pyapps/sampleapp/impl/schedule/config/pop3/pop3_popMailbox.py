__tags__ = 'schedule'
__author__ = 'incubaid'

def _extractMessage(mail_elements):
    """
    A helper method to retrieve the message text from an e-mail message
    """
    if not mail_elements:
        q.errorconditionhandler.raiseError('Ivalid value %s.' %mail_elements)

    boundry_headers = [boundary_header for boundary_header in [header for header in mail_elements if header.find('Content-Type') != -1] if boundary_header.find('boundary') != -1]
    if not boundry_headers:
        q.errorconditionhandler.raiseError('Could not find boundary to extract and read e-mail message.')

    if len(boundry_headers) > 1:
        q.errorconditionhanlder.raiseError('Found more than one boundary header.')

    boundary = boundry_headers[0].split('=')[1]
    start = mail_elements.find('--%s' %boundary) + 3
    end = mail_elements.find('--%s' %boundary, satrt + 1)
    if satrt == -1 or end == -1:
        q.errorconditionhandler.raiseError('Could not find boundary to extract and read e-mail message.')

    return '\n'.join([mail_elements[index] for index in range(start, end) if mail_elements[index]])

def main(q, i, p, params, tags):
    import poplib
    import base64
    view = '%s_view_%s_list' %('mail', 'pop3')
    filter = p.api.config.mail.pop3.getFilterObject()
    filter.add(view, 'server', 'pop.gmail.com')
    filter.add(view, 'login', 'analytics@incubaid.com')
    pop3guids = p.api.config.mail.pop3.find(filter)
    if len(pop3guids) > 1:
        q.errorconditionhandler.raiseError("Found more than one POP3 mailbox configured for '%s' on '%s' server." %('nourm@incubaid.com', 'pop.gmail.com'))

    pop3guid = pop3guids[0]
    pop3 = p.api.config.mail.pop3.getObject(pop3guid)
    mailbox = poplib.POP3_SSL(pop3.server)
    mailbox.user(pop3.login)
    mailbox.pass_(pop3.password)
    numMessages = len(mailbox.list()[1])
    for i in range(numMessages):
        for mail_elements in mailbox.retr(i+1)[1]:
            mail = _extractMessage(mail_elements)
            q.logger.log(mail, level=3)
            p.events.publish('pylabs.event.sampleapp.email', 'mail:%s' %base64.encodestring(mail))

def match(q, i, params, tags):
    import time
    return (params['taskletlastexecutiontime']  + 300 >= time.time())
