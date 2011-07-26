from enumerations import *
import pymodel as model
from acl import acl

class customer(model.RootObjectModel):

    #@doc name of customer
    name = model.String(thrift_id=1)

    #@doc optional description of customer
    description = model.String(thrift_id=2)

    #@doc address of the contact
    address = model.String(thrift_id=3)

    #@doc city where the contact resides
    city = model.String(thrift_id=4)

    #@doc country where the contact is located
    country = model.String(thrift_id=5)

    #@doc status
    status = model.Enumeration(customerstatustype,thrift_id=6)

    #@doc link to a resourcegroup, if used all machines which belong to this customer can only be deployed on backplanes & devices as defined in resourcegroup
    resourcegroupguid = model.GUID(thrift_id=9)

    #@doc usergroups linked to this customer
    cloudusergroups = model.List(model.GUID(),thrift_id=10)

    #@doc mac range to this customer
    macrange = model.String(thrift_id=11)
    
    #@doc sso domain name for this customer
    ssodomainname = model.String(thrift_id=12)
    
    #@doc sso username for this customer
    ssousername = model.String(thrift_id=13)
    
    #@doc flags whether this customer is registered
    registered = model.Boolean(thrift_id=14)

    #@doc sso pwd for this customer
    ssouserpwd = model.String(thrift_id=15)
    
    #@doc retention policy of disks for this customer
    retentionpolicyguid = model.GUID(thrift_id=16)

    #@doc system
    system = model.Boolean(thrift_id=17)
    
    #@doc series of tags format
    tags = model.String(thrift_id=18)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=19)
