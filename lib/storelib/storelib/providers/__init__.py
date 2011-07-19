
class IMonitorHistoryProvider(object):
    def create(self, dsid):
        raise NotImplementedError()
    def destroy(self, dsid):
        raise NotImplementedError()
    def exists(self, dsid):
        raise NotImplementedError()
    def save(self, dsid, *args):
        raise NotImplementedError()
    def getLatest(self, dsid):
        raise NotImplementedError()
    def getMin(self, dsid, starttime, endtime):
        raise NotImplementedError()
    def getMax(self, dsid, starttime, endtime):
        raise NotImplementedError()
    def getAverage(self, dsid, starttime, endtime):
        raise NotImplementedError()
    def getRange(self, dsid, resolution, starttime, endtime, aggregationfunction='AVG'):
        raise NotImplementedError()
    def getGroupedLatest(self, dsids, groupfunction):
        raise NotImplementedError()
    def getGroupedMin(self, dsids, starttime, endtime, groupfunction='ADD'):
        raise NotImplementedError()
    def getGroupedMax(self, dsids, starttime, endtime, groupfunction='ADD'):
        raise NotImplementedError()
    def getGroupedAvg(self, dsids, starttime, endtime, groupfunction='ADD'):
        raise NotImplementedError()
    def getGroupedRange(self, dsids, starttime, endtime, groupfunction='ADD'):
        raise NotImplementedError()