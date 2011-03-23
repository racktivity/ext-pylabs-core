__tags__ = 'wizard','customer','create'
__author__ = 'incubaid'

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


MSGBOX_CREATE_CONFIRMATION = "Create this new customer?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Customer creation"

MSGBOX_CUSTOMER_CREATE_FAILED = "Failed to create this new customer! Please contact your system administrator!"
MSGBOX_CUSTOMER_CREATE_FAILED_TITLE = "Customer creation failed"


def callCloudAPI(api, name, email, login, password, address, vat):
	result = api.customer.crm.create(name, email, login, password, address, vat)['result']    
	return result


def main(q, i, p, params, tags):

	form = q.gui.form.createForm()
	tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    ###########################
    # General information tab #
    ###########################

	tab.addText(name='name', text = TAB_GENERAL_NAME, helpText = TAB_GENERAL_NAME_HELPTEXT)
	tab.addText(name='email', text = TAB_GENERAL_EMAIL, validator="^\w+(\.\w+)*@\w+(\.\w+)+$", helpText = TAB_GENERAL_EMAIL_HELPTEXT)
	tab.addText(name='login', text = TAB_GENERAL_LOGIN, validator="^[a-zA-Z0-9]{1,16}$", helpText = TAB_GENERAL_LOGIN_HELPTEXT)	
	tab.addPassword(name='password', text = TAB_GENERAL_PASSWORD, helpText = TAB_GENERAL_PASSWORD_HELPTEXT)		
	tab.addText(name='address', text = TAB_GENERAL_ADDRESS, helpText = TAB_GENERAL_ADDRESS_HELPTEXT)	
	tab.addText(name='vat', text = TAB_GENERAL_VAT, helpText = TAB_GENERAL_VAT_HELPTEXT)

	answer = q.gui.dialog.showMessageBox(message=MSGBOX_CREATE_CONFIRMATION,
                                         title=MSGBOX_CREATE_CONFIRMATION_TITLE,
                                         msgboxButtons='OKCancel',
                                         msgboxIcon='Question',
                                         defaultButton='OK')

	if answer == 'CANCEL':
		return

	result = callCloudAPI(p.api,
    					  tabgeneral.elements['name'].value,
    					  tabgeneral.elements['email'].value,
    					  tabgeneral.elements['login'].value,
    					  tabgeneral.elements['password'].value,
    					  tabgeneral.elements['address'].value,
    					  tabgeneral.elements['vat'].value)

def match(q, i, p, params, tags):
    return True
