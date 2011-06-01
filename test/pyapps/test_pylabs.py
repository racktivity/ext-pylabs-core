#!/usr/bin/python

from pylabs.InitBase import q, p

print "Test API generate"
p.core.codemanagement.api.generate('sampleapp')
print "Test Initialize"
p.application.install('sampleapp')
print "Test Start"
p.application.start('sampleapp')
print "Test API object retrieval"
appserver_api = p.application.getAPI('sampleapp', context=q.enumerators.AppContext.APPSERVER)
print "Test OSIS"
c = appserver_api.model.crm.customer.new()
c.name = "Joske Vermeulen"
c.email = "joske@incubaid.com"
c.login = "joske"
c.password = "rooter"
appserver_api.model.crm.customer.save(c)
print "Try to retrieve the object from the db"
cc = appserver_api.model.crm.customer.get(c.guid)
assert c == cc
f = appserver_api.model.crm.customer.getFilterObject()
f.add("crm_view_customer_list", "name", "Joske Vermeulen")
print "Try to find the object"
guids = appserver_api.model.crm.customer.find(f)
assert len(guids) == 1
assert c.guid in guids

print "Try to restart the application"
p.application.stop('sampleapp')
p.application.start('sampleapp')

print "Try if we can install more than once"
p.application.install('sampleapp')

print "Testing NGinx"
import urllib2
site = urllib2.urlopen("http://localhost/sampleapp/")

print "Testing Actions"
api = p.application.getAPI('sampleapp')
jefke_name = "Jefke"
# Moehahaha
jefke_login = "jefketest'; DROP TABLE students;<script>alert(\"This should not show up\");</script>"
jefke_dict = api.action.crm.customer.create(jefke_name, jefke_login, "rooter", "jefke.test@incubaid.com")
jefke_guid = jefke_dict['result']

print "Testing Lead"
coldcall = "COLDCALL"
partner = "PARTNER"
existingbusiness = "EXISTINGBUSINESS"
prospecting = "PROSPECTING"
test_lead_create_dict = api.action.crm.lead.create("Test Lead", "leadcode", jefke_guid, coldcall, existingbusiness, prospecting, 0.5, 42)
test_lead_guid = test_lead_create_dict['result']

result_dict = api.action.crm.lead.update(test_lead_guid, name="Super Test Lead", source=partner)
assert 'result' in result_dict
assert result_dict['result'] == True

find_result_dict = api.action.crm.lead.find(name="Super Test Lead", source=partner, probability=42)
find_result = find_result_dict['result']
assert len(find_result) == 1
assert find_result[0] == test_lead_guid

test_lead = api.action.crm.lead.getObject(test_lead_guid)
assert test_lead.name == "Super Test Lead"
assert test_lead.code == "leadcode"
assert test_lead.customerguid == jefke_guid
assert test_lead.source == q.enumerators.leadsource.PARTNER
assert test_lead.type == q.enumerators.leadtype.EXISTINGBUSINESS
assert test_lead.status == q.enumerators.leadstatus.PROSPECTING
assert test_lead.amount == 0.5
assert test_lead.probability == 42

lead_list_dict = api.action.crm.lead.list()
lead_list = lead_list_dict['result']
print "Lead list:"
print lead_list
assert len(lead_list) == 1
assert lead_list[0]['name'] == "Super Test Lead"
assert lead_list[0]['guid'] == test_lead_guid

lead_list_types_dict = api.action.crm.lead.listTypes()
lead_list_types = lead_list_types_dict['result']
assert set(lead_list_types) == set(['EXISTINGBUSINESS', 'NEWBUSINESS'])

lead_list_sources_dict = api.action.crm.lead.listSources()
lead_list_sources = lead_list_sources_dict['result']
assert set(lead_list_sources) == set(['PARTNER', 'COLDCALL', 'TRADESHOW'])

lead_list_statuses_dict = api.action.crm.lead.listStatuses()
lead_list_statuses = lead_list_statuses_dict['result']
assert set(lead_list_statuses) == set(['CLOSEDLOST', 'CLOSEDWON', 'PROSPECTING', 'VALUEPROPOSITION'])

result_dict = api.action.crm.lead.delete(test_lead_guid)
assert 'result' in result_dict
assert result_dict['result'] is True

print "Test pop3 events:"
import base64
import time

mailmessage = '''
'!@***LEAD***@!'
name=mytestlead
code=somecode
'''
mail_tag = base64.encodestring(mailmessage).replace("\n", "")
tagstring = q.base.tags.getTagString(set(["label1", "label2"]), {"mail": mail_tag})
p.events.publish("pylabs.event.sampleapp.email", tagstring)
print "Wait for the event result"
def event_result_happened_once():
    result_dict = api.action.crm.lead.find(name='mytestlead', code='somecode')
    lead_guids = result_dict['result']
    l = len(lead_guids)
    if l == 0:
        return False
    elif l == 1:
        return True
    else:
        raise AssertionError("More than one matching lead was found")

for time_left in range(9, 0, -1):
    if event_result_happened_once():
        break
    print "Event did not happen yet, will wait for %d more second(s)" % time_left
    time.sleep(1)

assert event_result_happened_once()

print "Check if Jefke's page exists"
page_name = "customer_detail_" + jefke_guid
page_guids_dict = api.action.ui.page.find(name=page_name)
page_guids = page_guids_dict['result']
assert len(page_guids) == 1, "Expected to find 1 page guid, but found %d" % len(page_guids)

print "Check if we can access it"
site = urllib2.urlopen("http://localhost/sampleapp/#/crm/" + page_name)
content = site.read()
