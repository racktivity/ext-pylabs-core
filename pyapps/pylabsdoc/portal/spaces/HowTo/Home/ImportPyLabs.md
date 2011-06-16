@metadata title=Import PyLabs
@metadata tagstring=import library extension application


# How to Import PyLabs

There are three ways of importing PyLabs.

## PyLabs in Standard Applications

[[info]]
*Information** In all applications, use the line below to initialize PyLabs and as a result the `q` global variable will be available.
[[code]]
from pylabs.InitBase import *
[[/code]]
[[/info]]

[[code]]
from pylabs.InitBase import *

class testclass()
    def test(self):
        q.logger.log(your_message)

[[/code]]


## PyLabs in Extensions

[[code]]
from pylabs import q
class testclass()
    def test(self):
        q.logger.log(your_message)
[[/code]]        
   
        
## PyLabs in a PyLabs Library

[[code]]
import pylabs

class testclass()
    def test(self):
        pylabs.q.logger.log(your_message)
[[/code]]
