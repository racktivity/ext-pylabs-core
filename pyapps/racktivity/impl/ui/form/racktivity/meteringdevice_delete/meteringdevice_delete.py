__tags__ = "wizard", "meteringdevice_delete"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = i.config.cloudApiConnection.find('main')
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudApi.meteringdevice.getObject(meteringdeviceguid=meteringdeviceguid)
    children = cloudApi.meteringdevice.find(parentmeteringdeviceguid=meteringdevice.guid)['result']['guidlist']
    numactivepowerinputs = 0
    numactivepoweroutputs = 0
    activepowerinputlist = list()
    activepoweroutputlist = list()
    for powerinput in meteringdevice.powerinputs:
        if powerinput.cableguid:
            numactivepowerinputs = numactivepowerinputs + 1
            activepowerinputlist.append(powerinput)
    for poweroutput in meteringdevice.poweroutputs:
        if poweroutput.cableguid:
            numactivepoweroutputs = numactivepoweroutputs + 1
            activepoweroutputlist.append(poweroutput)
    answer = q.gui.dialog.showMessageBox('''The current Energy Switch has %s connected power input(s), %s connected power output(s), \
and %s children Energy Switch(s)\
Are you sure you want to delete this Energy Switch ?''' % (numactivepowerinputs, numactivepoweroutputs, len(children) ),
                                            "Delete Energy Switch", msgboxButtons="YesNo",
                                            msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    cloudApi.meteringdevice.delete(meteringdevice.guid)
    q.gui.dialog.showMessageBox("Energy Switch '%s' is being deleted" % meteringdevice.name, "Delete Energy Switch")

def main(q, i, p, params, tags):
    return True