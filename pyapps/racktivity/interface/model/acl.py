from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model

class acl(model.RootObjectModel):
    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(), thrift_id=1)
