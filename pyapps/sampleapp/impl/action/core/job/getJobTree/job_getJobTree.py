__author__ = 'aserver'
__tags__ = 'job', 'getJobTree'
__priority__= 3

def main(q, i, p, params, tags):
    sql= '''SELECT DISTINCT JOBLIST.guid,
                JOBLIST.parentjobguid,
                CLOUDUSER.login as cloudusername,
                JOBLIST.actionname,
                JOBLIST.name,
                JOBLIST.description,
                JOBLIST.starttime,
                JOBLIST.endtime,
                JOBLIST.jobstatus,
                JOBLIST.joborder,
                (SELECT ML.name FROM machine.view_machine_list as ML WHERE ML.guid = MACHINELIST.guid) as Executor
                FROM ONLY job.view_job_list JOBLIST
                LEFT JOIN clouduser.view_clouduser_list as CLOUDUSER on JOBLIST.clouduserguid = CLOUDUSER.guid
                LEFT JOIN machine.view_machine_list as MACHINELIST on CAST(MACHINELIST.agentguid as VARCHAR) = CAST(JOBLIST.agentguid as VARCHAR)
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
                ORDER BY JOBLIST.joborder;'''

    jobs = p.api.model.core.job.query(sql%{'rootobjectguid': params['rootobjectguid']})
    params['result'] = jobs

def match(q, i, params, tags):
    return True
