__author__ = 'racktivity'
__tags__ = 'job', 'clear'
__priority__= 3

def main(q, i, params, tags):
    q.drp.job.query("DELETE FROM job.main;SELECT True")
    q.drp.job.query("DELETE FROM job.view_job_list;SELECT True")
    q.drp.job.query("DELETE FROM job.view_job_parentlist;SELECT True")
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
