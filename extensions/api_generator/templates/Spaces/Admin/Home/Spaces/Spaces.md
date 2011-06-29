
<script language='javascript'>
$(document).ready(function(){
    
    $("#confirmdelete").dialog({autoOpen: false,
                                width: 550,
                                modal: true});
    
    $("#spaceform").dialog({autoOpen: false,
            width: 550,
            modal: true});
            
    $("#alert").dialog({
        autoOpen: false,
        width: 400,
        modal: true,
        buttons: {"Ok": function(){
                $(this).dialog("close");
            }}});
    
    var messagealert = function(title, message){
        $dialog = $("#alert");
        $dialog.dialog("option", "title", title);
        $dialog.find("#alertmessage").html(message);
        $dialog.dialog("open");
    };
    
    var confirmdelete = function(options){
        var options = $.extend({space: 'this',
                                ok: $.noop,
                                cancel: $.noop}, options);
        $("#confirmdelete > #space").text(options.space);
        $("#confirmdelete").dialog("option", "buttons", {'Ok': function(){
                                                                options.ok();
                                                                $(this).dialog("close");
                                                                },
                                                         'Cancel': function() {
                                                             options.cancel();
                                                             $(this).dialog("close");
                                                             }
                                                         });
        $("#confirmdelete").dialog("open");
    };
    
    
    
    var remotecall = function(options) {
        var options = $.extend({success: $.noop,
                                error: $.alerterror,
                                data: {}}, options);
                                    
        
        $.ajax({url: options.uri,
                dataType: 'json',
                data: options.data,
                success: options.success,
                error: options.error});
    };
    
    var listspaces = function(options) {
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['listSpaces']});
        remotecall(options);
    };
    
    var deletespace = function(spacename, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['deleteSpace'],
                                        data: {name: spacename}});
        remotecall(options);
    };
    
    var createspace = function(spacename, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['createSpace'],
                                        data: {name: spacename}});
        remotecall(options);
    };
    
    var editspace = function(name, newname, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['updateSpace'],
                                        data: {name: name,
                                               newname: newname}});
        remotecall(options);
    };
    
    var importspace = function(space, path, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['importSpace'],
                                        data: {space: space,
                                               filename: path}});
        remotecall(options);
    };
    
    var exportspace = function(space, path, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['exportSpace'],
                                        data: {space: space,
                                               filename: path}});
        remotecall(options);
    };
    
    console.log("Doing a list spaces call");
    
    var render = function(){
        listspaces({success: function(data){
                                var tbody = $("#spaceslist > tbody");
                                console.log("listspaces succeeded, rendering list...");
                                tbody.empty();
                                $.each(data, function(i, space){
                                    if (space == "Admin") return;
                                    
                                    tbody.append($("<tr>").append($("<td>").append($("<a>", {href: "#/Admin/" + space}).text(space)))
                                                          .append($("<td>").append($('<a>', {style: 'cursor: pointer'}).data('space', space).text('rename').click(function() {
                                                                var space = $(this).data('space');
                                                                $("#spaceform input").removeClass("ui-state-error").val(space);
                                                                $("#spaceform").dialog("option", "title", "Edit Space");
                                                                $("#spaceform").dialog("option", "buttons", {"Rename Space": function(){
                                                                                                            $dialog = $(this);
                                                                                                            $input = $dialog.find("input").removeClass("ui-state-error");
                                                                                                            
                                                                                                            var spacename = $.trim($dialog.find("#name").val());
                                                                                                            if (spacename == ""){
                                                                                                                $input.addClass("ui-state-error");
                                                                                                                return;
                                                                                                            }
                                                                                                            if (space == spacename){
                                                                                                                $dialog.dialog("close");
                                                                                                                return;
                                                                                                            }
                                                                                                            
                                                                                                            editspace(space, spacename, {success: function(){
                                                                                                                $("#space").find("option[value=" + space + "]").attr("value", spacename)
                                                                                                                    .text(spacename);
                                                                                                                    
                                                                                                                render();
                                                                                                                $dialog.dialog("close");
                                                                                                            }, error: $.alerterror});
                                                                                                        },
                                                                                                        
                                                                                                      "Cancel": function(){
                                                                                                          $(this).dialog("close");
                                                                                                        }});
                                                                                
                                                                $("#spaceform").dialog("open");
                                                              })))
                                                          .append($("<td>").append($('<a>', {style: 'cursor: pointer'}).data('space', space).text('delete').click(function(){
                                                                var space = $(this).data('space');
                                                                confirmdelete({space: space,
                                                                         ok: function(){
                                                                             deletespace(space, {success: function(){
                                                                                    $("#space").find("option[value=" + space + "]").remove();
                                                                                    render();
                                                                                 }});
                                                                         }});
                                                              }))));
                                });
                            }});
    };
    
    $("#createspace").button().click(function() {
        $("#spaceform").dialog("option", "title", "Create Space");
        $("#spaceform  input").removeClass("ui-state-error").val("");
        $("#spaceform").dialog("option", "buttons", {"Create Space": function(){
                                                    $dialog = $(this);
                                                    $input = $dialog.find("input").removeClass("ui-state-error");
                                                    
                                                    var spacename = $.trim($dialog.find("#name").val());
                                                    if (spacename == ""){
                                                        $input.addClass("ui-state-error");
                                                        return;
                                                    }
                                                    
                                                    createspace(spacename, {success: function(){
                                                        $("#space").append($("<option>", {'value': spacename}).text(spacename));
                                                        render();
                                                        $dialog.dialog("close");
                                                    }, error: $.alerterror});
                                                },
                                                
                                              "Cancel": function(){
                                                  $(this).dialog("close");
                                                }});
                        
        $("#spaceform").dialog("open");
    });


    render();
});

</script>

<div id='alert'>
<p id='alertmessage'></p>
</div>

<div id='confirmdelete' title='Delete Space'>
    Are you sure you want to delete <b id='space'></b> space?
    <div class='notice' style='margin-top: 25px;'>
    Deleting a space will delete all the pages in that space. There
    is noway to restore it back, so an "export" is adviced.
    </div>
</div>

<div id="spaceform" title="Create new space">
    <form>
    <fieldset>
        <label for="name">Name</label>
        <input type="text" name="name" id="name" class="text ui-widget-content ui-corner-all " />
    </fieldset>
    </form>
</div>

## Spaces

<table id='spaceslist' style='width: 80%;'>
<thead>
    <tr>
        <th style='width: 50%;'>Space</th>
        <th>Rename</th>
        <th>Delete</th>
    </tr>
</thead>
<tbody>
</tbody>
</table>

<button id='createspace'>Create New Space</button>
