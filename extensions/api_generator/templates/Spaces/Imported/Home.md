<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.jstree.js"/>
<link rel=StyleSheet href="/static/lfw/js/libs/jstree/themes/classic/style.css" type="text/css" />

<form target="appserver/rest/ui/editor/lisDirsInDir">
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
</form>

<script language="javascript">
x = null
//jsTree node clicked
function nodeClicked(path) {
    node = document.getElementById(path)
    $("#treediv").jstree("open_node", node)
    //update the file view
    $.ajax({
      url: "appserver/rest/ui/editor/listFilesInDir",
      type: "POST",
      data: "appname=" + getCurrentApp() + "&id=" + path,
      success: refreshFileView,
      error: importFail
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
    path = path.replace("/", '%2f');

    for (var i=0; i < files.length; i++)
    {
        c++;
        if (c == 1)
            html += "<tr>";
        pagelink="<a href='#/Imported/" + path + "%2f" + files[i] + "' target='blank_'>" + files[i] + "</a>";
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
    return true;
}
//return currently selected application
function getCurrentApp() {
    return $("#appname").val();
}
//Load specific app's tree
function loadTree(appname){
        $("#appname").val(appname)
    	var tree = $("#treediv").jstree({
    		"json_data": {
    			"ajax": {
    				"url": "appserver/rest/ui/editor/listDirsInDir?appname=" + appname,
    				"data": function(n) {
    					return {id: n.attr ? n.attr("id") : "portal/spaces/Imported"};
    				},
    			"progressive_render" : true
    			}
    		},
            "themes" : {
               "theme" : "classic",
            },
    		"plugins": ["themes", "json_data"]
    	});
        tree.click = nodeClicked;
};

function importSuccess(data)
{
    alert("Success: " + data);
}

function importFail(data)
{
    data = $.parseJSON(data.responseText);
    alert("Fail: " + data["exception"]);
}

function init()
{
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
