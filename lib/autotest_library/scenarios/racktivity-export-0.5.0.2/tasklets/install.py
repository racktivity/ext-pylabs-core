__tags__ = "test", "setup"
__author__ = "racktivity"
__priority__ = 90

def main(q, i, params, tags):
    q.qp.find("racktivity_cloud_api_client", version="0.5.0.2")[0].install()
    q.qp._runPendingReconfigeFiles()

def match(q, i, params, tags):
    return True