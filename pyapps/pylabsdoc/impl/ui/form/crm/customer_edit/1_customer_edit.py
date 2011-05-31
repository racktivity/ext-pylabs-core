TAB_GENERAL_TITLE = 'General'
TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_EMAIL = 'Email: '
TAB_GENERAL_LOGIN = 'Login: '
TAB_GENERAL_PASSWORD = 'Password: '
TAB_GENERAL_ADDRESS = 'Address: '
TAB_GENERAL_VAT = 'VAT: '
TAB_GENERAL_NAME_HELPTEXT = 'Please provide the customer\'s name'
TAB_GENERAL_EMAIL_HELPTEXT = 'Please provide the customer\'s email'
TAB_GENERAL_LOGIN_HELPTEXT = 'Please provide the customer\'s login'
TAB_GENERAL_PASSWORD_HELPTEXT = 'Please provide the customer\'s password'
TAB_GENERAL_ADDRESS_HELPTEXT = 'Please provide the customer\'s address'
TAB_GENERAL_VAT_HELPTEXT = 'Please provide the customer\'s VAT'


MSGBOX_CREATE_CONFIRMATION = "Update this customer?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Customer update"

MSGBOX_CUSTOMER_CREATE_FAILED = "Failed to update this customer! Please contact your system administrator!"
MSGBOX_CUSTOMER_CREATE_FAILED_TITLE = "Customer update failed"


def callCloudAPI(api, customerguid, name, email, login, password, address, vat):
    result = api.action.crm.customer.update(customerguid, name, login, password, email, address, vat)['result']    
    return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    ###########################
    # General information tab #
    ###########################
    customerguid = params['customerguid']
    customer = p.api.action.crm.customer.getObject(customerguid, executionparams={'description': 'Retrieving customer information'})
    
    tab_general.addText(name='name', text = TAB_GENERAL_NAME, value=customer.name, helpText = TAB_GENERAL_NAME_HELPTEXT)
    tab_general.addText(name='email', text = TAB_GENERAL_EMAIL, value=customer.email, validator="^\w+(\.\w+)*@\w+(\.\w+)+$", helpText = TAB_GENERAL_EMAIL_HELPTEXT)
    tab_general.addText(name='login', text = TAB_GENERAL_LOGIN, value=customer.login, validator="^[a-zA-Z0-9]{1,16}$", helpText = TAB_GENERAL_LOGIN_HELPTEXT)	
    tab_general.addPassword(name='password', text = TAB_GENERAL_PASSWORD, value=customer.password, helpText = TAB_GENERAL_PASSWORD_HELPTEXT)		
    tab_general.addText(name='address', text = TAB_GENERAL_ADDRESS, value=customer.address, helpText = TAB_GENERAL_ADDRESS_HELPTEXT)	
    tab_general.addText(name='vat', text = TAB_GENERAL_VAT, value=customer.vat, helpText = TAB_GENERAL_VAT_HELPTEXT)

    #answer = q.gui.dialog.showMessageBox(message=MSGBOX_CREATE_CONFIRMATION,
	#                                     title=MSGBOX_CREATE_CONFIRMATION_TITLE,
	#                                     msgboxButtons='OKCancel',
	#                                     msgboxIcon='Question',
	#                                     defaultButton='OK')
    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']

    result = callCloudAPI(p.api,
                          customerguid,
						  tab_general.elements['name'].value,
						  tab_general.elements['email'].value,
						  tab_general.elements['login'].value,
						  tab_general.elements['password'].value,
						  tab_general.elements['address'].value,
						  tab_general.elements['vat'].value)
    params['result'] = result

def match(q, i, p, params, tags):
	return True
