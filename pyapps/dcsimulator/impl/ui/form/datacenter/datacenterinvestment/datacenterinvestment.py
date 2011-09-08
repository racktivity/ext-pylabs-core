TAB_GENERAL_TITLE = 'Datacenter Investments'
TAB_GENERAL_LEASE_BUILDING = 'Percentage Lease Building (%): '
TAB_GENERAL_LEASE_INFRASTRUCTURE = 'Infrastructure Leasing (%): '
TAB_GENERAL_LEASE_HW = 'Hardware Leasing (%): '
TAB_GENERAL_INTEREST_RATE_BUILDING = 'Interest Rate Building (%): '
TAB_GENERAL_INTEREST_RATE_DC = 'Interest Rate Datacenter HW (%): '
TAB_GENERAL_LEASE_PERIOD_BUILDING = 'Lease Period Building (years): '
TAB_GENERAL_LEASE_PERIOD_DC = 'Lease Period Datacenter HW (years): '
TAB_GENERAL_TECHNOLOGY_UPFRONT = 'Technology Upfront (%): '
TAB_GENERAL_PERIOD_TO_ACTIVE = 'Period before DC is Active (months): '
TAB_GENERAL_LEASE_BUILDING_HELPTEXT = 'Percentage of investment for leasing the building'
TAB_GENERAL_LEASE_INFRASTRUCTURE_HELPTEXT = 'Percentage of investment for leasing the DC infrastructure'
TAB_GENERAL_LEASE_HW_HELPTEXT = 'Percentage of investment for leasing the DC hardware'
TAB_GENERAL_INTEREST_RATE_BUILDING_HELPTEXT = 'Interest rate for leasing the building'
TAB_GENERAL_INTEREST_RATE_DC_HELPTEXT = 'Interest rate for leasing the DC infrastructure'
TAB_GENERAL_LEASE_PERIOD_BUILDING_HELPTEXT = 'Lease period of the building (years)'
TAB_GENERAL_LEASE_PERIOD_DC_HELPTEXT = 'Lease period of the DC infrastructure (years)'
TAB_GENERAL_TECHNOLOGY_UPFRONT_HELPTEXT = 'Percentage of installed technology'
TAB_GENERAL_PERIOD_TO_ACTIVE_HELPTEXT = 'Months before the DC is active'


MSGBOX_CREATE_CONFIRMATION = "Set this investment scheme?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Investment Scheme Creation"

MSGBOX_INVESTMENT_SCHEME_CREATE_FAILED = "Failed to create this Investment Scheme! Please contact your system administrator!"
MSGBOX_INVESTMENT_SCHEME_CREATE_FAILED_TITLE = "Investment Scheme Creation Failed"


def callCloudAPI(api, leasebuilding, leaseinfrastructure, leasehw, interestbuilding, interestdatacenter, leaseperiodbuilding, leaseperioddatacenter, technology, installperiod):
        result = api.action.datacenter.investmentscheme.create(leasebuilding, leaseinfrastructure, leasehw, interestbuilding, interestdatacenter, leaseperiodbuilding, leaseperioddatacenter, technology, installperiod)['result']
	return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    ###########################
    # General information tab #
    ###########################

    tab_general.addInteger(name='leasebuilding', text = TAB_GENERAL_LEASE_BUILDING, helpText = TAB_GENERAL_LEASE_BUILDING_HELPTEXT)
    tab_general.addInteger(name='leaseinfrastructure', text = TAB_GENERAL_LEASE_INFRASTRUCTURE, helpText = TAB_GENERAL_LEASE_INFRASTRUCTURE_HELPTEXT)
    tab_general.addInteger(name='leasehw', text = TAB_GENERAL_LEASE_HW, helpText = TAB_GENERAL_LEASE_HW_HELPTEXT)	
    tab_general.addText(name='interestbuilding', text = TAB_GENERAL_INTEREST_RATE_BUILDING, helpText = TAB_GENERAL_INTEREST_RATE_BUILDING_HELPTEXT)		
    tab_general.addText(name='interestdatacenter', text = TAB_GENERAL_INTEREST_RATE_DC, helpText = TAB_GENERAL_INTEREST_RATE_DC_HELPTEXT)	
    tab_general.addInteger(name='leaseperiodbuilding', text = TAB_GENERAL_LEASE_PERIOD_BUILDING, value = 20, helpText = TAB_GENERAL_LEASE_PERIOD_BUILDING_HELPTEXT)
    tab_general.addInteger(name='leaseperioddatacenter', text = TAB_GENERAL_LEASE_PERIOD_DC, value = 3, helpText = TAB_GENERAL_LEASE_PERIOD_BUILDING_HELPTEXT)
    tab_general.addInteger(name='technology', text = TAB_GENERAL_TECHNOLOGY_UPFRONT, helpText = TAB_GENERAL_TECHNOLOGY_UPFRONT_HELPTEXT)
    tab_general.addInteger(name='installperiod', text = TAB_GENERAL_PERIOD_TO_ACTIVE, helpText = TAB_GENERAL_PERIOD_TO_ACTIVE_HELPTEXT)
    
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
                          tab_general.elements['leasebuilding'].value,
                          tab_general.elements['leaseinfrastructure'].value,
                          tab_general.elements['leasehw'].value,
                          float(tab_general.elements['interestbuilding'].value),
                          float(tab_general.elements['interestdatacenter'].value),
                          tab_general.elements['leaseperiodbuilding'].value,
                          tab_general.elements['leaseperioddatacenter'].value,
                          tab_general.elements['technology'].value,
                          tab_general.elements['installperiod'].value)

    params['result'] = result
    
def match(q, i, p, params, tags):
	return True

