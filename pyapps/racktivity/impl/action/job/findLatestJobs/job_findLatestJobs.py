__author__ = 'racktivity'
__tags__ = 'job', 'findLatestJobs'
__priority__= 3

def main(q, i, params, tags):
    sql= '''SELECT 
	JOBLIST.guid, 
	JOBLIST.parentjobguid, 
	CLOUDUSER.login as cloudusername,  
	JOBLIST.actionname, 
	JOBLIST.description, 
	JOBLIST.name ,
	JOBLIST.description , 
	JOBLIST.starttime, 
	JOBLIST.endtime, 
	JOBLIST.jobstatus
FROM job.view_job_list JOBLIST
LEFT JOIN clouduser.view_clouduser_list as CLOUDUSER on JOBLIST.clouduserguid = CLOUDUSER.guid
WHERE JOBLIST.jobStatus in (%(jobstatus)s) and JOBLIST.parentjobguid IS NULL
AND (JOBLIST.rootobjecttype IS NULL OR JOBLIST.rootobjecttype NOT IN ('job','cmc'))
ORDER BY JOBLIST.starttime DESC LIMIT %(maxrows)s'''

    jobStatus = "'RUNNING'"
    if params['errorsonly'] == True:
        jobStatus = "'ERROR'"

    params['result'] = {'returncode': True,
                        'joblist': q.drp.job.query(sql%{'jobstatus': jobStatus, 'maxrows':params['maxrows']})}

def match(q, i, params, tags):
    return True