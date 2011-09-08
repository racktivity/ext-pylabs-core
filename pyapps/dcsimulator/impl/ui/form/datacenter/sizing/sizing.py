TAB_GENERAL_TITLE = 'Datacenter Sizing'
TAB_GENERAL_SIZE = 'Datacenter Size (m2): '
TAB_GENERAL_RACKSURFACE = 'Rack Surface (m2): '
TAB_GENERAL_KWHOURCOST = 'Cost per kW/h (EUR): '
TAB_GENERAL_PUE = 'Power Usage Effectivness: '
TAB_GENERAL_SIZE_HELPTEXT = 'Total datacenter surface in square meters, minimum 500'
TAB_GENERAL_RACKSURFACE_HELPTEXT = 'Surface of a rack in square meters'
TAB_GENERAL_KWHOURCOST_HELPTEXT = 'Cost per used kW/h in EUR'
TAB_GENERAL_PUE_HELPTEXT = 'Ratio of effective power needed for theoretical power needed'

MSGBOX_CREATE_CONFIRMATION = "Set this datacenter sizing scheme?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Datacenter Sizing Confirmation"

MSGBOX_PROD_DISTRIBUTION_FAILED = "Failed to set this Datacenter Sizing Scheme!"
MSGBOX_PROD_DISTRIBUTION_FAILED_TITLE = "Datacenter Sizing Failed!"


def callCloudAPI(api, size, racksurface, kwhourcost, pue):
	result = api.action.datacenter.sizingscheme.create(size, racksurface, kwhourcost, pue)['result']    
	return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    ###########################
    # General information tab #
    ###########################

    tab_general.addInteger(name='size', text = TAB_GENERAL_SIZE, helpText = TAB_GENERAL_SIZE_HELPTEXT)
    tab_general.addInteger(name='racksurface', text = TAB_GENERAL_RACKSURFACE, value=3, helpText = TAB_GENERAL_RACKSURFACE_HELPTEXT)
    tab_general.addText(name='kwhourcost', text = TAB_GENERAL_KWHOURCOST, value=0.05, helpText = TAB_GENERAL_KWHOURCOST_HELPTEXT)
    tab_general.addText(name='pue', text = TAB_GENERAL_PUE, value=1.4, helpText = TAB_GENERAL_PUE_HELPTEXT)
    
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
                          tab_general.elements['size'].value,
                          tab_general.elements['racksurface'].value,
                          float(tab_general.elements['kwhourcost'].value),
                          float(tab_general.elements['pue'].value)
                          )

    params['result'] = result
    
def match(q, i, p, params, tags):
	return True

