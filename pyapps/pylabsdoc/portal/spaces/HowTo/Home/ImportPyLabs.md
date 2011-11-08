@metadata title=Import Pylabs
@metadata tagstring=import library extension application


# How to Import Pylabs

There are three ways of importing Pylabs.

## Pylabs in Standard Applications

[[info]]
*Information** In all applications, use the line below to initialize Pylabs and as a result the `q` global variable will be available.
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


## Pylabs in Extensions

[[code]]
from pylabs import q
class testclass()
    def test(self):
        q.logger.log(your_message)
[[/code]]        
   
        
## Pylabs in a Pylabs Library

[[code]]
import pylabs

class testclass()
    def test(self):
        pylabs.q.logger.log(your_message)
[[/code]]
