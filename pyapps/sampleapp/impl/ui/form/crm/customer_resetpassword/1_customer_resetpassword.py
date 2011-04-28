import uuid
TAB_GENERAL_TITLE = 'General'
TAB_GENERAL_EMAIL = 'Email: '
TAB_GENERAL_LOGIN = 'Login: '
TAB_GENERAL_LOGIN_HELPTEXT = 'Please provide the customer\'s login'
TAB_GENERAL_EMAIL_HELPTEXT = 'Please provide the customer\'s email'
MSGBOX_CREATE_CONFIRMATION = "Reset password?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Reset customer password"

MSGBOX_CUSTOMER_CREATE_FAILED = "Failed to reset customer's password! Please contact your system administrator!"
MSGBOX_CUSTOMER_CREATE_FAILED_TITLE = "Customer password update failed"


def callCloudAPI(api, customerguid, password):
    result = api.action.crm.customer.resetPassword(customerguid,password= password)['result']    
    return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    ###########################
    # General information tab #
    ###########################
    customerguid = params['customerguid']
    customer = p.api.action.crm.customer.getObject(customerguid, executionparams={'description': 'Retrieving customer information'})

    tab_general.addText(name='login', text = TAB_GENERAL_LOGIN, validator=customer.login, helpText = TAB_GENERAL_LOGIN_HELPTEXT)
    tab_general.addText(name='email', text = TAB_GENERAL_EMAIL, validator=customer.email, helpText = TAB_GENERAL_EMAIL_HELPTEXT)
    
    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    newpasswordstr = str(uuid.uuid1()).replace('-','')
    newpassword = newpasswordstr[0:8]
    result = callCloudAPI(p.api,
                          customerguid, newpassword)
    params['result'] = result

def match(q, i, p, params, tags):
    return True
