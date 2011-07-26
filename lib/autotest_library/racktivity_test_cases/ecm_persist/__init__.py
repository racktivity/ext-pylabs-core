from datetime import datetime, timedelta
from pylabs import q, i

class Constants:
    USER_NAME = 'testUserForAutoTest'
    DASHBOARD1_NAME = 'dashboard1'
    DASHBOARD2_NAME = 'dashboard2'
    WIDGET1_NAME = 'widget1'
    WIDGET2_NAME = 'widget2'
    WIDGET3_NAME = 'widget3'
    WIDGET4_NAME = 'widget4'
    WIDGETTYPE1_NAME = 'widget_type1'
#    WIDGETTYPE1_SETTINGS = [{'key':'refreshrate', 'defaultvalue':'300'}, {'key':'url', 'defaultvalue':'http://www.renewableenergyworld.com/rss/renews.rss'}, {'key':'maxitems', 'defaultvalue':'5'}, {'key':'optionsdisplaystyle', 'defaultvalue':'slide'}]
    WIDGETTYPE1_SETTINGS = [{'key':'wt1_setting1', 'defaultvalue':'wt1_value1'}, {'key':'wt1_setting2', 'defaultvalue':'wt1_value2'}]
    WIDGETTYPE1_TAGS = ['tag1', 'tag2']
    WIDGETTYPE1_DESCRIPTION = 'Description of widget 1'
    WIDGETTYPE2_NAME = 'widget_type2'
    WIDGETTYPE2_SETTINGS = [{'key':'wt2_setting1', 'defaultvalue':'wt2_value1'}, {'key':'wt2_setting2', 'defaultvalue':'wt2_value2'}]
    WIDGETTYPE2_TAGS = ['tag3', 'tag4']
    WIDGETTYPE2_DESCRIPTION = 'Description of widget 2'
    CONSUMER_KEY = USER_NAME
    CONSUMER_SECRET = 't35tp455w0rd'
    TOKEN_KEY = '839d463a-6bfc-11e0-92e3-af56637bdded'
    TOKEN_SECRET = '8bef8e74-6bfc-11e0-9854-272dac9792e1'

def _createWidgetType(osis, name, settings, tags, description):
    widgettype = osis.widgettype.new()
    widgettype.name = name
    widgettype.icon = "%s.png" % name
    widgettype.packagename = "racktivity_%s" % name
    widgettype.packageversion = "1.1"
    widgettype.tags = tags
    widgettype.description = description
    for setting in settings:
        newSetting = widgettype.widgettypesettings.new()
        newSetting.key = setting['key']
        newSetting.defaultvalue = setting['defaultvalue']
        widgettype.widgettypesettings.append(newSetting)
    osis.widgettype.save(widgettype)
    return widgettype

def _createDashboard(osis, name, order, user):
    dashboard = osis.dashboard.new()
    dashboard.title = name
    dashboard.userguid = user.guid
    dashboard.order = order
    osis.dashboard.save(dashboard)
    return dashboard

def _createWidget(osis, title, nr, type, dashboard):
    widget = osis.widget.new()
    widget.title = title
    widget.dashboardguid = dashboard.guid
    widget.column = (nr % 3) + 1
    widget.order = (nr % 2) + 1
    widget.width = 1
    widget.height = 500 
    widget.collapsed = False
    #widget.widgettypeguid = "167f1844-c27c-4651-a137-cd1adcccbacc" #type.guid
    widget.widgettypeguid = type.guid
    for setting in type.widgettypesettings:
        newSetting = widget.widgetsettings.new()
        newSetting.key = setting.key
        newSetting.value = setting.defaultvalue
        widget.widgetsettings.append(newSetting)
    osis.widget.save(widget)
    return widget

def _createToken():
    client = q.clients.arakoon.getClient('ecm_cluster')
    validuntil = (datetime.now() + timedelta(hours = 1.0)).strftime("%s")
    client.set(key='token_$(%s)' % Constants.TOKEN_KEY, value=str({'validuntil':validuntil, \
                                                          'tokensecret':Constants.TOKEN_SECRET}))
def _removeToken():
    client = q.clients.arakoon.getClient('ecm_cluster')
    if client.exists('token_$(%s)' % Constants.TOKEN_KEY):
        client.delete('token_$(%s)' % Constants.TOKEN_KEY)

def prepare():
    osis = i.config.osisconnection.find('ecm_persist')
    """
        Create test user with 2 dashboards
        Create 2 widgets in each dashboard
        Create 2 widgettypes
    """
    # Create test user
    user = osis.uiuser.new()
    user.name = Constants.USER_NAME
    osis.uiuser.save(user)
    Constants.USER_GUID = user.guid
    
    # Create widget types
    widgettype1 = _createWidgetType(osis, Constants.WIDGETTYPE1_NAME, Constants.WIDGETTYPE1_SETTINGS, Constants.WIDGETTYPE1_TAGS, Constants.WIDGETTYPE1_DESCRIPTION)
    widgettype2 = _createWidgetType(osis, Constants.WIDGETTYPE2_NAME, Constants.WIDGETTYPE2_SETTINGS, Constants.WIDGETTYPE2_TAGS, Constants.WIDGETTYPE2_DESCRIPTION)
    Constants.WIDGETTYPE1_GUID = widgettype1.guid
    Constants.WIDGETTYPE2_GUID = widgettype2.guid

    # Create dashboards
    dashboard1 = _createDashboard(osis, Constants.DASHBOARD1_NAME, 1, user)
    dashboard2 = _createDashboard(osis, Constants.DASHBOARD2_NAME, 2, user)
    Constants.DASHBOARD1_GUID = dashboard1.guid
    Constants.DASHBOARD2_GUID = dashboard2.guid

    # Create widgets in first dashboard
    widget1 = _createWidget(osis, Constants.WIDGET1_NAME, 1, widgettype1, dashboard1)
    widget2 = _createWidget(osis, Constants.WIDGET2_NAME, 2, widgettype2, dashboard1)
    Constants.WIDGET1_GUID = widget1.guid
    Constants.WIDGET2_GUID = widget2.guid

    # Create widgets in second dashboard
    widget3 = _createWidget(osis, Constants.WIDGET3_NAME, 3, widgettype2, dashboard2)
    widget4 = _createWidget(osis, Constants.WIDGET4_NAME, 4, widgettype1, dashboard2)
    Constants.WIDGET3_GUID = widget3.guid
    Constants.WIDGET4_GUID = widget4.guid
    
    # Set selected dashboard
    user.selecteddashboardguid = dashboard1.guid
    osis.uiuser.save(user)

    _createToken()

def cleanup():
    """
        Clean up test user and all his items
    """
    osis = i.config.osisconnection.find('ecm_persist')
    
    # Find user(s)
    userFilter = osis.uiuser.getFilterObject()
    userFilter.add('view_uiuser_list', 'name', Constants.USER_NAME)
    userGuids = osis.uiuser.find(userFilter)
    for userGuid in userGuids:
        user = osis.uiuser.get(userGuid)
        # Find dashboards
        dashboardFilter = osis.dashboard.getFilterObject()
        dashboardFilter.add('view_dashboard_list', 'userguid', userGuid)
        dashboardGuids = osis.dashboard.find(dashboardFilter)
        for dashboardGuid in dashboardGuids:
            dashboard = osis.dashboard.get(dashboardGuid)
            # Find widgets
            widgetFilter = osis.widget.getFilterObject()
            widgetFilter.add('view_widget_list', 'dashboardguid', dashboardGuid)
            widgetGuids = osis.widget.find(widgetFilter)
            for widgetGuid in widgetGuids:
                widget = osis.widget.get(widgetGuid)
                for setting in widget.widgetsettings:
                    widget.widgetsettings.remove(setting)
                osis.widget.delete(widgetGuid)
            osis.dashboard.delete(dashboardGuid)
        osis.uiuser.delete(userGuid)
    # Find widget types
    typeGuids = list()
    type1Filter = osis.widgettype.getFilterObject()
    type1Filter.add('view_widgettype_list', 'name', Constants.WIDGETTYPE1_NAME)
    type1Guids = osis.widgettype.find(type1Filter)
    typeGuids.extend(type1Guids)
    type2Filter = osis.widgettype.getFilterObject()
    type2Filter.add('view_widgettype_list', 'name', Constants.WIDGETTYPE2_NAME)
    type2Guids = osis.widgettype.find(type2Filter)
    typeGuids.extend(type2Guids)

    # Remove each widget type
    for typeGuid in typeGuids:
        type = osis.widgettype.get(typeGuid)
        for setting in type.widgettypesettings:
            type.widgettypesettings.remove(setting)
        osis.widgettype.delete(typeGuid)

    _removeToken()