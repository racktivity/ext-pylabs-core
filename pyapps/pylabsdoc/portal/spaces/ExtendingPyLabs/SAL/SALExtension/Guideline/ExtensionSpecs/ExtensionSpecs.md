# Writing Specifications for a PyLabs Extension

Specifications define the interface of a PyLabs Extension, or in other words the specification provides information on the methods exposed by a PyLabs Extension.

Typically Specifications are written by a software architect, hence the name "specifications" instead of "Interface". Specifications form the basis for the actual development of the PyLabs Extension by a developer. PyLabs Specifications are not written as a text file, they are written in a standardized format in Python as described in this section.

A Specification file is by itself a Python file that contains the class name and the methods that must be available in the PyLabs Extension. For each class and method the software architect adds the PyDocs so that the developer can fully focus on writing code.

## Specifications for System Wrappers

System Wrappers are implemented as a set of PyMonkey Extensions. The following paragraphs cover specifications for System Wrapper extensions:

[[children]][[/children]]