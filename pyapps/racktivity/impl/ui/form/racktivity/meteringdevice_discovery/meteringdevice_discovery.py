__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_discovery'

from pylabs.pmtypes import IPv4Range, IPv4Address
import json

AUTODISCOVERY_POLICY = 'racktivity_autodiscovery'
TITLE = 'Create/Update Auto-discovery Policy'

def main(q, i, p, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    autodiscoverypolicyguids = cloudapi.policy.find(AUTODISCOVERY_POLICY)['result']['guidlist']
    autodiscoverypolicy = None
    interval = 15.0
    nr_workers = 1
    discardaddresses = 'yes'
    policyparams = dict()
    if autodiscoverypolicyguids:
        autodiscoverypolicyguid = autodiscoverypolicyguids[0]
    else:
        answer = q.gui.dialog.showMessageBox('The auto-discovery policy is not found, Do you want to create it?', \
                                             TITLE, msgboxButtons="YesNo", \
                                             msgboxIcon="Question", defaultButton="No")
        if answer == 'Yes':
            autodiscoverypolicyguid = cloudapi.policy.create(name = 'racktivity_autodiscovery', description = 'Policy to start the autodiscovery', \
                                                         interval = 15.0, rootobjecttype = 'meteringdevice', rootobjectaction = 'discovery', \
                                                         runbetween = '[("00:00", "24:00")]', runnotbetween = '[]', \
                                                         policyparams = '{"nr_workers":1, "discardaddresses":[]}')['result']['policyguid']
        else:
            return
        
    autodiscoverypolicy = cloudapi.policy.getObject(autodiscoverypolicyguid)
    
    if autodiscoverypolicy.policyparams:
        policyparams = json.loads(autodiscoverypolicy.policyparams)
        nr_workers = policyparams['nr_workers'] 
        interval = autodiscoverypolicy.interval
        discardaddresses = policyparams['discardaddresses']
            
    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Create/Update Auto-discovery Policy')
    tab.addInteger('nr_workers', 'Number of Workers', value=nr_workers, minValue=1)
    tab.addInteger('interval', 'Minutes between discoveries', value=interval, helpText='Enter the time in minutes between 2 discoveries', minValue=1)
    tab.addText('discardaddresses', 'IP address discard list', value=", ".join(discardaddresses), helpText="Enter the IP addresses to skip as ipaddress1, ipaddress2, ...")

    invalid = True
    while invalid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        ips = tab.elements['discardaddresses'].value
        invalid = False
        for ip in ips.split(","):
            ip = ip.strip()
            if ip and not q.system.net.validateIpAddress(ip):
                tab.elements['discardaddresses'].status = "error"
                tab.elements['discardaddresses'].message = "Invlid ip address list given"
                invalid = True
    
    tab = form.tabs['main']
    policyparams = {'nr_workers': int(tab.elements['nr_workers'].value),
                    'discardaddresses': filter(None, map(lambda s: s.strip(), tab.elements['discardaddresses'].value.split(",")))}
    
    policyparamsStr = json.dumps(policyparams)
    cloudapi.policy.updateModelProperties(autodiscoverypolicyguid, name = 'racktivity_autodiscovery', \
                                          policyparams=policyparamsStr, interval=float(tab.elements['interval'].value))
    q.gui.dialog.showMessageBox('Auto-discovery policy is being updated' , TITLE)

def main(q, i, p, params, tags):
    return True
