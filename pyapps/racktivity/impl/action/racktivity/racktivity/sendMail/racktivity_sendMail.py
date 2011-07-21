__author__ = 'racktivity'

def main(q, i, p, params, tags):
    filterObject = p.api.model.racktivity.racktivity.getFilterObject()
    racktivityconfig_guid = p.api.model.racktivity.racktivity.find(filterObject)
    if not racktivityconfig_guid:
        q.logger.log("No racktivity config object found", 1)
        return 

    racktivityconfig = p.api.model.racktivity.racktivity.get(racktivityconfig_guid[0])
    if not racktivityconfig.smtp:
        q.logger.log("The SMTP server is not configured", 1)
        return

    to = params['to']
    if not to:
        #get the admin email
        filterObject = p.api.model.racktivity.clouduser.getFilterObject()
        filterObject.add("racktivity_view_clouduser_list", 'login', 'admin')
        result = p.api.model.racktivity.clouduser.find(filterObject)
        if not result:
            q.logger.log("Can't find the admin user object")
            return
        admin = p.api.model.racktivity.clouduser.get(result[0])
        to = admin.email

    q.actions.actor.alertandcontactagent.sendMail(smtpserver=racktivityconfig.smtp, subject=params['subject'], body=params['body'],
                                 sender=params['sender'], to=to, smtplogin=racktivityconfig.smtplogin, smtppassword=racktivityconfig.smtppassword,
                                 jobguid = params['jobguid'],
                                 executionparams = {'description' : 'Sending email to admin'})

def match(q, i, params, tags):
    return True