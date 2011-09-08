TAB_RACKS_TITLE = 'Datacenter Rack Distribution'
TAB_INVESTMENTS_TITLE= 'Datacenter Investments'
TAB_SIZING_TITLE = 'Datacenter Sizing'
TAB_SALES_TITLE = 'Sales Configuration'

TAB_RACKS_COLLOCATION = '% Racks for Collocation: '
TAB_RACKS_STORAGE = '% Racks for Storage:  '
TAB_RACKS_CPU = '% Rack for CPU: '
TAB_INVESTMENTS_LEASE_BUILDING = 'Percentage Lease Building (%): '
TAB_INVESTMENTS_LEASE_INFRASTRUCTURE = 'Infrastructure Leasing (%): '
TAB_INVESTMENTS_LEASE_HW = 'Hardware Leasing (%): '
TAB_INVESTMENTS_INTEREST_RATE_BUILDING = 'Interest Rate Building (%): '
TAB_INVESTMENTS_INTEREST_RATE_DC = 'Interest Rate Datacenter HW (%): '
TAB_INVESTMENTS_LEASE_PERIOD_BUILDING = 'Lease Period Building (years): '
TAB_INVESTMENTS_LEASE_PERIOD_DC = 'Lease Period Datacenter HW (years): '
TAB_INVESTMENTS_TECHNOLOGY_UPFRONT = 'Technology Upfront (%): '
TAB_INVESTMENTS_PERIOD_TO_ACTIVE = 'Period before DC is Active (months): '
TAB_SIZING_SIZE = 'Datacenter Size (m2): '
TAB_SIZING_RACKSURFACE = 'Rack Surface (m2): '
TAB_SIZING_KWHOURCOST = 'Cost per kW/h (EUR): '
TAB_SIZING_PUE = 'Power Usage Effectivness: '
TAB_SALES_COLLOCATION = 'Rack Rental (kEur/month): '
TAB_SALES_CPU = 'CPU Rack Rental (kEur/month): '
TAB_SALES_STORAGE = 'Storage Rack Rental (kEur/month): '
TAB_SALES_BANDWIDTH = 'Cost Bandwidth (Eur/Mbps/month): '

TAB_RACKS_COLLOCATION_HELPTEXT = 'Percentage Collocated Racks in Datacenter'
TAB_RACKS_STORAGE_HELPTEXT = 'Percentage Storage Racks in Datacenter'
TAB_RACKS_CPU_HELPTEXT = 'Percentage CPU Racks in Datacenter'
TAB_INVESTMENTS_LEASE_BUILDING_HELPTEXT = 'Percentage of investment for leasing the building'
TAB_INVESTMENTS_LEASE_INFRASTRUCTURE_HELPTEXT = 'Percentage of investment for leasing the DC infrastructure'
TAB_INVESTMENTS_LEASE_HW_HELPTEXT = 'Percentage of investment for leasing the DC hardware'
TAB_INVESTMENTS_INTEREST_RATE_BUILDING_HELPTEXT = 'Interest rate for leasing the building'
TAB_INVESTMENTS_INTEREST_RATE_DC_HELPTEXT = 'Interest rate for leasing the DC infrastructure'
TAB_INVESTMENTS_LEASE_PERIOD_BUILDING_HELPTEXT = 'Lease period of the building (years)'
TAB_INVESTMENTS_LEASE_PERIOD_DC_HELPTEXT = 'Lease period of the DC infrastructure (years)'
TAB_INVESTMENTS_TECHNOLOGY_UPFRONT_HELPTEXT = 'Percentage of installed technology'
TAB_INVESTMENTS_PERIOD_TO_ACTIVE_HELPTEXT = 'Months before the DC is active'
TAB_SIZING_SIZE_HELPTEXT = 'Total datacenter surface in square meters, minimum 500'
TAB_SIZING_RACKSURFACE_HELPTEXT = 'Surface of a rack in square meters'
TAB_SIZING_KWHOURCOST_HELPTEXT = 'Cost per used kW/h in EUR'
TAB_SIZING_PUE_HELPTEXT = 'Ratio of effective power needed for theoretical power needed'
TAB_SALES_COLLOCATION_HELPTEXT = 'Rental price per rack in kEur/month'
TAB_SALES_CPU_HELPTEXT = 'Rental price per CPU rack in kEur/month'
TAB_SALES_STORAGE_HELPTEXT = 'Rental price per Storage rack in kEur/month'
TAB_SALES_BANDWIDTH_HELPTEXT = 'Cost for bandwidth in Euro per Mbps per month'

MSGBOX_CREATE_CONFIRMATION = "Set this investment scheme?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "Investment Scheme Creation"

MSGBOX_INVESTMENT_SCHEME_CREATE_FAILED = "Failed to create this Investment Scheme! Please contact your system administrator!"
MSGBOX_INVESTMENT_SCHEME_CREATE_FAILED_TITLE = "Investment Scheme Creation Failed"


def callCloudAPI(api, ** args):
   
    result = api.action.datacenter.businessparams.create(** args)['result']    
    return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_racks  = form.addTab('racks' , TAB_RACKS_TITLE)
    tab_investments  = form.addTab('investments' , TAB_INVESTMENTS_TITLE)
    tab_sizing = form.addTab('sizing' , TAB_SIZING_TITLE)
    tab_sales  = form.addTab('sales' , TAB_SALES_TITLE)
    
    #########################
    # Rack distribution tab #
    #########################
    
    tab_racks.addInteger(name='collocation', text = TAB_RACKS_COLLOCATION, helpText = TAB_RACKS_COLLOCATION_HELPTEXT)
    tab_racks.addInteger(name='storage', text = TAB_RACKS_STORAGE, helpText = TAB_RACKS_STORAGE_HELPTEXT)
    tab_racks.addInteger(name='cpu', text = TAB_RACKS_CPU, helpText = TAB_RACKS_CPU_HELPTEXT)
    
    ###################
    # Investments tab #
    ###################
    
    tab_investments.addInteger(name='leasebuilding', text = TAB_INVESTMENTS_LEASE_BUILDING, helpText = TAB_INVESTMENTS_LEASE_BUILDING_HELPTEXT)
    tab_investments.addInteger(name='leaseinfrastructure', text = TAB_INVESTMENTS_LEASE_INFRASTRUCTURE, helpText = TAB_INVESTMENTS_LEASE_INFRASTRUCTURE_HELPTEXT)
    tab_investments.addInteger(name='leasehw', text = TAB_INVESTMENTS_LEASE_HW, helpText = TAB_INVESTMENTS_LEASE_HW_HELPTEXT)	
    tab_investments.addText(name='interestbuilding', text = TAB_INVESTMENTS_INTEREST_RATE_BUILDING, helpText = TAB_INVESTMENTS_INTEREST_RATE_BUILDING_HELPTEXT)		
    tab_investments.addText(name='interestdatacenter', text = TAB_INVESTMENTS_INTEREST_RATE_DC, helpText = TAB_INVESTMENTS_INTEREST_RATE_DC_HELPTEXT)	
    tab_investments.addInteger(name='leaseperiodbuilding', text = TAB_INVESTMENTS_LEASE_PERIOD_BUILDING, value = 20, helpText = TAB_INVESTMENTS_LEASE_PERIOD_BUILDING_HELPTEXT)
    tab_investments.addInteger(name='leaseperioddatacenter', text = TAB_INVESTMENTS_LEASE_PERIOD_DC, value = 3, helpText = TAB_INVESTMENTS_LEASE_PERIOD_BUILDING_HELPTEXT)
    tab_investments.addInteger(name='technology', text = TAB_INVESTMENTS_TECHNOLOGY_UPFRONT, helpText = TAB_INVESTMENTS_TECHNOLOGY_UPFRONT_HELPTEXT)
    tab_investments.addInteger(name='installperiod', text = TAB_INVESTMENTS_PERIOD_TO_ACTIVE, helpText = TAB_INVESTMENTS_PERIOD_TO_ACTIVE_HELPTEXT)
    
    #########################
    # Datacenter Sizing tab #
    #########################
    
    tab_sizing.addInteger(name='size', text = TAB_SIZING_SIZE, helpText = TAB_SIZING_SIZE_HELPTEXT)
    tab_sizing.addInteger(name='racksurface', text = TAB_SIZING_RACKSURFACE, value=3, helpText = TAB_SIZING_RACKSURFACE_HELPTEXT)
    tab_sizing.addText(name='kwhourcost', text = TAB_SIZING_KWHOURCOST, value=0.05, helpText = TAB_SIZING_KWHOURCOST_HELPTEXT)
    tab_sizing.addText(name='pue', text = TAB_SIZING_PUE, value=1.4, helpText = TAB_SIZING_PUE_HELPTEXT)
    
    
    ##########################
    # Datacenter Selling tab #
    ##########################
    
    tab_sales.addText(name='salescollocation', text = TAB_SALES_COLLOCATION, value = 0.8, helpText = TAB_SALES_COLLOCATION_HELPTEXT)
    tab_sales.addText(name='salescpu', text = TAB_SALES_CPU, value = 6, helpText = TAB_SALES_CPU_HELPTEXT)
    tab_sales.addText(name='salesstorage', text = TAB_SALES_STORAGE, value = 14, helpText = TAB_SALES_STORAGE_HELPTEXT)
    tab_sales.addText(name='salesbandwidth', text = TAB_SALES_BANDWIDTH, helpText = TAB_SALES_BANDWIDTH_HELPTEXT)
    
    
    #########################
    # Confirmation overview #
    #########################
    
    form.loadForm(q.gui.dialog.askForm(form))
    tab_racks = form.tabs['racks']
    tab_investments = form.tabs['investments']
    tab_sizing = form.tabs['sizing']
    tab_sales = form.tabs['sales']
    
    message = "&nbsp;&nbsp;Confirmation required<br><br>Do you want to use the provided business parameters?"
    answer = q.gui.dialog.showMessageBox(message = message, 
                                         title = 'Confirmation',
                                         msgboxButtons = 'OKCancel',
					 msgboxIcon = 'Question',
                  			 defaultButton = 'OK')

    cloudAPIArgs = dict()

    cloudAPIArgs['collocation'] = tab_racks.elements['collocation'].value
    cloudAPIArgs['storage'] = tab_racks.elements['storage'].value
    cloudAPIArgs['cpu'] = tab_racks.elements['cpu'].value

    cloudAPIArgs['leasebuilding'] = tab_investments.elements['leasebuilding'].value
    cloudAPIArgs['leaseinfrastructure'] = tab_investments.elements['leaseinfrastructure'].value
    cloudAPIArgs['leasehw'] = tab_investments.elements['leasehw'].value
    cloudAPIArgs['interestbuilding'] = float(tab_investments.elements['interestbuilding'].value)
    cloudAPIArgs['interestdatacenter'] = float(tab_investments.elements['interestdatacenter'].value)
    cloudAPIArgs['leaseperiodbuilding'] = tab_investments.elements['leaseperiodbuilding'].value
    cloudAPIArgs['leaseperioddatacenter'] = tab_investments.elements['leaseperioddatacenter'].value
    cloudAPIArgs['technology'] = tab_investments.elements['technology'].value
    cloudAPIArgs['installperiod'] = tab_investments.elements['installperiod'].value

    cloudAPIArgs['size'] = tab_sizing.elements['size'].value
    cloudAPIArgs['racksurface'] = tab_sizing.elements['racksurface'].value
    cloudAPIArgs['kwhourcost'] = float(tab_sizing.elements['kwhourcost'].value)
    cloudAPIArgs['pue'] = float(tab_sizing.elements['pue'].value)

    cloudAPIArgs['salescollocation'] = float(tab_sales.elements['salescollocation'].value)
    cloudAPIArgs['salescpu'] = float(tab_sales.elements['salescpu'].value)
    cloudAPIArgs['salesstorage'] = float(tab_sales.elements['salesstorage'].value)
    cloudAPIArgs['salesbandwidth'] = float(tab_sales.elements['salesbandwidth'].value)

    result = callCloudAPI(p.api, ** cloudAPIArgs)	
    params['result'] = result
    
def match(q, i, p, params, tags):
	return True

