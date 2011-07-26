__tags__= "test", "setup"
__priority__ = 100

def main(q, i, params, tags):

    q.qp._runPendingReconfigeFiles()

    ECM_CLUSTER_NAME = 'ecm_cluster'
    # Create the Arakoon cluster used by the OAuth service
    arakoon_clusters = q.manage.arakoon.listClusters()
    if not ECM_CLUSTER_NAME in arakoon_clusters:
        newcluster = q.manage.arakoon.getCluster(ECM_CLUSTER_NAME)
        newcluster.setUp(1)
        newcluster.start()
        cfg = q.clients.arakoon.getClientConfig(ECM_CLUSTER_NAME)
        try:
            cfg.generateFromServerConfig()
        except Exception:
            pass

def match(q, i, params, tags):
    return params['stage'] == 2