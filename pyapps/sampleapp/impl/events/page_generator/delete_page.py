def main(q, i, p, params, tags):
    guid = params["eventBody"]
    p.action.ui.page.delete(guid)
        
def match(q, i, params, tags):
    return 'pylabs.event.sampleapp.osis.delete.' in params["eventKey"]