__author__ = 'racktivity'
__tags__ = 'wizard', 'datacenter_create'
COUNTRIES = ['Afghanistan',
             'Albania',
             'Algeria',
             'American Samoa',
             'Andorra',
             'Angola',
             'Anguilla',
             'Antarctica',
             'Antigua and Barbuda',
             'Argentina',
             'Armenia',
             'Aruba',
             'Australia',
             'Austria',
             'Azerbaijan',
             'Bahamas',
             'Bahrain',
             'Bangladesh',
             'Barbados',
             'Belarus',
             'Belgium',
             'Belize',
             'Benin',
             'Bermuda',
             'Bhutan',
             'Bolivia',
             'Bosnia and Herzegovina',
             'Botswana',
             'Bouvet Island',
             'Brazil',
             'British Indian Ocean Territory',
             'British Virgin Islands',
             'Brunei Darussalam',
             'Bulgaria',
             'Burkina Faso',
             'Burundi',
             'Cambodia',
             'Cameroon',
             'Canada',
             'Cape Verde',
             'Cayman Islands',
             'Central African Republic',
             'Chad',
             'Chile',
             'China',
             'Christmas Island',
             'Cocos (Keeling) Islands',
             'Colombia',
             'Comoros',
             'Congo',
             'Cook Islands',
             'Costa Rica',
             "Cote d'Ivoire",
             'Croatia',
             'Cuba',
             'Cyprus',
             'Czech Republic',
             'Denmark',
             'Djibouti',
             'Dominica',
             'Dominican Republic',
             'Ecuador',
             'Egypt',
             'El Salvador',
             'Equatorial Guinea',
             'Eritrea',
             'Estonia',
             'Ethiopia',
             'Falkland Islands',
             'Faroe Islands',
             'Fiji',
             'Finland',
             'France',
             'French Guiana',
             'French Polynesia',
             'French Southern Territories',
             'Gabon',
             'Gambia',
             'Georgia',
             'Germany',
             'Ghana',
             'Gibraltar',
             'Greece',
             'Greenland',
             'Grenada',
             'Guadeloupe',
             'Guam',
             'Guatemala',
             'Guernsey',
             'Guinea',
             'Guinea-Bissau',
             'Guyana',
             'Haiti',
             'Heard Island and McDonald Islands',
             'Holy See',
             'Honduras',
             'Hong Kong',
             'Hungary',
             'Iceland',
             'India',
             'Indonesia',
             'Iran',
             'Iraq',
             'Ireland',
             'Isle of Man',
             'Israel',
             'Italy',
             'Jamaica',
             'Japan',
             'Jersey',
             'Jordan',
             'Kazakhstan',
             'Kenya',
             'Kiribati',
             'Korea',
             'Kuwait',
             "Lao People's Democratic Republic",
             'Latvia',
             'Lesotho',
             'Liberia',
             'Liechten',
             'Lithuania',
             'Luxembourg',
             'Macedonia',
             'Madagascar',
             'Malaysia',
             'Maldives',
             'Malta',
             'Marshall Islands',
             'Martinique',
             'Mau',
             'Mauritius',
             'Mayotte',
             'Mexico',
             'Moldova',
             'Monaco',
             'Mongol',
             'Montenegro',
             'Montser',
             'Morocco',
             'Mozambique',
             'Myanmar',
             'Nauru',
             'Ne',
             'Netherlands Antilles',
             'New Caledonia',
             'Nicaragua',
             'Niger',
             'Nigeria',
             'Niue',
             'Norfolk Island',
             'North',
             'Norway',
             'Oman',
             'Palau',
             'Panama',
             'Paragu',
             'Peru',
             'Philippines',
             'Pitcairn Islands',
             'Portugal',
             'Puerto',
             'Qatar',
             'Romania',
             'Russian Federation',
             'Rwanda',
             'Saint Helena',
             'Saint Kitts and Nevis',
             'Saint Martin',
             'Saint Vincen',
             'Samoa',
             'San Marino',
             'Sao Tome and Principe',
             'Senegal',
             'Serbia',
             'Seychelles',
             'Sierra Leone',
             'Singapore',
             'Slovenia',
             'Solomon Islands',
             'South Africa',
             'South Georgia and the So',
             'Spain',
             'Sudan',
             'Suriname',
             'Svalbard & Jan Mayen Islands',
             'Swaziland',
             'Sweden',
             'Syrian Arab Republic',
             'Taiwan',
             'Tajikistan',
             'Tanzania',
             'Thailand',
             'Timor-Leste',
             'To',
             'Togo',
             'Tokelau',
             'Trinidad and Tobago',
             'Tunisia',
             'Turkey',
             'Turkmenistan',
             'Tuvalu',
             'Ukraine',
             'United Arab Emirates',
             'United Kingdom',
             'United States Minor Outlyin',
             'United States Virgin I',
             'United States of America',
             'Uruguay',
             'Uzbekistan',
             'Venezuela',
             'Vietnam',
             'Wallis and Futuna',
             'Yemen',
             'Zambia',
             'Zimbabwe',
             'land Islands']

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

def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    locationguid = params['extra']['locationguid']
    feeds = cloudapi.feed.list()['result']['feedinfo']
    feedDict = dict([(feed['guid'], feed['name']) for feed in feeds if not feed['datacenterguid']])
    feedDict['new'] = 'Create new feed'
    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Create Datacenter')
    tab.addText('name', 'Name', message='Please enter the datacenter name', optional=False)
    tab.addMultiline('description', 'Description', message='Please enter the datacenter description')
    tab.addText("latitude", "Latitude", validator="^\d*(\.\d+)?$")
    tab.addText("longitude", "Longitude", validator="^\d*(\.\d+)?$")
    tab.addChoice('feed', 'Feed', feedDict, selectedValue='new', message='Please select a feed')
    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        else:
            valid = True

    tab = form.tabs['main']
    tagstring = getTagString(q, tab)
    
    lat = tab.elements['latitude'].value or 0.0
    long = tab.elements['longitude'].value or 0.0
    
    result = cloudapi.datacenter.create(name=tab.elements['name'].value,
                               description=tab.elements['description'].value,
                               locationguid=locationguid,
                               coordinatesinfo={'latitude': float(lat),
                                                'longitude': float(long)},
                               tags=tagstring)

    datacenterguid = result['result']['datacenterguid']
    feedchoice = tab.elements['feed'].value
    if feedchoice == 'new':
        productiontypes = dict([(k, k.capitalize()) for k in q.enumerators.feedProductionType._pm_enumeration_items.keys()])
        feedform = q.gui.form.createForm()
        feedtab = feedform.addTab('feed', 'Create Feed')
        feedtab.addText('name', 'Name', optional=False)
        feedtab.addChoice('productiontype', 'Production Type', productiontypes, optional=False)
        feedtab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
        feedtab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
        form.loadForm(q.gui.dialog.askForm(feedform))
        feedtab = form.tabs['feed']
        tagstring = getTagString(q, feedtab)
        cloudapi.feed.create(name=feedtab.elements['name'].value,
                                      feedproductiontype=feedtab.elements['productiontype'].value,
                                      tags=tagstring,
                                      datacenterguid=datacenterguid)
    else:
        cloudapi.feed.updateModelProperties(feedchoice, datacenterguid=datacenterguid)

    q.gui.dialog.showMessageBox('Datacenter "%s" is being created' % tab.elements['name'].value, "Create Datacenter")

def main(q, i, p, params, tags):
    return True