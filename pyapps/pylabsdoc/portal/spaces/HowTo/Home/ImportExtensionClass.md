@metadata title=Import Classes from Extensions
@metadata tagstring=import class extension

# How to Import Classes from Extensions

If you have, for example, an extension located at `/opt/qbase5/lib/pylabs/extensions/example/ExampleClass.py` and you wish to import the class `ExampleClass` into your application, use the following import statement:

[[code]]
from example.ExampleClass import ExampleClass
[[/code]]

[[info]]
**Information** 
This is only possible when `__init__.py` has been created in the example folder. If there is no `__init__.py` file then the class can only be used within the extension.
[[/info]]