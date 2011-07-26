from enumerations import *
import pymodel as model
from acl import acl

# @doc class which provides the properties of a threshold
class racktivity(model.RootObjectModel):
    #@doc racktivity software version
    sw_version = model.String(thrift_id=1)
    #@doc snmp server
    smtp = model.String(thrift_id=2)
    #@doc smtp password
    smtppassword = model.String(thrift_id=3)
    #@doc smtp login
    smtplogin = model.String(thrift_id=4)
    #check for the status of the application, if configured or not.
    configured = model.Boolean(thrift_id=5)
    #@doc series of tags format
    tags = model.String(thrift_id=6)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=7)