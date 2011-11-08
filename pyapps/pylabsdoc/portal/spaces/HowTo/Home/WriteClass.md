@metadata title=Write a Class
@metadata tagstring=class write


# How to Write a Class in Pylabs

## Example Class

[[code]]
# for entry level programs we use:
from pylabs.InitBaseCore import q
# in pylabs framework we use:
import pylabs

class ExampleClass():
    """ Documentation string 

    This is the more extensive documentation of this class.
    """

    def __init__(self):
        """ Initialization of the class """
        

    def exampleMethod(self, number, qpackageList):
        """ This example method does example 
        
        The example uses the qpackageList and does a number of activities on,...
        
        @param number: The number value used for...
        @param qpackageList: The qpackageList contains the qpackages
        @return: list of reworked qpackages
        """

    ###
    Implement the rest of your class here
    ###
[[/code]]
