@metadata title=Q-Package Tasklets
@metadata order=50
@metadata tagstring=tasklet compile backup codemanagement configure install package start stop

[Mercurial]: http://mercurial.selenic.com/
[configure]: #/Q-Packages/Configure


# Q-Package Tasklets

## backup Tasklet
The `backup` tasklet is the tasklet tagged with "backup".
The `backup` tasklet allows one to take a backup of the data stored in the data structure being used.
The restore tasklet lets you put the saved data back in the data structure.

[[code]]
Out[1].backup(url='ftp://login:password@10.100.1.1/myroot/')
Out[1].restore(url='ftp://login:password@10.100.1.1/myroot/')
[[/code]]


## codemanagement Tasklet
The `codemanagement` tasklet is the tasklet tagged with "codemanagement". 
It is mainly used to get the necessary code from a version control system or from a local repository. It is used to gather the different files and directories into one Q-Package, a so called _recipe_.


###Using a Recipe File
Using the _recipe_ is the easiest way to get the necessary code for your Q-Package. The recipe is stored in the file `recipe.json` and must be created in `/opt/qbase5/var/qpackages4/metadata/<domain>/<qpackage name>/<version>/`.
The recipe file is a list of dicts. Each dict contains the location, branch, and the required directories from the version control system. One recipe may refer to multiple repositories.  

Below you find an example of a recipe:

	[
	  { "branch" : "default",
	    "location" : "https://bitbucket.org/foo/bar/",
	    "mapping" :
	      {
	        "pyapps/newapp" : "generic/pyapps/newapp"
	      }
	  },
	  {
	    "branch" : "default",
        "location" : "http://bitbucket.org/another/location",
	    "mapping" :
	     {
	        "docs/somedocs" : "generic/pyapps/newapp/portal/spaces/somedocs",
	        "docs/moredocs" : "generic/pyapps/newapp/portal/spaces/moredocs"
	     }
	  }
	]

By calling the `checkout()` method on a package, the codemanagement tasklet is executed. 
These are the steps that are executed when using the recipe file:

1. First a clone is created of the branches defined in the recipe. The destination of the clone is asked for when calling the `checkout()` method. 
In the above example, there are two repositories (`bar` and `location`).
The clone is created in for example `/opt/qbase5/var/mercurial/`, where you find the two repositories.
2. Execute the mapping from the recipe, which copies the directories from `/opt/qbase5/var/mercurial/<repo>/<mapping source>` to `/opt/qbase5/var/src/<qpackage name>/<version>/<mapping destination>`.
For the given example, `/opt/qbase5/var/mercurial/bar/pyapps/newapp` will be recursively copied to `/opt/qbase5/var/src/newapp/<version>/generic/pyapps/newapp`.



###Without a Recipe File
An alternative is to work without the `recipe.json` file, then you have to put everything in the `codemanagement` tasklet.
Pylabs 5 has a built-in [Mercurial][] client, which allows you to clone a Mercurial repository into Pylabs:

[[code]]
connection =  i.config.clients.mercurial.findByUrl("link to mercurial repo")
[[/code]]

This action not only creates a connection to the repository, but creates a local clone of the selected Mercurial repository.
With the created `connection` object, you can do the same actions as the CLI version of Mercurial, but in a simplified way

To create a Mercurial recipe:

[[code]]
from clients.mercurial.HgRecipe import HgRecipe
recipe = HgRecipe()
recipe.addRepository(connection)
[[/code]]

Once you have your connection you can decide which directories or files you need for your Q-Package recipe. To add source files or directories to a recipe:

[[code]]
recipe.addSource(?
Definition: recipe.addSource(self, hgConnection, source_path, destination_path, branch='')
Documentation:
    Add a source (ingredient) to the recipe
[[/code]]

The `addSource()` method takes three parameters:

* a Mercurial connection
* A string, representing the path of a directory in the Mercurial repository, relative to the root of the cloned repository
* A string, representing the corresponding path in `/opt/qbase5`


## compile Tasklet
The `compile` tasklet is the tasklet tagged with "compile". 
The tasklet is only necessary if the package needs to be compiled in order to become usable for Pylabs, for example the _ocaml_ Q-Package.

This tasklet compiles the source files and put the resulting files in their proper location in Pylabs. The tasklet can assume that the source files are put in Pylabs in advance, for example by the codemanagement tasklet.

The tasklet should:

1. Install any tools (e.g. compilers) needed for compilation
2. Add the location of the compiler to the environment-variable PATH, and set the environment variable LIBRARY_PATH to `/opt/qbase5/lib`
3. Compile the source-files.


## configure Tasklet
The `configure` tasklet is the tasklet tagged with "configure". 
The `configure` tasklet allows you to configure an application after its installation, for example [setting a default configuration of a web server][configure]. 
The install tasklet of the Q-Package needs a `signalConfigurationNeeded` parameter in order to execute this tasklet.

[[code]]
#excerpt of install tasklet:
qpackage.signalConfigurationNeeded()
[[/code]]

If this line is present, the Q-Shell is restarted after the Q-Package installation then launches this `configure` tasklet. This tasklet saves the necessary data in the required configuration files.


## install Tasklet
The `install` tasklet is the tasklet tagged with "install".

This tasklet must copy all files from the package-directory to the proper location in the Pylabs framework, and execute all other necessary actions during installation. The package directory can be retrieved from the Q-Package object by calling the function `getPathFiles()`.

There are two helper functions:

* *<qpackage>.copyFiles()*: this function copies all files from the package-directory to the proper directories in Pylabs. It expects that the files are organized by the platform they should be installed on. For example, the files in /files/<domain>/<name>/<version>/windows/ will only be copied if the Q-Package is installed on a windows platform, and files in /files/<domain>/<name>/<version>/generic/ will be copied in any case.

* *q.qpackagetools.copyEggToSandbox(sourceEggZipFile, targetEggFile)*: this function is used when installing a Python Egg. It will rename the egg based on the Pylabs conventions for an Egg version. The function takes two parameters:
    * The location (full path) of the source Egg-file in the package-directory.
    * The directory (full path) in Pylabs, where the Egg must be installed.


## package Tasklet
The `package` tasklet is the tasklet tagged with "package".

This tasklet must pick all files from the Pylabs sandbox and copy them to the proper place in the Pylabs Q-Package directories `/opt/qbase5/var/qpackages4/files/...`. 
When you use the recipe file, the source files are located in `/opt/qbase5/var/src...`.

The tasklet must package the files to the form they will be installed. (For example: compiling `.py` files to `.pyc` files, combine multiple JAVA `.class` file to a single `.JAR` archive)

There is a helper function called `q.qpackagetools.convertSourceToPyc()` which takes a path as argument. All `.py` files in that path (and in any sub-directory) will be compiled to `.pyc` files. It is advised to copy all files to their proper directory first, and then compile the `.py` files in place.


## startstop Tasklet
The `startstop` tasklet has two methods, `start` and `stop`, to respectively start and stop the application.

*`start` method*
The goal is to provide a method to start (stop/restart) services without having the extension already installed.

*`stop` method*
The goal is to provide a method to stop (start/restart) services without having the extension already installed.
