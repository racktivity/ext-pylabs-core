__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    p.api.model.racktivity.job.query("DELETE FROM job.main;SELECT True")
    p.api.model.racktivity.job.query("DELETE FROM job.view_job_list;SELECT True")
    p.api.model.racktivity.job.query("DELETE FROM job.view_job_parentlist;SELECT True")
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
