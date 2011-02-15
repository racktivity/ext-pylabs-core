# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

# To be sure that code and comments will not be moved, place all items in a file in this order:
#     - Comment header (all lines starting with #)
#     - Class definitions (comments and code above, between and below the classes will be grouped together)
#     - File-level methods (comments between methods will be grouped together)
#     - File-level commands and comments

# The parser code in CodeStructure.process() has still some issues:
#     - Multiline strings are not supported
#     - Already existing properties will not be parsed as property.    

INDENT = 4

from pylabs import q
from exceptions import SyntaxError

from codetools.parser.PropertyDef import PropertyDef
from codetools.parser.MethodDef import MethodDef
from codetools.parser.ClassDef import ClassDef
from codetools.parser.CodeFile import CodeFile
from codetools.parser.TypeDef import TypeDef

class CodeParser:
    
    def __init__(self):
        pass

    def parse(self, filePath):
        
        cf = CodeFile(filePath)
        lines = q.system.fileGetContents(filePath).split("\n")
        state="filestart"
        decorators=[]
        currentClassDef = None
        currentMethodDef = None
        
        for lineNr in range(len(lines)):
            
            line = lines[lineNr]
            
            if state == "defbody_inmultilinestring":
                currentMethodDef.addLine2body(line)
                if len(line.split('"""')) == 2: # The line contains ["""] exactly once
                    state = "defbody"
                continue
                
            if line.strip() == "": #check if we find an empty line, which we have to ignore
                if state == "defbody":
                    currentMethodDef.body += "\n"
                continue
            
            if (state=="defbody" or state=="defheader") and not currentClassDef is None and not line.startswith(" " * INDENT * 2): # If currentClassDef is None, we were parsing a file-level method.
                state = "classbody" # We were parsing a class-level method, but the indentation of the current line is too short to be part of that method. Thus, the method code has ended.
                
            if (state=="defbody" or state=="defheader") and currentClassDef is None and not line.startswith(" " * INDENT):
                state = "filebody" # We were parsing a file-level method, but the indentation of the current line is too short to be part of that method. Thus, the method code has ended.
                
            if (state=="classbody" or state=="classheader") and not line.startswith(" " * INDENT):
                currentClassDef = None
                state = "filebody" # We were parsing a class, but the indentation of the current line is too short to be part of the class. Thus, the class-code has ended.
                                
            if (state=="filestart" or state == "filebody") and line.lower().strip().startswith("namespace"):
                # This line defines the namespace where the file belongs.
                if not cf.namespace == "":
                    raise Exception("Cannot set namespace twice.")
                if line.find("=") == -1:
                    raise Exception("Syntax error in line [%s]. Correct format: [namespace = \"com.acme.mynamespace\"]" % line)
                namespaceString = line.split("=")[1].split("#")[0].strip()
                if not ((namespaceString.startswith('"') and namespaceString.endswith('"')) or (namespaceString.startswith("'") and namespaceString.endswith("'"))): # The value is a string
                    raise Exception("Syntax error in line [%s]. Correct format: [namespace = \"com.acme.mynamespace\"]" % line)
                cf.namespace = namespaceString[1:-1] # Strips leading and trailing quotes.
                continue
                                
            if (state=="filestart" or state == "filebody") and line.lower().strip().startswith("datatypes"):
                # This line defines the file where datatypes used in the file are defined.
                if not len(cf.types) == 0:
                    raise Exception("Cannot set datatypes twice.")
                if line.find("=") == -1:
                    raise Exception("Syntax error in line [%s]. Correct format: [datatypes = \"types.ini\"] or [datatypes = [\"types1.ini\", \"types2.ini\", \"types3.ini\"]]" % line)
                typefilesString = line.split("=")[1].split("#")[0].strip()
                if typefilesString.startswith("[") and typefilesString.endswith("]"):
                    typefilesArray = [tf.strip for tf in typefilesString[1:-1].split(",")]
                else:
                    typefilesArray = [typefilesString]
                for fileString in typefilesArray:
                    if not ((fileString.startswith('"') and fileString.endswith('"')) or (fileString.startswith("'") and fileString.endswith("'"))): # The value is a string
                        raise Exception("Syntax error in line [%s]. Correct format: [datatypes = \"types.ini\"] or [datatypes = [\"types1.ini\", \"types2.ini\", \"types3.ini\"]]" % line)
                continue
                                                                                                               
            if state=="filestart":
                if line.startswith("#"): # License code
                    if not len(cf.license) == 0:
                        cf.license += "\n"
                    cf.license += line.strip()[1:]
                    continue
                elif line.startswith("import ") or line.startswith("from "): # Module imports
                    cf.imports += line + "\n"
                    continue
                else: # Header has ended
                    state = "filebody"
                 
            if state=="filebody" and line.lower().startswith("class "): # Class definition found
                classfound=True
                toParse = line
                
                # Find comments
                if toParse.find("#") > -1:
                    toParse, comment = line.split("#", 1)
                else:
                    comment = ""
                toParse = toParse[6:].rstrip(": ") # converts "class foo(super):  " to "foo(super)"

                # Find classname and inheritance
                if toParse.find("(")==-1:
                    classname = toParse
                    inheritance = ""
                else:
                    classname=toParse.split("(")[0].strip()
                    inheritance=toParse.split("(")[1].rstrip(")")

                # Create classDef object        
                currentClassDef = ClassDef(cf, classname, inheritance.strip(), comment)
                cf.addClassDef(currentClassDef)
                q.logger.log("**CLASS:%s" % classname)
                state = "classheader"
                continue
            
            if state == "classheader" and line.lstrip().startswith('"'*3): # Class docstring found
                toParse = line.strip()[3:].strip()
                if toParse.endswith('"'*3): # One-line docstring
                    currentClassDef.docstring = toParse[:-3].strip()
                else:
                    state = "classheader_indocstring"
                    if len(toParse) > 0:
                        currentClassDef.docstring = toParse
                continue
            
            if state == "classheader_indocstring":
                toParse = line.strip()
                if toParse.endswith('"'*3):
                    if len(toParse) > 3:
                        currentClassDef.docstring += "\n" + toParse[:-3]
                    state = "classheader"
                else:
                    currentClassDef.docstring += "\n" + toParse
                continue
            
            if state in ["classheader", "classbody", "filebody"] and line.lstrip().startswith("##@"): # Class decorator found
                decorators += [s.strip() for s in line.strip(" #@").split("@")]
                if state == "classheader":
                    state = "classbody"
                continue
            
            if state in ["classheader", "classbody"] and line.lstrip().startswith("##+"): # This line defines a pre-initialized instance of the class.
                                                                                          # Example : # line                    == "    ##+ name = "test", id = 5    , enabled = True  # a comment"
                lineWithoutComments     = line.lstrip()[3:].split("#")[0]                             # line                    == " name = "test", id = 5    , enabled = True  "
                nameValueStrings        = lineWithoutComments.split(",")                              # nameValueStrings        == [" name = \"test\"", " id = 5   ", " enabled = True  "]
                nameValuePairs          = [s.split("=") for s in nameValueStrings]                    # nameValuePairs          == [[" name ", " \"test\""], [" id ", " 5   "], [" enabled ", " True  "]]
                nameValueTuplesStripped = [(p[0].strip(), p[1].strip()) for p in nameValuePairs]      # nameValueTuplesStripped == [("name", "\"test\""), ("id", "5"), ("enabled", "True")]
                currentClassDef.preinitEntries.append(dict(nameValueTuplesStripped))                  # preinitEntries[-1]      == {"name": "\"test\"", "id": "5", "enabled": "True"}
                continue
            
            if (state == "classheader" or state == "classbody") and line.lstrip().startswith("#"): # Comments found
                if not currentClassDef.comment == "":
                    currentClassDef.comment += "\n"
                currentClassDef.comment += line.strip().lstrip("#")
                continue

            if state == "classheader":
                if line.strip() == "pass" or line.strip().startswith("pass ") or line.strip().startswith("pass#"):
                    state = "filebody"
                    q.logger.log("Found empty class: [%s]" % currentClassDef.name, 6)
                    currentClassDef = None
                    continue
                else: # All possible content for class headers is already caught. If we reach here, the body of the class begins.
                    state = "classbody"
                
            if state == "classbody" and line.startswith(" " * INDENT + "def "): # Class-level function definition found
                state = "parsedef"

            if state == "filebody" and line.startswith("def "): # File-level function definition found. Set currentClassDef = None to make clear we're in a file-level function.
                currentClassDef = None
                state = "parsedef"
            
            if state == "parsedef": # Parse the function definition.
                toParse = line
                
                # Find comments
                if toParse.find("#") > -1:
                    toParse, comment = line.split("#", 1)
                else:
                    comment = ""
                toParse = toParse.lstrip().rstrip(": ") # converts "    def foo(self, x):  " to "foo(self, x)"

                # Find methodname and params
                methodname=toParse.split("(")[0][3:].strip() # Take everything between [def] and [(].
                params=toParse.split("(")[1].rstrip(")")

                # Create methodDef object        
                currentMethodDef = MethodDef(currentClassDef, cf, methodname, params, comment, decorators)
                if currentClassDef is None:
                    cf.addMethodDef(currentMethodDef)
                else:
                    currentClassDef.addMethodDef(currentMethodDef)
                q.logger.log("**METHOD:%s" % classname)
                decorators = []
                state = "defheader"
                continue

            
            if state == "defheader" and line.lstrip().startswith('"'*3): # Function docstring found
                toParse = line.strip()[3:].strip()
                if toParse.endswith('"'*3): # One-line docstring
                    currentMethodDef.docstring = toParse[:-3].strip()
                    state = "defbody"
                else:
                    state = "defheader_indocstring"
                    currentMethodDef.docstring = toParse
                continue
            
            if state == "defheader_indocstring":
                toParse = line.strip()
                if toParse.endswith('"'*3):
                    if len(toParse) > 3:
                        if not currentMethodDef.docstring == "":
                            currentMethodDef.docstring += "\n"
                        currentMethodDef.docstring += toParse[:-3]
                    state = "defbody"
                else:
                    if not currentMethodDef.docstring == "":
                        currentMethodDef.docstring += "\n"
                    currentMethodDef.docstring += toParse
                continue
            
            if state == "defheader": # No method header found, assuming start of method body
                state = "defbody"
            
            if state == "defbody":
                currentMethodDef.addLine2body(line)
                if currentMethodDef.name == "__init_properties__":
                   #init properties contains the class properties definitions
                   #TODO: Code is not complete no check for dict, key,t array types...
                   q.logger.log("reading property",6)
                   dictKey = ""
                   if line.find("##") > -1: # Property definition with type specifier found
                        propNameAndDefVal, propTypeAndComments = line.split("##", 1)
                        if propTypeAndComments.find("#") > 1:
                            propType, propComments = propTypeAndComments.split("#", 1)
                        else:
                            propType, propComments = propTypeAndComments, ""
                   else: # The property definition has no type specifier
                        if line.find("#") > 1:
                            propNameAndDefVal, propComments = line.split("#", 1)
                        else:
                            propNameAndDefVal, propComments = line, ""
                        propType = ""
                   if propNameAndDefVal.find("=") == -1:
                       propName, propDefVal = propNameAndDefVal.strip(), "None" # The property has no default value
                   else:
                       propName, propDefVal = propNameAndDefVal.split("=")
                   if propType.strip().lower().startswith("array("):
                       propType = propType.strip()[6:-1]
                       isArray = True
                   else:
                       isArray = False
                   if propType.strip().lower().startswith("dict("):
                       params = propType.strip()[5:-1].split(",")
                       dictKey = params[0]
                       propType = params[1]
                       isDict = True
                   else:
                       isDict = False
    
                   q.logger.log("Adding property with name %s" % propName.strip())
                   currentClassDef.addPropertyDef(PropertyDef(currentClassDef, propName.strip(), propDefVal.strip(), propType.strip(), propComments.strip(), isArray = isArray, isDict = isDict,dictKey = dictKey, decorators = decorators))
                   decorators = [] # reset decorator list.


                if len(line.split('"""')) == 2: # The line contains ["""] exactly once
                    state = "defbody_inmultilinestring"
                continue
            
            if state == "classbody": # We're in a classbody, but not in a function body. Lines starting with "#" are already caught. So this line is a property definition.
                if line.find("##") > -1: # Property definition with type specifier found
                    propNameAndDefVal, propTypeAndComments = line.split("##", 1)
                    if propTypeAndComments.find("#") > 1:
                        propType, propComments = propTypeAndComments.split("#", 1)
                    else:
                        propType, propComments = propTypeAndComments, ""
                else: # The property definition has no type specifier
                    if line.find("#") > 1:
                        propNameAndDefVal, propComments = line.split("#", 1)
                    else:
                        propNameAndDefVal, propComments = line, ""
                    propType = ""
                if propNameAndDefVal.find("=") == -1:
                    propName, propDefVal = propNameAndDefVal.strip(), "None" # The property has no default value
                else:
                    propName, propDefVal = propNameAndDefVal.split("=")
                if propType.strip().lower().startswith("array("):
                    propType = propType.strip()[6:-1]
                    isArray = True
                else:
                    isArray = False
                    
                currentClassDef.addPropertyDef(PropertyDef(currentClassDef, propName.strip(), propDefVal.strip(), propType.strip(), propComments.strip(), isArray = isArray, decorators = decorators))
                decorators = [] # reset decorator list.
                continue
            
            if state == "filebody":
                cf.body += line + "\n"
                continue
            
            #Should never reach here.
            raise SyntaxError("Could not parse [%s]. Ended with state [%s]." % (self.dir + os.sep + self.name, state))
            
        return cf