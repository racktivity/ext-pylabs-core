<link rel=StyleSheet href="/static/lfw/js/libs/jstree/themes/classic/style.css" type="text/css" />
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.jstree.js"/>

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
            <!-- Destination space <select id="cbospace" name="space"/> <a href="#/Admin/Spaces" target="_blank">New space</a><br/> -->
            Project name <input type="text" name="projectname" id="projectname" /><br/>
            <button onclick="btnImportClicked();">Import</button>
            <div id="msg"></div>
        </td>
    </tr>
</table>
<h4><a href="./#/Imported/Home">Imported projects</a></h4>

<script language="javascript">

function nodeSelected(event, data) {
    path = data.inst._get_node().attr("id");
    data.inst.open_node()
    $("#dirname").val(path);
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
            "ui": {
                "select_limit":1
            },
            "themes" : {
               "theme" : "classic",
            },
    		"plugins": ["themes", "json_data", "ui"]
    	});
        tree.bind("select_node.jstree", nodeSelected);
};

function btnImportClicked()
{
    $.ajax({
      url: "appserver/rest/ui/editor/importProject",
      type: "POST",
      data: "appname=" + getCurrentApp() + "&source=" + $("#dirname").val() + "&projectname=" + $("#projectname").val(),
      success: importSuccess,
      error: importFail
    });
}

function importSuccess(data)
{
    alert("Porject has been imported successfully\nPlease click on 'Imported projects' link below to see your project");
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
