__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    roomguid = params['roomguid'] or None
    from rootobjectaction_lib import rootobjectaction_list
    
    params['result'] = {'returncode': True,
                        'roominfo': rootobjectaction_list.room_list(roomguid=roomguid)}

def match(q, i, params, tags):
    return True
