@metadata title=Updating a Q-Package
@metadata order=60
@metadata tagstring=update qpackage


# Updating a Q-Package

When you need to apply changes to an application, you have to create a new version of the Q-Package.
There are two ways to create an update of a new Q-Package:

* via the `quickPackage` method on a Q-Package
* via manual intervention in the PyLabs 5 Q-Package directories


## quickPackage to Update Q-Package

The `quickPackage` method on a Q-Package is by far the easiest way to update a Q-Package. With this method you have to retrieve the Q-Package and execute the `quickPackage` method on it.

The `quickPackage` method performs three tasks:

* **checkout**: download the sources from the versioning system of the Q-Package
* **compile**: compile the sources to make them compatible with PyLabs
* **package**: package the sources

See [Creating a Q-Package|Creating a Q-Package#Building the Q-Package] for more information.

After executing the `quickPackage` method, you have to publish the domain in which the updated Q-Package resides, to make the new version of the Q-Package readily available to other users.


## Manual Update of a Q-Package
In the procedure of the above section, one is considered to have all sources in a versioning system (e.g. Mercurial, Bazaar, ...). This is far out the most recommended way to manage your applications.
However, an alternative is to manually update the sources in the Q-Package directories of your PyLabs framework. This is then the procedure to follow:

1. Find and download the Q-Package via the Q-Shell:
[[code]]
i.qp.find('your app')
i.qp.lastPackage.download()
[[/code]]
This action downloads the bundle (`.tgz` file) of the Q-Package to `/opt/qbase5/var/qpackages4/bundles/<domain>`.
<br />
2. Extract the Q-Package to the Q-Package directory of PyLabs: 
<br>
[[warning]]
**Warning** 
<br>
Leave the Q-Shell session open!
    cd /opt/qbase5/var/qpackages4/bundles/<domain>
    tar xvf <packagename>.tgz -C /opt/qbase5/var/qpackages4/files/<domain>/<Q-Package>/<version>/<platform>/
[[/warning]]
<br>
3. Apply the changes to the files in the Q-Package directories (`/opt/qbase5/var/qpackages4/files/<domain>/<Q-Package>/<version>/<platform>/`).
<br />
4. Optionally compile the sources:
[[code]]
i.qp.lastPackage.compile()
[[/code]]
<br>
5. Publish the new Q-Package:
<br>
[[code]]
i.qp.publishDomain('yourdomainname', commitMessage='your commitmessage here')
[[/code]]
[[warning]]
**Warning** 
<br>
The changes introduced by a manual update are NOT part of the version repositories.  The next regular package release will inevitably overwrite the changes.  To avoid this, you need to add the changes to the version repository.
[[/warning]]
