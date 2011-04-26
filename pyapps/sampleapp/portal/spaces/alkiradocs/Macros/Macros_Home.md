[howto]: /sampleapp/#/alkiradocs/Macros\_HOWTO

#Alkira Macros
As we have mentioned, Alkira is highly customizable; this is due to the fact that you can develop your own macros, which are written in _JavaScript_.
These macros can have a wide range of usage, from highlighting code and showing a Google map, to adding a Wizard.

The macro files themselves (JavaScript files) are stored in `/opt/qbase5/www/lfw/js/macros` and must have unique names.

In this section you can find an overview of the available macros and how you can create [your own macro][howto].


##Adding Macros to Alkira Pages
Adding a macro to an Alkira page is similar to adding a `DIV` element to an HTML page, but with a different syntax.
To add a macro to an Alkira page, use the following structure:

    [[<macroname>: param1=value1, param2=value2, ...]]
    
    ...macrobody...
    
    [[/macroname]]
    
For practical examples, see in the list of implemented macros below.


##Currently Implemented Macros

<div class="macro macro_include">{"name": "Macros"}</div>

