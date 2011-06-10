[qptasklets]: /pylabsdoc/#/PyLabs50/QPTasklets
[Ocaml]: http://caml.inria.fr/ocaml/index.en.html


## Creating a Binary Q-Package

A binary Q-Package is a Q-Package that contains binary files from an existing application. The creation of a Binary Q-Package itself is complete similar as explained in the [Creating a Q-Package] section.

The typical procedure to create such a Q-Package:

1. check out the code from an application: get the source files via the [codemanagement][qptasklets] tasklet.
2. compile the code: compile the source code in order to become compatible with PyLabs 5
3. package the code

Below you find the `codemanagement`, `compile`, and `package` tasklet for the [Ocaml][] Package.


#### Example of codemanagement Tasklet
In this example, the source of the OCaml package is a `tar.gz` file. The tasklet downloads the source code, and extracted in the PyLabs temporary directory.

[[include:name=codemanagement]][[/include]]


#### Example of compile Tasklet
The `compile` tasklet is responsible to make OCaml PyLabs aware.

[[include:name=compile]][[/include]]


#### Example of package Tasklet
The `package` tasklet copies the compiled package to the proper location in PyLabs.

[[include:name=package]][[/include]]
