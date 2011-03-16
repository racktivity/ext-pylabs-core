__tags__ = 'wizard','order','create'
__author__ = 'incubaid'

TAB_GENERAL_TITLE = 'General'
TAB_GENERAL_PRODUCT = 'Product :'
TAB_GENERAL_PRODUCT_HELPTEXT = 'Please choose a product'
TAB_GENERAL_QUANTITY = 'Quantity :'
TAB_GENERAL_QUANTITY_HELPTEXT = 'Please select the quantity required'

MSGBOX_CONFIRMATION = "Proceed with the order?"
MSGBOX_CONFIRMATION_TITLE = "Order confirmation"

MSGBOX_ORDER_FAILED = "Failed to confirm your order! Please contact your system administrator!"
MSGBOX_ORDER_FAILED_TITLE = "Order confirmation failed"


def callCloudAPI(q, i, productguid, quantity):

    cloudAPI = i.config.cloudApiConnection.find('main')
    cloudAPI.setCredentials(params['login'],params['password'])
    result = cloudAPI.order.create(params['customerguid'])['result']
    result = cloudAPI.order.addItem(result, productguid, quantity)['result']
    
    return result


def getProducts(q, api):
    products = dict()
    result = api.product.list()['result']
    
    map(lambda x: products.__setitem__(x['guid'], x['description']), result)
    return products


def callback_productChanged(q, i, params, tags) :
    cloudAPI = i.config.cloudApiConnection.find('main')
    cloudAPI.setCredentials(params['login'],params['password'])
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    tab_general = form.tabs['general']

    return form

def callback_quantityChanged(q, i, params, tags) :
    cloudAPI = i.config.cloudApiConnection.find('main')
    cloudAPI.setCredentials(params['login'],params['password'])
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    tab_general = form.tabs['general']

    return form

def main(q, i, params, tags):

    cloudAPI = i.config.cloudApiConnection.find('main')
    cloudAPI.setCredentials(params['login'],params['password'])

    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    ###########################
    # General information tab #
    ###########################

    tab_general.addDropDown(name     = 'product',
                            text     = TAB_GENERAL_PRODUCT,
                            values   = templates,
                            selectedValue = templateguid,
                            trigger  = 'change',
                            callback = 'productChanged',
                            helpText = TAB_GENERAL_PRODUCT_HELPTEXT)

    tab_general.addInteger(name = 'quantity',
                          text = TAB_GENERAL_QUANTITY,
                          minValue = 1,
                          maxValue = 10,
                          value = 1,
                          helpText = TAB_GENERAL_QUANTITY_HELPTEXT,
                          trigger = 'change',
                          callback = 'quantityChanged',
                          stepSize = 1)


    answer = q.gui.dialog.showMessageBox(message=MSGBOX_CONFIRMATION,
                                         title=MSGBOX_CONFIRMATION_TITLE,
                                         msgboxButtons='OKCancel',
                                         msgboxIcon='Question',
                                         defaultButton='OK')

    if answer == 'CANCEL':
        return

    result = callCloudAPI(q, i,
    					  tabgeneral.elements['product'].value,
    					  tabgeneral.elements['quantity'].value)

def match(q,i,params,tags):
    return True
