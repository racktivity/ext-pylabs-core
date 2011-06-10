[qpinstall]: /pylabsdoc/#/Q-Packages/QPInstall


## EJabberd

This paragraph will briefly describe EJabberd.
Please note that the steps below are essential for installing EJabberd, so do not skip them.


### Creating a User

Before you install Ejabberd, you have to make sure there is a user on your system called "qbase". To do this, open a terminal, insure you have super user permissions  and run the following command:

    useradd qbase


### User Configuration Package

Once the user has been created, you can proceed with installing the "qbaseuserconfig" Q-Package.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.


### Reviewing the Default User

When the package is installed, you have to review the default user and provide a password:

    i.config.qbase.users.review()


### Installing EJabberd

After carrying out the instructions in the previous sections, you can now proceed with installing EJabberd.

The Q-Package is called "ejabberd"; find and install the latest one.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.

After the installation is complete, you should have EJabberd successfully installed in your sandbox.