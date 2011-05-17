## Q-Shell's Magic Functions

Since the Q-Shell is completely based on IPython, you can use the magic commands (often referred to as magic functions) of IPython in the Q-Shell. A _magic command_ provides a series of functions which allow you to control the behavior of IPython itself, plus a lot of system-type features. All these functions are prefixed with a % character, but parameters are given without parentheses or quotes.

For example, you can run test scripts, debug a test script, store the used variables and its values when leaving the Q-Shell, etc...

To get a list of the magic functions, press '%' and ENTER.

![Magic Functions](images/images50/qshell/Q-Shell_06.png)

Just like the PyLabs functions, you can call the help of a magic function by adding the question mark to the magic function.

    In [3]: %magic?
    Definition: %magic(self, parameter_s='')
    Documentation:
        Print information about the magic function system.
        

### Store Session Variables
When using the Q-Shell in an interactive way, it is possible that you have defined several variables. It is possible to store these variables in the internal Q-Shell database. When closing and restarting your Q-Shell you can recall the stored variables.

    In [5]: aCompany = "Incubaid"
    
    In [6]: anInteger = 19
    
    In [7]: %store aCompany
    Stored 'aCompany' (str)
    
    In [8]: %store anInteger
    Stored 'anInteger' (int)
    
    Close and restart your Q-Shell
    In [1]: aCompany
    Out[1]: 'Incubaid'
    
    In [2]: anInteger
    Out[2]: 19

Recall the complete list of stored variables by calling the function `%store`.

To remove all variables: `%store -z`


###Run a Python File
Supposed that you have created a small script (`helloWorld.py`) that you have saved in the directory {{/home/user}}. The script only prints "Hello World!" on your screen. To run this script from the Q-Shell:

    In [1]: cd /home/user/
    /home/user
    
    In [2]: %run helloWorld.py
    Hello World!


### Save Lines to a File
When you are testing in the Q-Shell, you do not want to lose or retype all the lines to obtain a script. With the `%save` function, you can select the lines that you want to save to a file. Automatically the `.py` extension is added to the file name.

    In [7]: print "Hello Moon!"
    Hello World!
    
    In [8]: %save helloWorld 7
    File `helloWorld.py` exists. Overwrite (y/[N])? y
    The following commands were written to file `helloWorld.py`:
    print "Hello Moon!"
    
    In [9]: %run helloWorld.py
    Hello Moon!

As you can notice, if the file would already exist, it can be overwritten.
