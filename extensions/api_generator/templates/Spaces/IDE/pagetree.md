<link rel=StyleSheet href="/static/lfw/js/libs/jstree/themes/classic/style.css" type="text/css" />
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.jstree.js"/>
<!-- <script language="javascript" src="/static/lfw/js/filetree.js"/> -->

<div id="tree">
</div>

<script>

$(document).ready(function() {
    var METHODS = {getnode: "getNode",
               getfile: "getFile",
               setfile: "setFile",
               newfile: "newFile",
               newdir:  "newDir",
               del: "delete",
               rename: "rename"};
               
    var remotecall = function(method, options) {
        var options = $.extend({success: $.noop,
                                error: $.alerterror,
                                data: {}}, options);
                                
        $.ajax({url: 'appserver/rest/ui/ide/' + method,
                type: 'POST',
                dataType: 'json',
                data: options.data,
                success: options.success,
                error: options.error});
    };
    
    var openedfiles = {};
    var generateid = function() {
        return Math.floor(Math.random() * 100000000);
    };
    
    var createNewFile = function(item) {
        var id = item.attr("id");
        var tree = this;
        $.prompt("New file Name ?", {title: "Create new file",
                                     pattern: /.+/,
                                     error: "File name can't be empty",
                                     ok: function(name) {
                                        var fid = id + "/" + name;
                                        remotecall(METHODS.newfile, {data: {id: fid},
                                            success: function() {
                                                tree.create(item, "last", {data: name,
                                                                           state: 'leaf',
                                                                           attr: {id: fid, rel: 'file'}},
                                                                        $.noop,
                                                                        true);
                                            }});
                                    }});
    };
    
    var createNewDir = function(item) {
        var id = item.attr("id");
        var tree = this;
        $.prompt("New directory Name ?", {title: "Create new directory",
                                     pattern: /.+/,
                                     error: "Directory name can't be empty",
                                     ok: function(name) {
                                        var fid = id + "/" + name;
                                        remotecall(METHODS.newdir, {data: {id: fid},
                                            success: function() {
                                                tree.create(item, "first", {data: name,
                                                                           state: 'leaf',
                                                                           attr: {id: fid}},
                                                                        $.noop,
                                                                        true);
                                            }});
                                    }});
    };
    
    var deleteItem = function(item){
        var id = item.attr("id");
        var type = item.attr("rel") == "file" ? "file" : "folder";
        var tree = this;
        $.confirm("Are you sure you want to delete this " + type + "?", {title: "Delete " + type,
                                     ok: function(name) {
                                        remotecall(METHODS.del, {data: {id: id},
                                            success: function(){
                                                tree.remove(item);
                                            }});
                                    }});
    };
    
    var rename = function(item){
        var id = item.attr("id");
        var tree = this;
        
        $.prompt("New Name ?", {title: "Rename",
                                 value: tree.get_text(item),
                                 pattern: /.+/,
                                 error: "New name can't be empty",
                                 ok: function(name) {
                                    remotecall(METHODS.rename, {data: {id: id, name: name},
                                        success: function() {
                                            console.log(item);
                                            tree.rename_node(item, name);
                                            var m = /(.+)\/[^\/]+$/.exec(id);
                                            if (!m){
                                                $.alert("Failed to update node ID");
                                            }
                                            item.attr("id", m[1] + "/" + name);
                                            tree.refresh(item);
                                        }});
                                }});
    };
    var contextmenu = function(item) {
        var type = item.attr("rel");
        if (type === undefined) type = "folder";
        
        var actions = [];
        
        if (type === "folder" || type === "project") {
            actions.push({label: "Create New File",
                          action: createNewFile});
            actions.push({label: "Create New Directory",
                          action: createNewDir,
                          separator_after: true});
        }
        
        if (type === "file" || type === "folder") {
            actions.push({label: "Rename",
                        action: rename,
                        separator_after: true});
            actions.push({label: "Delete",
                          action: deleteItem});
        }
        
        return actions;
    };
    
    $("#tree").jstree({ plugins: ['themes', 'json_data', 'types', 'ui', 'contextmenu', 'crrm'],
                        ui: {
                            select_limit: 1,
                        },
                        types: {
                            types: { project: {icon: {image: '/static/lfw/img/editor/project.png'}},
                                     file: {icon: {image: '/static/lfw/img/editor/file.png'}},
                                     default: {}}
                        },
                        contextmenu: {
                            items: contextmenu,
                        },
                        json_data: {
                                ajax: { url: 'appserver/rest/ui/ide/getNode',
                                        data: function(n) {
                                            return {id: n.attr ? n.attr("id") : "."};
                                        }},
                            progressive_render : true
                            },
                        themes: {theme : "classic"},
                    });
    
    $(".jstree-leaf").die("dblclick").live("dblclick", function(e){
        if ($(this).attr("rel") !== "file")
            return;
        
        var fileid = $(this).attr("id");
        if (fileid in openedfiles){
            //give focus to file.
            var id = openedfiles[fileid];
            $("#editortabs").tabs("select", "#" + id);
        } else {
            var id = generateid();
            var m = /([^\/]+)$/.exec(fileid);
            if (!m) {
                console.log("Can't extract the file name");
                return;
            }
            var filename = m[1];
            openedfiles[fileid] = id;
            $("#editortabs").tabs("add", "#" + id, filename);
            $("#editortabs").tabs("select", "#" + id);
            
            remotecall(METHODS.getfile, {data: {id: fileid},
                        success: function(data){
                            var editor = $("#editortabs").find("#" + id).data("original", data).editor({editorbar:false});
                            editor.editor("filetype", "py");
                            editor.editor("content", data);
                        }});
        }
        
    });
    
    $("#editortabs span.ui-icon-close" ).live( "click", function() {
        var tab = $(this).parent("li");
        var hashid = tab.find("a").attr("href");
        var id = hashid.replace("#", "");
        var editor = $(hashid);
        
        var _close = function(){
            console.log("Closing");
            $.each(openedfiles, function(k, v){
                if (v == id){
                    delete openedfiles[k];
                }
            });
            
            var index = $("li", $("#editortabs")).index(tab);
            $("#editortabs").tabs("remove", index );
        };
        
        if (editor.data("original") != editor.editor("content")) {
            $.confirm("Close without saving?",
                {title: "Confirm Close",
                ok: function() {
                    _close();
                }});
        } else {
            _close();
        }
    });
    
    $("#editortabs span.ui-icon-note" ).live( "click", function() {
        var tab = $(this).parent("li");
        var hashid = tab.find("a").attr("href");
        var id = hashid.replace("#", "");
        var editor = $(hashid);
        var fileid = null;
        $.each(openedfiles, function(k, v){
            if (v == id) {
                fileid = k;
            }
        });
        
        if (!fileid){
            $.alert("Can't get the file id back, it sounds like a serious issue!", {title: "Save Error"});
            return;
        }
        
        remotecall(METHODS.setfile,
            {data: {id: fileid,
                    content: editor.editor("content")},
            success: function(){
                editor.data('original', editor.editor("content"));
            }
            });
    });
    
});
</script>
