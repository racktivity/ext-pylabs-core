<link rel=StyleSheet href="/static/lfw/js/libs/jstree/themes/classic/style.css" type="text/css" />




<script type='text/javascript' src='/static/jswizards/ext/jquery.ui.datetimepicker.js'></script>
<script type='text/javascript' src='/static/jswizards/ext/jquery.floatbox.1.0.8.js'></script>
<script type='text/javascript' src='/static/jswizards/js/jswizards.js'></script>
<!-- END js wizard stuff -->

<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.hotkeys.js"/>
<script language="javascript" src="/static/lfw/js/libs/jstree/jquery.jstree.js"/>
<!-- <script language="javascript" src="/static/lfw/js/filetree.js"/> -->

<div id="racktree">
</div>

<script>
$(document).ready(function(){
    var contextmenu = function(item) {
        var type = item.attr("rel");
        var service = "appserver/rest/ui/wizard";
        var domain = "racktivity";
        var actions = [];
        if (type === "enterprise") {
            actions.push({label: "Update",
                          action: function(item){
                              var guid = item.attr("id");
                              JSWizards.launch(service, domain, "enterprise_update", {});
                          }});
                          
        }else if (type === "location"){
            
        }else if (type === "datacenter"){
            
        }else if (type === "floor"){
            
        }else if (type === "room"){
            
        }else if (type === "pod"){
            
        }else if (type === "row"){
            
        }else if (type === "rack"){
            
        }else if (type === "meteringdevice"){
            
        }
        
        actions.push({label: "Delete",
                      separator_before: true,
                      action: function(item){
                          alert("delete");
                      }});
        return actions;
    };
    $("#racktree").jstree({ plugins: ['themes', 'json_data', 'types', 'ui', 'contextmenu', 'crrm'],
                        ui: {
                            select_limit: 1,
                        },
                        types: {
                            types: {enterprise: {icon: {image: '/static/lfw/img/editor/project.png'}},
                                    /* more types should be added for different icons */
                                    file: {icon: {image: '/static/lfw/img/editor/file.png'}},
                                    default: {}}
                        },
                        contextmenu: {
                            items: contextmenu,
                        },
                        json_data: {
                                ajax: { url: 'appserver/rest/ui/portal/getNode',
                                        data: function(n) {
                                            return {id: n.attr ? n.attr("rel") + ":" + n.attr("id") : "."};
                                        }},
                            progressive_render : true
                            },
                        themes: {theme : "classic"},
                    });
});

</script>
