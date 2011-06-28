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
            <div id="demo1" class="demo"></div></td>
        <td>
            Directory to import <input type="text" name="dirname" id="dirname" /><br/>
            Destination space <select id="cbospace" name="space"/> <a href="#/Admin/Spaces" target="_blank">New space</a><br/>
            <button onclick="btnImportClicked();return false;">Import</button>
            <div id="msg"></div>
        </td>
    </tr>
</table>
</form>

<script language="javascript">
x = null
//jsTree node clicked
function nodeClicked(path) {
    $("#dirname").val(path);
    node = document.getElementById(path)
    $("#demo1").jstree("open_node", node)
}

//Select "appname" value changed
function appChanged()
{
    $("#dirname").val("");
    //Reload spaces
    cboSpace = $('#cbospace');
    var spacelist = $.ajax({
        url: "appserver/rest/ui/editor/listSpaces?appname=" + getCurrentApp(),
        async: false}).responseText;
    spacelist = $.parseJSON(spacelist);
    $.each(spacelist, function(index, spacename) { 
      cboSpace.append($("<option></option>").text(spacename));
    });
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
    	var tree = $("#demo1").jstree({
    		"json_data": {
    			"ajax": {
    				"url": "appserver/rest/ui/editor/listDirsInDir?appname=" + appname,
    				"data": function(n) {
    					return {id: n.attr ? n.attr("id") : "."};
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

function btnImportClicked()
{
    $.ajax({
      url: "appserver/rest/ui/editor/importDir",
      type: "POST",
      data: "appname=" + getCurrentApp() + "&dirname=" + $("#dirname").val(),
      success: importSuccess,
      error: importFail
    });
}

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
