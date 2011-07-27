import enterprise
import location
import clouduser
import cloudusergroup
import datacenter
import room
import rack
import device
import meteringdevice
import ipaddress
import cable
import backplane
import lan
import feed
import resourcegroup
import logicalview
import floor
import pod
import row
import policy

def cleanenv():
    from pylabs import i,q,p
    cloudapi = p.api.action.racktivity
    
    for location in cloudapi.location.find()['result']['guidlist']:
        try:
            cloudapi.location.delete(location)
        except:
            continue
    
    for datacenter in cloudapi.datacenter.find()['result']['guidlist']:
        try:
            cloudapi.datacenter.delete(datacenter)
        except:
            continue
    
    for floor in cloudapi.floor.find()['result']['guidlist']:
        try:
            cloudapi.floor.delete(floor)
        except:
            continue
    
    for room in cloudapi.room.find()['result']['guidlist']:
        try:
            cloudapi.room.delete(room)
        except:
            continue
    
    for pod in cloudapi.pod.find()['result']['guidlist']:
        try:
            cloudapi.pod.delete(pod)
        except:
            continue
        
    for row in cloudapi.row.find()['result']['guidlist']:
        try:
            cloudapi.row.delete(row)
        except:
            continue
        
    for rack in cloudapi.rack.find()['result']['guidlist']:
        try:
            cloudapi.rack.delete(rack)
        except:
            continue
    
    for meteringdevice in cloudapi.meteringdevice.find()['result']['guidlist']:
        try:
            cloudapi.meteringdevice.delete(meteringdevice)
        except:
            continue
    
    for device in cloudapi.device.find()['result']['guidlist']:
        try:
            cloudapi.device.delete(device)
        except:
            continue
    
    for policy in cloudapi.policy.find()['result']['guidlist']:
        try:
            cloudapi.policy.delete(policy)
        except:
            continue
    
    for resourcegroup in cloudapi.resourcegroup.find()['result']['guidlist']:
        try:
            cloudapi.resourcegroup.delete(resourcegroup)
        except:
            continue
        
    for ipaddress in cloudapi.ipaddress.find()['result']['guidlist']:
        try:
            cloudapi.ipaddress.delete(ipaddress)
        except:
            continue

    for backplane in cloudapi.backplane.find()['result']['guidlist']:
        try:
            cloudapi.backplane.delete(backplane)
        except:
            continue

    for logicalview in cloudapi.logicalview.find()['result']['guidlist']:
        try:
            cloudapi.logicalview.delete(logicalview)
        except:
            continue
