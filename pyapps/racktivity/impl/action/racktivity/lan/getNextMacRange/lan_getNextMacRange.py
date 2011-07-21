__author__ = 'racktivity'
__priority__= 3

def increment(mac):
    incremented = False
    items = mac.split(':')
    newmac = []
    while len(newmac) < len(items):
        val = items[-len(newmac)-1]
        if not incremented:
            if int(val,16) < 255 :
                val = hex(int(val,16)+1)[2:4]
                if len(val) == 1: 
                    val = '0' + val
                newmac.append(val)
                incremented = True
            else:
                newmac.append('00')
        else:
            newmac.append(val)
    if incremented:
       return ':'.join(reversed(newmac))
          
def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    sql = "select macrange from lan.view_lan_list where not macrange is null order by macrange desc"
    result = p.api.model.racktivity.lan.query(sql)
    result = increment(result[0]['macrange'])
    params['result'] = {'returncode': True,
                        'macrange': result}
       
def match(q, i, params, tags):
    return True
