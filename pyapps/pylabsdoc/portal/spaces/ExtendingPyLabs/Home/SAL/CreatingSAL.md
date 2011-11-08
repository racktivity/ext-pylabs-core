@metadata title=Creating a SAL
@metadata order=10
@metadata tagstring=create sal extension

[extensiontutorial]: #/ExtendingPylabs/CreateExtension


#Creating SAL's

SAL means 'System Abstraction Layer' it is used to abstract an underlying layer.
Typically it means creating extensions to support the same API to manage or use applications on different platforms.

Being called a SAL, does not mean it is only used to make an abstract layer above different operating systems, but it is also used for the management extensions of different tools or to contact APIs.


## SAL Basic Structure

A basic extension should consist of at least 2 files:

* Main class file
* Extension file

### Extension File

The extensions file contains a reference to the file and class which functions should be available and a 'mount point' on which the functionality can be called.

    [hook_cloud_api_generator]
    qlocation=q.generator.cloudapi
    moduleName=CloudApiGenerator
    classname=CloudApiGenerator
    enabled=1

* *qlocation:* is the hook on which the new functions are available.
* *moduleName:* is the name of the file in the same directory which contains the classname.
* *classname:* is the class which will be exposed in the qlocation.


## Example

Take a look at the [Extension Tutorial][extensiontutorial].