__tags__ = 'pop3','create'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    import poplib
    import base64
    pop3guid = p.api.model.config.pop3.find(server="pop.gmail.com", login="analytics@incubaid.com")['result'][0]
    pop3 = p.api.model.config.pop3.getObject(pop3guid)
    mailbox = poplib.POP3_SSL(pop3.server)
    mailbox.user(pop3.login)
    mailbox.pass_(pop3.password)
    numMessages = len(mailbox.list()[1])
    for i in range(numMessages):
        for mail in mailbox.retr(i+1)[1]:
            print mail
            p.events.publish('pylabs.event.sampleapp.email', 'mail:%s'%base64.encodestring(mail))

def match(q, i, params, tags):
    import time
    return (params['taskletlastexecutiontime']  + 300 <= time.time())
