@metadata title=Name Spaces
@metadata order=90
@metadata tagstring=name spaces q i p libraries

[pyapps]: /#/PyLabsApps/Home


#Name Spaces
PyLabs has three name spaces, `i.`, `p.`, and `q.`, that give access to the PyLabs libraries. Each of the name spaces has its own specific purpose in PyLabs.

The `q.` name space is used when writing scripts. The commands in this name space are not interactive, they require that all input parameters are given when the command is called. Although the `q.` name space
is not interactive it can still be used inside the Q-Shell, mainly for testing purposes prior to writing a script.

The `i.` name space provides interactivity in the Q-Shell: commands do not have to be entered with sets of parameters unlike in the `q.` name space. Instead the user is asked to enter the parameters step by step. 
As a result, many Q-Shell operations are much more user-friendly, because you do not need to know all the parameters for the commands. Commands in the `i.` name space cannot be used inside a script if the script needs to run without user interaction.

The last name space, `p.`, is used to control PyLabs applications ([PyApps][pyapps], for example to install or start a PyApp.