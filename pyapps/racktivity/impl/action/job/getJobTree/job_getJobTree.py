__author__ = 'racktivity'
__tags__ = 'job', 'getJobTree'
__priority__= 3

def main(q, i, params, tags):
    sql= '''SELECT DISTINCT JOBLIST.guid,
                JOBLIST.parentjobguid,
                CLOUDUSER.login as cloudusername,
                JOBLIST.actionname,
                JOBLIST.name,
                JOBLIST.description,
                JOBLIST.starttime,
                JOBLIST.endtime,
                JOBLIST.jobstatus,
                FROM ONLY job.view_job_list JOBLIST
                LEFT JOIN clouduser.view_clouduser_list as CLOUDUSER on JOBLIST.clouduserguid = CLOUDUSER.guid
                where JOBLIST.guid in (
                                                WITH RECURSIVE childjobs AS
                                                (
                                                    -- non-recursive term
                                                    SELECT job.view_job_list.guid
                                                    FROM job.view_job_list
                                                    WHERE job.view_job_list.parentjobguid = '%(rootobjectguid)s'

                                                    UNION ALL

                                                    -- recursive term
                                                    SELECT jl.guid
                                                    FROM job.view_job_list AS jl 
                                                    JOIN
                                                        childjobs AS cj
                                                        ON (jl.parentjobguid = cj.guid)
                                                )
                                                SELECT guid from childjobs
                                      )
                or JOBLIST.guid = '%(rootobjectguid)s'
                ORDER BY JOBLIST.starttime;'''
                
    jobs = q.drp.job.query(sql%{'rootobjectguid': params['rootobjectguid']})
    
    params['result'] = {'returncode': True,
                        'jobtree': jobs}

def match(q, i, params, tags):
    return True