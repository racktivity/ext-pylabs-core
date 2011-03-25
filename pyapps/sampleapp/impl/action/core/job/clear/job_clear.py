__author__ = 'aserver'
__tags__ = 'job', 'clear'
__priority__= 3

def main(q, i, p, params, tags):
    
    p.api.model.core.job.query("DELETE FROM job.main;SELECT True")
    p.api.model.core.job.query("DELETE FROM job.view_job_list;SELECT True")
    p.api.model.core.job.query("DELETE FROM job.view_job_parentlist;SELECT True")
    #clear policyrun entries as well
    p.api.model.core.job.query("DELETE FROM policyrun.main;SELECT True")
    p.api.model.core.job.query("DELETE FROM policyrun.view_policyrun_list;SELECT True")
    
    params['result'] = True
    
def match(q, i, params, tags):
    return True
