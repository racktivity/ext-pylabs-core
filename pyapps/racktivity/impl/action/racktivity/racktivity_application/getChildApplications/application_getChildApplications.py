__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'getChildApplications'
__priority__= 3


def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    sql = """
    SELECT DISTINCT appSrv.applicationtemplateguid, 
                    appSrv.machineguid as machineguid, 
                    appSrv.service2applicationguid, 
                    appSrv.guid as guid, 
                    appList.name as applicationname,
                    appList.status, 
                    appSrv."servicename", 
                    appList.description, 
                    ( SELECT machine.view_machine_list.name
                      FROM machine.view_machine_list
                      WHERE appSrv.machineguid = machine.view_machine_list.guid) as machinename
                    FROM  ONLY racktivity_application.view_racktivity_application_services appSrv 
                    INNER JOIN racktivity_application.view_racktivity_application_list appList
                    ON appList.guid = appSrv.guid
                    AND service2applicationguid = '%s'
	                --AND appList.template = False
    """
    sql = sql%params['applicationguid']
    
    applics = q.drp.racktivity_application.query(sql)
 
    keys = ['guid','applicationname', 'description','status', 'applicationtemplateguid','machinename', 'machineguid']
    results = list()
    for app in applics:
        result = dict()
        for key in app.iterkeys():
            if key in keys:
                result[key] = app[key]
        results.append(result)    
    params['result'] = {'returncode':True, 'childinfo':results}

def match(q, i, params, tags):
    return True


