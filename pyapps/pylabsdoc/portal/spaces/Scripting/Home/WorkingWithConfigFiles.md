@metadata title=Configuration Files
@metadata order=30
@metadata tagstring=config configuration file


#Working with Configuration Files

Sometimes it can be useful to work with configuration files. PyLabs is able to populate or modify such configuration files.


##Configuration File Structure

The configuration files must be plain text files and have the following structure:

    [section1]
    param1 = value1
    param2 = value2
     
    [section2]
    param3 = value3
    
There is no specific file extension required for the configuration file.


##Creating a New Configuration File

[[tip]]
Do not close your Q-Shell session throughout this complete page.
[[/tip]]

Creating a new configuration file is very easy. In this example we create the configuration file `foo.cfg` in the directory `/opt/qbase5/cfg/foo`. The directory `foo` does not necessarily exist in your environment.

Execute the code below in the Q-Shell:

[[code]]
cfgName = 'foo.cfg'
newCfgDir = q.dirs.cfgDir + 'foo/'

newCfgFile = q.tools.inifile.new(newCfgDir + cfgName)
[[/code]]

If you look in `/opt/qbase5/cfg/foo`, you see an empty file `foo.cfg`. In the next section you learn how to populate the created configuration file.


##Populating a Configuration File
After creating the configuration file, you can start adding the configuration parameters. As shown above, a configuration file consists of sections and each section has its own parameters.
To add a parameter to the configuration file, you have to provide a section name, a parameter name, and value for the parameter.
If you add a parameter to a section, that does not yet exist, your script will fail.

Bear in mind that section names are case sensitive.

[[code]]
newCfgFile.addSection('section1')
newCfgFile.addParam('section1', 'foo', 'bar')
[[/code]]

If you now open the file `foo.cfg` in `/opt/qbase5/cfg/foo`, you see the following data:

    [section1]
    foo = bar
    
Now you can add as many sections and parameters as you want.


##Updating a Configuration File
Sometimes it may be required to update a configuration file, for example add, update, or remove parameters. There exist some functions to assist you in retrieving sections and parameters:

[[code]]
iniFile = q.tools.inifile.open('/opt/qbase5/cfg/foo/foo.cfg')

iniFile.getSections()
iniFile.getParams('section1')
[[/code]]

Both `get` functions return a list, where the latter is a list of parameter names, excluding their values.

If you want to know if a section or parameter exists, use the Boolean `check` functions:

[[code]]
iniFile.checkSection('section1')
iniFile.checkParam('section1', 'foo')
[[/code]]

To add a section and parameters, just do the same as in the previous paragraph. To assign a new value to a parameter, add the parameter with the same section and parameter name, but with a new value.

[[code]]
iniFile.addSection('new section')
iniFile.addParam('new section', 'john', 'cleese')

iniFile.addParam('section1', 'foo', 'baz1')
iniFile.addParam('section1', 'bar', 'baz2')
[[/code]]

These commands results in the following configuration file:

    [my section]
    john = cleese
    
    [section1]
    foo = baz1
    bar = baz2
