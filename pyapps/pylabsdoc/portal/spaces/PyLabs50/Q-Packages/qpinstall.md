## Installing a Q-Package
The installation of a Q-Package is a simple procedure of two steps, executed in PyLabs' Q-Shell. When you know the exact name of the Q-Package you can even install the Q-Package with one command.

The two steps to install a Q-Package:
1. Finding a Q-Package
2. Installing a Q-Package


#### Before Installing a Q-Package
Prior to the installation of a Q-Package it is recommended to update the Q-Package metadata of your PyLabs framework.

    In [1]: i.qp.updateMetaDataAll()
     Update metadata information for qpackages domain pylabs5
     * updateqpackage metadata for domain pylabs5                DONE
     Update metadata information for qpackages domain pylabs5_test
     * updateqpackage metadata for domain pylabs5_test           DONE
     Update metadata information for qpackages domain qpackages5
     * updateqpackage metadata for domain qpackages5             DONE

The `updateMetaDataAll` method updates the metadata repositories of all domains in your PyLabs framework. This action assures that you will look up the most up to date Q-Packages.

#### Finding a Q-Package
In the Q-Shell use the `findByName` method. This method accepts one argument, the name of the Q-Package. The argument can contain '*' as wildcard, as starting as well as ending character. See the examples below:

    In [12]: i.qp.findByName('agen*')
    lastPackages: [IPackage pylabs5 agent 0.5]
    Out[12]: IPackage pylabs5 agent 0.5
    
    In [13]: i.qp.findByName('agent')
    lastPackages: [IPackage pylabs5 agent 0.5]
    Out[13]: IPackage pylabs5 agent 0.5
    
    In [14]: i.qp.findByName('*gent')
    lastPackages: [IPackage pylabs5 agent 0.5]
    Out[14]: IPackage pylabs5 agent 0.5

It is possible that your `findByName` action returns more than one result. In that case the matches are shown in a list from which you can choose:

    In [17]: i.qp.findByName('ocaml*')
     Multiple packages found, please choose one
        1: IPackage qpackages5 ocaml-pcre 6.0.1
        2: IPackage qpackages5 ocaml-text 0.2
        3: IPackage qpackages5 ocaml-findlib 1.2.4
        4: IPackage qpackages5 ocaml-extra 1.0
        5: IPackage qpackages5 ocaml 3.11.2
        6: IPackage qpackages5 ocaml 3.11.1
        Select Nr (1-6):

To work with the found Q-Package you can either use `i.qp.lastPackage` or store the Q-Package instance in a variable, `package = i.qp.findByName('agent')`.


#### Installing a Q-Package
With the found Q-Package from the previous section you can easily install the Q-Package with the `install` method.

    In [18]: i.qp.lastPackage.install()
    
    or
    
    In [19]: package.install()

**Tip**
If you know the name of the Q-Package, you can install it with one line:

    In [20]: i.qp.findByName('agent').install()
