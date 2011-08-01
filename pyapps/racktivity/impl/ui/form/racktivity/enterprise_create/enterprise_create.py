__author__ = 'racktivity'

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
    cloudapi = i.config.cloudApiConnection.find('main')
    form = q.gui.form.createForm()
    
    enterprisetab = form.addTab('enterprise', 'Enterprise')
    enterprisetab.addText('name', 'Name', message='Please enter the enterprise name', optional=False)
    enterprisetab.addMultiline('description', 'Description', message='Please enter the enterprise description')
    enterprisetab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    enterprisetab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')

    campustab = form.addTab('campus', 'Campus')
    campustab.addText('name', 'Name', optional=False)
    campustab.addMultiline('description', 'Description')
    campustab.addText('alias', 'Alias')
    campustab.addText('address', 'Address')
    campustab.addText('city', 'City')
    campustab.addChoice("country", "Country", dict(enumerate(COUNTRIES)))
    campustab.addYesNo('public', 'Is Public campus')
    campustab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    campustab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        enterprisetab = form.tabs['enterprise']
        enterprisetags = enterprisetab.elements['tags'].value
        campustab = form.tabs['campus']
        campustags = campustab.elements['tags'].value
        if enterprisetags and ':' not in enterprisetags:
            enterprisetab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            enterprisetab.elements['tags'].status = 'error'
            valid = False
        elif campustags and ':' not in campustags:
            campustab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            campustab.elements['tags'].status = 'error'
            valid = False
        else:
            valid = True
        
    campustab = form.tabs['campus']
    tagstring = getTagString(q, campustab)
    
    returnedvalue = cloudapi.location.create(name=campustab.elements['name'].value,
                                                 description=campustab.elements['description'].value,
                                                 alias=campustab.elements['alias'].value,
                                                 address=campustab.elements['address'].value,
                                                 city=campustab.elements['city'].value,
                                                 country=COUNTRIES[int(campustab.elements['country'].value)],
                                                 tags=tagstring,
                                                 public=True if campustab.elements['public'].value=='Yes' else False)
    campusguid = returnedvalue['result']['locationguid']
    
    enterprisetab = form.tabs['enterprise']
    tagstring = getTagString(q, enterprisetab)

    cloudapi.enterprise.create(name=enterprisetab.elements['name'].value,
                               description=enterprisetab.elements['description'].value,
                               campuses=[campusguid],
                               tags=tagstring)

    q.gui.dialog.showMessageBox('enterprise "%s" is being created' % enterprisetab.elements['name'].value, "Create enterprise")

def main(q, i, p, params, tags):
    return True