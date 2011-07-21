__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    
    sql = \
    """
select 
    ipaddress.view_ipaddress_list.address, 
    ipaddress.view_ipaddress_list.netmask, 
    ipaddress.view_ipaddress_list.guid, 
    case 
    when lan.view_lan_list.publicflag = 'f' then 'False' 
    when lan.view_lan_list.publicflag = 't' then 'True' 
    end as ispublic 
from ipaddress.view_ipaddress_list 
inner join only lan.view_lan_list on cast(lan.view_lan_list.guid as varchar) = ipaddress.view_ipaddress_list.languid 
where ipaddress.view_ipaddress_list.languid = '%s'
    """ % params["languid"]

    result = p.api.model.racktivity.ipaddress.query(sql)
    
    params['result'] = {'returncode': True,
                        'ipinfo': result}
    
def match(q, i, params, tags):
    return True
