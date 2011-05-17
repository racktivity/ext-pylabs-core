## Q-Shell Debug Mode

It might occur that something goes wrong in your Q-Shell and that you get a message that you must run Q-Shell in debug mode for more information. To do so:

1. Open a terminal session and go to your {{/opt/qbase}} folder.
2. Run {{./qshell -d}}

Your Q-Shell starts in debug mode.

### Extra Functionality

When Q-Shell debug mode is activated, following functionality is available in Q-Shell:
* Private methods and members (starting with `pm_` or an underscore) are visible when using tab completion.
* When an error occurs, the full stacktrace is printed on the screen.
* When you ask information about a function (by adding a question mark at the end) you will get more extensive information about the location and type of the function.
