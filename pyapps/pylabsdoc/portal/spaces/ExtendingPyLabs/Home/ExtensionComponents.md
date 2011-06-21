@metadata title=Extension Components
@metadata order=20
@metadata tagstring=component extension configuration location

[hook]: http://en.wikipedia.org/wiki/Hooking

#Components of an Extension

A PyLabs extension consists of at least two files, a configuration file and a module. For more advanced extensions, it may be necessary to create your own libraries.
Every PyLabs extension has its specific location in the PyLabs directory structure.


##Extension Location

Each PyLabs extension is a subdirectory of `/opt/qbase5/lib/pylabs/extensions` (can be called in the Q-Shell via the command `q.dirs.extensionsDir`).
The name of the subdirectory must be lowercase, use underscores to separate words, for example `my_extension`.


##Extension Configuration File
The name of an extension configuration file is always `extension.cfg`.
Each PyLabs extension has a [hook][] which contains the following information:

* name space location: location in the `q.` name space
* module name: the name of the Python file (without extension), case-sensitive
* class name: name of the class in the module, case sensitive
* enabled: 0 or 1, 0 disables the module (not visible in Q-Shell), 1 enables the configuration

Each hook is a section in the configuration file. The name of a hook must always start with `hook`.

It is possible to hook multiple classes on the `q.` object within one extension. This involves nothing but listing all hooks in the configuration file, making sure all section names start with `hook`.

Example of a configuration file:

    [hook1]
    qlocation=q.demoExtension.demoHelloWorld
    modulename=helloWorldModule
    classname=HelloWorldClass
    enabled=1
     
    [hook2]
    qlocation=q.demo.helloworld
    modulename=hook2HelloWorld
    classname=HelloWorldClass
    enabled=1
     
    [hook3]
    qlocation=q.hello.hook3
    modulename=hook3HelloWorld
    classname=HelloWorldClass
    enabled=1

    
##Extension Module
The module of the extension is a Python file with at least one class, containing one or more methods. 
The file name must match the `modulename` in the extension configuration file and the class name must match the `classname`.
