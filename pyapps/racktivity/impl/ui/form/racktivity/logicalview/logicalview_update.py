__tags__ = 'wizard','logicalview_update'
__author__ = 'racktivity'


def getTagString(q, tab):
    labels = None
    labelsvalue = tab.elements['labels'].value
    trim = lambda s: s.strip()
    if labelsvalue:
        labels = set(map(trim, labelsvalue.split(',')))

    tags = dict()
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in map(trim, tagsvalue.split(',')):
            tagslist = tag.split(':')
            tags[tagslist[0].strip()] = tagslist[1].strip()
    return q.base.tags.getTagString(labels, tags)


DISABLE_PARENTTREE = True

TYPES_MAP = {'campus': 'Campus',
             'datacenter': 'Datacenter',
            'floor': 'Floor',
            'room': 'Room',
            'pod': 'Pod',
            'row': 'Row',
            'rack': 'Rack',
            'energyswitch': 'EnergySwitch'}

OBJ_ORDER = ('campus', 'datacenter', 'floor', 'room',
            'pod', 'row', 'rack', 'energyswitch')

def callback_type_selected(q, i, params, tags):
    form = q.gui.form.createForm()
    formData = params['formData']
    form.loadForm(formData)
    tab = form.tabs['main']
    if tab.elements['search_type'].value == 'energyswitch_port':
        tab.elements['search_parent_type'].values = {'energyswitch': 'EnergySwitch'}
        tab.elements['search_parent_type'].value = 'energyswitch'
        tab.optional = False
        return form
    
    selected = tab.elements['search_type'].value
    index = OBJ_ORDER.index(selected)
    
    possibleparents = dict([ (OBJ_ORDER[i], TYPES_MAP[OBJ_ORDER[i]]) for i in range(index)])
    possibleparents['any'] = 'Any'
    tab.elements['search_parent_type'].values = possibleparents
    tab.elements['search_parent_type'].value = 'any'
    tab.optional = False
    return form

def main(q, i, params, tags):

    cloudapi = i.config.cloudApiConnection.find('main')
    form = q.gui.form.createForm()
    logicalviewguid = params['extra']['logicalviewguid']
    logicalview = cloudapi.logicalview.getObject(logicalviewguid)
    
    tab = form.addTab('main', 'Update Logical View')
    tab.addText('name', 'Name', value=logicalview.name, message='Please enter the logical view name', optional=False)
    
    tab.addChoice("search_type", "Type", {'datacenter': 'Datacenter',
                                                    'floor': 'Floor',
                                                    'room': 'Room',
                                                    'pod': 'Pod',
                                                    'row': 'Row',
                                                    'rack': 'Rack',
                                                    'energyswitch': 'EnergySwitch',
                                                    'energyswitch_port': 'EnergySwitch port'},
                                                    selectedValue="",
                                                    message='Select the type of the entity you want to view.',
                                                    helpText="Select the types to view. In case of EnergySwitch port, you can select other types.",
                                                    trigger="change", callback="type_selected")
    
    tab.addText('search_tags_labels', 'Match Tags & Labels', message='Please enter the tags and labels to search separated by && or ||',
                helpText="Enter here the lables and tags you want to match. && and || can be used (e.g 'label1 && label2' or 'tag1:value1 && label2'", optional=True)
    
    tab.addText('search_name', 'Match Name', message='Please enter the name to search separated by && or ||',
                helpText="Enter here the Name you want to match. && and || can be used, also * can be used to do a NOT exact match (e.g 'name1 && namex*'", optional=True)
    
    tab.addChoice("search_parent_type", "Parent Type", {'any': 'Any',
                                                        'campus': 'Campus'},
                                                        selectedValue="any",
                                                        message='Select the type of the parent.',
                                                        helpText="Select the types to view. In case of EnergySwitch port, you can select other types.")
    
    tab.addText("search_parent_name", "Parent Name", message="The parent name", helpText="The parent name (exact match) must be provided if a parent is selected")
    
    tab.addMultiline('description', 'Description', value=logicalview.description, message='Please enter the logical view description')
    tab.addYesNo('share', "Share", selectedValue=logicalview.share, status='', trigger=None, callback=None)
    tagobj = q.base.tags.getObject(logicalview.tags or '')
    tab.addText('tags', 'Tags',  value=",".join(["%s:%s" % (k, v) for k, v in tagobj.tags.iteritems()]),
                helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', value=",".join(tagobj.labels),
                helpText='Enter labels as comma separated values e.g. label1,label2')
    
    valid = False
    while not valid:
        valid = True
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        parent = tab.elements['search_parent_type'].value
        if parent != "any":
            parentname = tab.elements['search_parent_name'].value.strip()
            if not parentname:
                tab.elements['search_parent_name'].message = "Parent name is required"
                tab.elements['search_parent_name'].status = "error"
                valid = False
            else:
                tab.elements['search_parent_name'].status = ""
            
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
            valid = False
    
    #build search string.
    tab = form.tabs['main']
    search = []
    search.append("types:{%s}" % tab.elements['search_type'].value)
    tagslabels = tab.elements['search_tags_labels'].value.strip()
    if tagslabels:
        search.append("tags_labels:{%s}" % tagslabels)
    namesearch = tab.elements['search_name'].value.strip()
    if namesearch:
        search.append("name:{%s}" % namesearch)
        
    parent = tab.elements['search_parent_type'].value
    if parent != "any":
        if parent == "energyswitch" or not DISABLE_PARENTTREE:
            parentname = tab.elements['search_parent_name'].value.strip()
            search.append("parenttree:{%(parent)s:%(name)s}" % {'parent': parent, 'name': parentname})
    
    searchstr = ",".join(search)
    
    tagstring = getTagString(q, tab)
    cloudapi.logicalview.updateModelProperties(logicalviewguid,name=tab.elements['name'].value,
                         viewstring=searchstr,
                         description=tab.elements['description'].value,
                         share=tab.elements['share'].value,
                         tags=tagstring)
    
    q.gui.dialog.showMessageBox("Logical view '%s' is being updated" % tab.elements['name'].value, "Update Logical view")
    

def match(q,i,params,tags):
    return True
