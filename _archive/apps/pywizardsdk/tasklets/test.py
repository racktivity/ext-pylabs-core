__tags__= ('wizard','test')
__author__='pylabs'



def main(q,i,params,tags):


    form = q.gui.form.createForm()
    boatTab = form.addTab('boatTab','Boat')
    form.tabs['boatTab'].addChoice(name = 'boat_choice', text = 'Select your boat options', values = {"bo1": 'Boat option1', "bo2": 'Boat Option2'})
    resultform = q.gui.form.createForm()
    resultform.loadForm(q.gui.dialog.askForm(form))
    q.logger.log('boat choice is %s'%resultform.tabs['boatTab'].elements['boat_choice'].value)

    form.removeTab('boatTab')
    form1 = form
    villaTab = form1.addTab('villaTab', 'Villa')
    form1.tabs['villaTab'].addChoice(name = 'villa_choice', text = 'Select your villa options', values = {'vo1': 'Villa option1', 'vo2': 'Villa Option2', 'vo3': 'Villa Option3'})
    resultform.loadForm(q.gui.dialog.askForm(form1))
    q.logger.log('villa choice is %s'%resultform.tabs['villaTab'].elements['villa_choice'].value)

    form1.removeTab('villaTab')
    form2 = form1
    jetskiTab = form2.addTab('jetskiTab', 'Jet Ski')
    form2.tabs['jetskiTab'].addChoice(name = 'jetski_choice', text = 'Select your Jet Ski options', values = {'jso1': 'Jet Ski option1', 'jso2': 'Jet Ski Option2', 'jso3': 'Jet Ski Option3'})
    resultform.loadForm(q.gui.dialog.askForm(form2))
    #q.logger.log('jetski choice is %s'%resultform.tabs['jetskiTab'].elements['jetski_choice'].value)


def match(q,i,params,tags):
    return True
