<link rel=StyleSheet href="/static/lfw/js/libs/jstree/themes/classic/style.css" type="text/css" />
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.jstree.js"/>
<script language="javascript" src="/static/lfw/js/filetree.js"/>

<table>
    <tr>
        <td colspan=2>
            <select id="appname" name="appname"></select>
        </td>
    </tr>
    <tr>
        <td>
            <div id="treediv"></div>
        </td>
        <td>
            <div id="filediv"></div>
        </td>
    </tr>
</table>

<script language="javascript">
x = null
//jsTree node clicked
function nodeSelected(event, data) {
    path = data.inst._get_node().attr("id");
    data.inst.open_node()
    
    //update the file view
    $.ajax({
      url: "appserver/rest/ui/editor/listFilesInDir",
      type: "POST",
      data: "appname=" + getCurrentApp() + "&id=" + path,
      success: refreshFileView,
      error: error
    });
}

function refreshFileView(data)
{
    var ROW_NUM = 3
    var c = 0;
    var html = "<table border=1>"
    files = data["files"];
    path = data["path"];
    //remove the first part of the path until the word Imported
    idx = path.indexOf("Imported/") + 9
    path = path.substr(idx,path.length)
    //encode the slashes /
    path = path.replace(/\//g, "%2f");

    for (var i=0; i < files.length; i++)
    {
        c++;
        if (c == 1)
            html += "<tr>";
        filename = files[i][0]
        fileext = files[i][1]
        if (fileext)
            pagelink="<a href='/../" + getCurrentApp() + "/#/Imported/" + path + "%2f" + filename + "' target='_blank'>" +filename + "</a>";
        else
            pagelink="<b>" + filename + "</b>";
        html += "<td>" + pagelink + "</td>"
        if (c == ROW_NUM)
        {
            html += "</tr>\n";
            c = 0;
        }
    }
    html += "</table>";
    document.getElementById("filediv").innerHTML = html;
}

//Select "appname" value changed
function appChanged()
{
    $("#dirname").val("");
    //Reload tree
    loadTree(getCurrentApp());
    //Reload applications
    //reloadApps();
    return true;
}
//return currently selected application
function getCurrentApp() {
    return $("#appname").val();
}

function getContextMenu(node)
{
    root = this._get_parent(node) == -1;
    text = this.get_text(node);
    result = null;
    if (root)
    {
        result = {
            "export": {
                "label"				: "Export project '"  + text + "'",
                "action"			: exportProject },
            "delete" : {
                "label"				: "Delete project '"  + text + "'",
                "action"			: deleteProject }
        }
    }
    return result;
}

function deleteProject(node)
{
    text = this.get_text(node);
    
    //update the file view
    $.ajax({
      url: "appserver/rest/ui/editor/deleteProject",
      type: "POST",
      data: "appname=" + getCurrentApp() + "&projectname=" + text,
      success: function () {
          alert("Project " + text + " has been deleted"); 
          loadTree(getCurrentApp());
        },
      error: error
    });
}

function exportProject(node)
{
    text = this.get_text(node);
    
    //update the file view
    $.ajax({
      url: "appserver/rest/ui/editor/exportProject",
      type: "POST",
      data: "appname=" + getCurrentApp() + "&projectname=" + text,
      success:  function () {
          alert("Project " + text + " has been exported"); 
        },
      error: error
    });

}

//Load specific app's tree
function loadTree(appname){
    //Clear the file view
    document.getElementById("filediv").innerHTML = "";

    $("#appname").val(appname)
    tree = loadFileTree("#treediv", appname, "portal/spaces/Imported", getContextMenu);
    tree.bind("select_node.jstree", nodeSelected);
};

function error(data)
{
    data = $.parseJSON(data.responseText);
    alert("Fail: " + data["exception"]);
}

function init()
{
    //Hide the toolbox
     $("#toolbar").css("visibility", "hidden")
    //Initalize appname combobox
    select = $('#appname');
    var applist = $.ajax({
        url: "appserver/rest/ui/editor/listPyApps",
        async: false}).responseText;
    applist = $.parseJSON(applist)

    $.each(applist, function(index, app) { 
      select.append($("<option></option>").text(app));
    });
    select.change(appChanged);
    //Initalize tree
    appChanged();
}

$(document).ready(init);
</script>
