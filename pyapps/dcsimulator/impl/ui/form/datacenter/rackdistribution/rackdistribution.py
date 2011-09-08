TAB_GENERAL_TITLE = 'Datacenter Rack Distribution'
TAB_GENERAL_COLLOCATION = 'Collocation (%): '
TAB_GENERAL_STORAGE = 'Storage (%):  '
TAB_GENERAL_CPU = 'CPU Racks (%): '
TAB_GENERAL_COLLOCATION_HELPTEXT = 'Percentage Collocated Racks in Datacenter'
TAB_GENERAL_STORAGE_HELPTEXT = 'Percentage Storage Racks in Datacenter'
TAB_GENERAL_CPU_HELPTEXT = 'Percentage CPU Racks in Datacenter'


MSGBOX_CREATE_CONFIRMATION = "Set this Rack Distribution scheme?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Datacenter Distribution Confirmation"

MSGBOX_PROD_DISTRIBUTION_FAILED = "Failed to set this Rack Distribution Scheme!"
MSGBOX_PROD_DISTRIBUTION_FAILED_TITLE = "Rack Distribution Failed!"


def callCloudAPI(api, collocation, storage, cpu):
	result = api.action.datacenter.distributionscheme.create(collocation, storage, cpu)['result']    
	return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    ###########################
    # General information tab #
    ###########################

    tab_general.addInteger(name='collocation', text = TAB_GENERAL_COLLOCATION, helpText = TAB_GENERAL_COLLOCATION_HELPTEXT)
    tab_general.addInteger(name='storage', text = TAB_GENERAL_STORAGE, helpText = TAB_GENERAL_STORAGE_HELPTEXT)
    tab_general.addInteger(name='cpu', text = TAB_GENERAL_CPU, helpText = TAB_GENERAL_CPU_HELPTEXT)	
    
    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    #q.gui.dialog.askForm(form)
    
    #answer = q.gui.dialog.showMessageBox(message=MSGBOX_CREATE_CONFIRMATION,
    #                                     title=MSGBOX_CREATE_CONFIRMATION_TITLE,
    #                                     msgboxButtons='OKCancel',
    #                                     msgboxIcon='Question',
    #                                     defaultButton='OK')

    #if answer == 'CANCEL':
    #    return

    result = callCloudAPI(p.api,
                          tab_general.elements['collocation'].value,
                          tab_general.elements['storage'].value,
                          tab_general.elements['cpu'].value
                          )

    params['result'] = result
    
def match(q, i, p, params, tags):
	return True

