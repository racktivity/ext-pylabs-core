TAB_GENERAL_TITLE = 'Sales Configuration'
TAB_GENERAL_COLLOCATION = 'Rack Rental (kEur/month): '
TAB_GENERAL_CPU = 'CPU Rack Rental (kEur/month): '
TAB_GENERAL_STORAGE = 'Storage Rack Rental (kEur/month): '
TAB_GENERAL_BANDWIDTH = 'Cost Bandwidth (Eur/Mbps/month): '
TAB_GENERAL_COLLOCATION_HELPTEXT = 'Rental price per rack in kEur/month'
TAB_GENERAL_CPU_HELPTEXT = 'Rental price per CPU rack in kEur/month'
TAB_GENERAL_STORAGE_HELPTEXT = 'Rental price per Storage rack in kEur/month'
TAB_GENERAL_BANDWIDTH_HELPTEXT = 'Cost for bandwidth in Euro per Mbps per month'

MSGBOX_CREATE_CONFIRMATION = "Set this datacenter sales scheme?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Datacenter Sales Confirmation"

MSGBOX_PROD_DISTRIBUTION_FAILED = "Failed to set this Datacenter Sales Scheme!"
MSGBOX_PROD_DISTRIBUTION_FAILED_TITLE = "Datacenter Sales Failed!"


def callCloudAPI(api, collocation, cpu, storage, bandwidth):
	result = api.action.datacenter.salesscheme.create(collocation, cpu, storage, bandwidth)['result']    
	return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    ###########################
    # General information tab #
    ###########################

    tab_general.addText(name='collocation', text = TAB_GENERAL_COLLOCATION, value = 0.8, helpText = TAB_GENERAL_COLLOCATION_HELPTEXT)
    tab_general.addText(name='cpu', text = TAB_GENERAL_CPU, value = 6, helpText = TAB_GENERAL_CPU_HELPTEXT)
    tab_general.addText(name='storage', text = TAB_GENERAL_STORAGE, value = 14, helpText = TAB_GENERAL_STORAGE_HELPTEXT)
    tab_general.addText(name='bandwidth', text = TAB_GENERAL_BANDWIDTH, helpText = TAB_GENERAL_BANDWIDTH_HELPTEXT)
    
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
                          float(tab_general.elements['collocation'].value),
                          float(tab_general.elements['cpu'].value),
                          float(tab_general.elements['storage'].value),
                          float(tab_general.elements['bandwidth'].value)
                          )

    params['result'] = result
    
def match(q, i, p, params, tags):
	return True

