echo firefox "file:///opt/qbase3/apps/pywizardsdk/vpdcwizard.swf?allowScriptAccess=always&wizardName=test&wizardTitle=titleexample&wizardSdkAddress=localhost&wizardSdkPort=7799"
echo If it doesn't work check you flash install go to http://www.adobe.com/software/flash/about

/opt/qbase3/bin/python wizardRunner.py --host localhost --port 7799

