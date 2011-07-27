##Projects

You can browse your imported projects, to edit files. Edited files are synchronized back automatically to
it's original location on *Save*.
 
- To import projects, go to the "Import" page in the *Admin* space and follow instructions.
- To export/delete a project, just right click the project name in the projects tree.

----------------------------


<link rel=StyleSheet href="/static/lfw/js/libs/jstree/themes/classic/style.css" type="text/css" />
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.jstree.js"/>

<div id="editortabs">
    <ul>
    </ul>
</div>

<script language='javascript'>
    $("#editortabs").tabs({tabTemplate: "<li><a href='#{href}'>#{label}</a> <span title='Save' style='cursor: pointer' class='ui-icon ui-icon-note'>Save</span> <span title='Close' style='cursor: pointer' class='ui-icon ui-icon-close'>Close</span></li>",
                           panelTemplate: "<div style='height: 600px'></div>",
                            add: function(e, ui) {
                                /*
                                console.log("In add event");
                                console.log(e);
                                console.log(ui);
                                $(ui.panel).append($("<p>").text("This is my new tab"));
                                */
                            }});
    
</script>
