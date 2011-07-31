__tags__ = "wizard", "feed_delete"
__author__ = "racktivity"

def main(q,i,params,tags):
    cloudApi = i.config.cloudApiConnection.find('main')

    feedguid = params['extra']['feedguid']
    feed = cloudApi.feed.getObject(feedguid)
    datacenter = cloudApi.datacenter.getObject(feed.datacenterguid)
    numoffeeds = 0
    for feedconnector in feed.feedconnectors:
        if feedconnector.cableguid:
            numoffeeds += 1

    answer = q.gui.dialog.showMessageBox('''The current feed is used by Datacenter %s, and has %s connected device(s),
are you sure you want to delete this feed?''' % (datacenter.name, numoffeeds),
                                             "Delete feed", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer.lower() == "no":
        return
    
    cloudApi.feed.delete(feedguid=feedguid)
    q.gui.dialog.showMessageBox("Feed '%s' is being deleted" % feed.name, "Delete Feed")

def match(q,i,params,tags):
    return True