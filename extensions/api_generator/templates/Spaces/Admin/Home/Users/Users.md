
<script language='javascript'>
$(document).ready(function(){
    
    $("#confirmdelete").dialog({autoOpen: false,
                                width: 550,
                                modal: true});
    
    $("#userform").dialog({autoOpen: false,
            width: 550,
            modal: true});
    
    var confirmdelete = function(options){
        var options = $.extend({user: 'this',
                                ok: $.noop,
                                cancel: $.noop}, options);
        $("#confirmdelete > #user").text(options.user);
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
    
    var listusers = function(options) {
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['users']});
        remotecall(options);
    };
    
    var deleteuser = function(username, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['deleteUser'],
                                        data: {name: username}});
        remotecall(options);
    };
    
    var createuser = function(username, passwd, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['createUser'],
                                        data: {name: username,
                                               password: passwd}});
        remotecall(options);
    };
    
    var edituser = function(username, passwd, options){
        var options = $.extend(options, {uri: LFW_CONFIG['uris']['updateUser'],
                                        data: {name: username,
                                               password: passwd}});
        remotecall(options);
    };
    
    var render = function(){
        listusers({success: function(data){
                                var tbody = $("#userslist > tbody");
                                console.log("listusers succeeded, rendering list...");
                                tbody.empty();
                                console.log(data);
                                $.each(data, function(i, user){
                                    tbody.append($("<tr>").append($("<td>").text(user))
                                                          .append($("<td>").append($('<a>', {style: 'cursor: pointer'}).data('user', user).text('Change Password').click(function() {
                                                                
                                                                var user = $(this).data('user');
                                                                $("#userform input").removeClass("ui-state-error").val('');
                                                                $("#userform").find("#name").attr("disabled", true).val(user);
                                                                $("#userform").dialog("option", "title", "Edit User");
                                                                $("#userform").dialog("option", "buttons", {"Change Password": function(){
                                                                                                            
                                                                                                            $dialog = $(this);
                                                                                                            $input = $dialog.find("input").removeClass("ui-state-error");
                                                                                                            var passwd = $.trim($dialog.find("#password").val());
                                                                                                            var cpasswd = $.trim($dialog.find("#cpassword").val());
                                                                                                            
                                                                                                            if (!passwd) {
                                                                                                                $dialog.find("#password").addClass("ui-state-error");
                                                                                                                $.alert("Password is required", {title: "Validation Error"});
                                                                                                                return;
                                                                                                            }
                                                                                                            
                                                                                                            if (passwd != cpasswd) {
                                                                                                                $dialog.find("#cpassword").addClass("ui-state-error");
                                                                                                                $.alert("Passwords don't match", {title: "Validation Error"});
                                                                                                                return;
                                                                                                            }
                                                                                                            
                                                                                                            edituser(user, passwd, {success: function() {
                                                                                                                $.alert("Password updated successfully", {title: 'Password Changed'});
                                                                                                                $dialog.dialog("close");
                                                                                                            }, error: $.alerterror});
                                                                                                            
                                                                                                        },
                                                                                                        
                                                                                                      "Cancel": function(){
                                                                                                          $(this).dialog("close");
                                                                                                        }});
                                                                                
                                                                $("#userform").dialog("open");
                                                                
                                                              })))
                                                          .append($("<td>").append($('<a>', {style: 'cursor: pointer'}).data('user', user).text('delete').click(function(){
                                                                var user = $(this).data('user');
                                                                confirmdelete({user: user,
                                                                         ok: function(){
                                                                             deleteuser(user, {success: function(){
                                                                                    render();
                                                                                 }});
                                                                         }});
                                                              }))));
                                });
                            }});
    };
    
    $("#createuser").button().click(function() {
        $("#userform").dialog("option", "title", "Create User");
        $("#userform").find("#name").attr("disabled", false);
        $("#userform  input").removeClass("ui-state-error").val("");
        $("#userform").dialog("option", "buttons", {"Create User": function(){
                                                    $dialog = $(this);
                                                    
                                                    $dialog.find("input").removeClass("ui-state-error");
                                                    var username = $.trim($dialog.find("#name").val());
                                                    var passwd = $.trim($dialog.find("#password").val());
                                                    var cpasswd = $.trim($dialog.find("#cpassword").val());
                                                    
                                                    if (username == "") {
                                                        $dialog.find("#name").addClass("ui-state-error");
                                                        $.alert("Name is required", {title: "Validation Error"});
                                                        return;
                                                    }
                                                    
                                                    if (!passwd) {
                                                        $dialog.find("#password").addClass("ui-state-error");
                                                        $.alert("Password is required", {title: "Validation Error"});
                                                        return;
                                                    }
                                                    
                                                    if (passwd != cpasswd) {
                                                        $dialog.find("#cpassword").addClass("ui-state-error");
                                                        $.alert("Passwords don't match", {title: "Validation Error"});
                                                        return;
                                                    }
                                                    
                                                    createuser(username, passwd, {success: function() {
                                                        render();
                                                        $dialog.dialog("close");
                                                    }, error: $.alerterror});
                                                },
                                              "Cancel": function() {
                                                  $(this).dialog("close");
                                                }});
                        
        $("#userform").dialog("open");
    });


    render();
});

</script>

<div id='confirmdelete' title='Delete User'>
    Are you sure you want to delete user <b id='user'></b>?
</div>

<div id="userform" title="Create new user">
    <form>
    <fieldset>
        <div>
            <label for="name">Name</label>
            <input type="text" id="name" class="text ui-widget-content ui-corner-all " />
        </div>
        <div>
            <label for="password" >Password</label>
            <input type="password" id="password" class="text ui-widget-content ui-corner-all " />
        </div>
        <div>
            <label for="cpassword">Confirm Password</label>
            <input type="password" id="cpassword" class="text ui-widget-content ui-corner-all " />
        </div>
    </fieldset>
    </form>
</div>

## Users

<table id='userslist' style='width: 80%;'>
<thead>
    <tr>
        <th style='width: 50%;'>User</th>
        <th>Edit</th>
        <th>Delete</th>
    </tr>
</thead>
<tbody>
</tbody>
</table>

<button id='createuser'>Create New User</button>
