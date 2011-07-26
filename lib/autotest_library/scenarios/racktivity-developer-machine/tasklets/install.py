__tags__ = "test", "setup"
__author__ = "racktivity"
__priority__ = 90

def main(q, i, params, tags):
    q.qp.findNewest("OAuth_lib").install()
    q.qp.findNewest("racktivity_cloud_api_client").install()
    q.qp._runPendingReconfigeFiles()

def match(q, i, params, tags):
    return True