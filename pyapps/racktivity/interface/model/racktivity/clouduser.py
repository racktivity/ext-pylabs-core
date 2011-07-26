from enumerations import *
import pymodel as model
from acl import acl

# @doc a clouduser is someone who can access the datacenter infrastructure, security is given on this level, a clouduser can be a customer, the term customer is no longer used
class clouduser(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc first name of the clouduser account
    firstname = model.String(thrift_id=2)

    #@doc last name of the clouduser account
    lastname = model.String(thrift_id=3)

    #@doc optional description of clouduser
    description = model.String(thrift_id=4)

    #@doc login
    login = model.String(thrift_id=5)

    #@doc password
    password = model.String(thrift_id=6)

    #@doc address of the contact
    address = model.String(thrift_id=7)

    #@doc city where the contact resides
    city = model.String(thrift_id=8)

    #@doc country where the contact is located
    country = model.String(thrift_id=9)

    #@doc status of the clouduser
    status = model.Enumeration(clouduserstatustype,thrift_id=10)

    #@doc certificate of the clouduser account for secure acces into datacenter
    certificate = model.String(thrift_id=11)

    #@doc checksum of the certificate for verifying the validity of the certificate
    certificatechecksum = model.String(thrift_id=12)

    #@doc private key
    privatekey = model.String(thrift_id=13)

    #@doc e-mail address of the clouduser (can be comma separated)
    email = model.String(thrift_id=14)

    #@doc mobile phone
    phonemobile = model.String(thrift_id=15)

    #@doc landline phone
    phonelandline = model.String(thrift_id=16)

    #@doc system
    system = model.Boolean(thrift_id=17)

    #@doc series of tags format
    tags = model.String(thrift_id=18)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=19)
