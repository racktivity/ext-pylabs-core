
<script language='javascript'>
$(document).ready(function(){
    
    /**
    Note To Klaas:
    I am thinking of using jquery accordion as data grid for our entities as following
    
    Users:
    =========================================
    |Azmy                                   |
     ---------------------------------------
    | [Edit] [Delete]                       |
    | Groups:                               |
    |  -----------------------------------  |
    | | Group 1 |     unassing            | | 
    | | Group 2 |     unassing            | |
    |  -----------------------------------  |
    | [Assign group]                        |
    =========================================
    |Klaas                                  |
    =========================================
    ...
    
    - Also for rules
    
    Rules:
    =========================================
    |Admin                                  |
     ---------------------------------------
    | [Edit] [Delete]                       |
    | [function ... ]   <change>            |
    | [context  ... ]   <change>            |
    |                                       |
    | Groups:                               |
    |  -----------------------------------  |
    | | Group 1 |     <remove>            | | 
    | | Group 2 |     <remove>            | |
    |  -----------------------------------  |
    | [Add group]                           |
    =========================================
    |Rule2                                  |
    =========================================
    ...
    
    - Groups can be a normal table where group can only have name.
    
    - So I starting by creating an Accordion class where you can dynamically
    add/delete panels from it (I have tested this).
    
    - I started working on a UserPanel class (but I had to go home before I do much with it :P ... good luck ;) )
    - Also a RulePanel needs to be created
    
    - The idea is when you first load the page you use the lfw service to get the needed data which is enough to build
    - your views. and handle acctions to 
    
    
    When you load this page you will get a demo of what I think it should look like.
    
    Feel free to drop this entirly if you think it's not good enough or if you have a better idea.
    
    START OF DEMO
    */
    var Accordion = function(parent){
        
        var body = $("<div>").accordion();
        
        var tmpl = "<h3 class='accordion-header' id='${name}'><a href='#'>${name}</a></h3>" +
                    "<div class='accordion-panel'></div>";
        
        this.exists = function(name){
            return body.find("#" + name).length > 0;
        };
        
        this.add = function(name, panel) {
            if (!this.exists(name)){
                var item = $.tmpl(tmpl, {name: name});
                item.filter(".accordion-panel")
                    .append(panel);
                    
                body.accordion("destroy")
                    .append(item)
                    .accordion();
                
            }
        };
        
        this.delete = function(name) {
            var item = body.accordion("destroy")
                .find("#" + name);
            
            if (item.length > 0){
                item.next().remove();
                item.remove();
            }
            
            body.accordion();
        };
        
        this.getDom = function(){
            return body;
        };
        
        if (parent){
            this.appendTo(parent);
        }
    };
    
    var UserPanel = function(userid) {
        
        var body = $("#user-panel").tmpl();
        body.find("button").button();
        
        var that = this;
        
        body.find(".user-edit").click(function(e){
            alert("Edit user: " + that.userid());
        });
        
        body.find(".user-delete").click(function(e){
            alert("Edit Delete: " + that.userid());
        });
        
        body.find(".user-assign").click(function(e){
            alert("Assign group: " + that.userid());
        });
        
        this.userid = function(id){
            if (id === undefined){
                return body.data("userid");
            } else {
                body.data("userid", id);
            }
        };
        
        this.getDom = function(){
            return body;
        };
        
        if(userid){
            this.userid(userid);
        }
    };
    
    var acc = new Accordion();
    $("#test").append(acc.getDom());
    acc.add("Azmy", new UserPanel("Azmy").getDom());
    acc.add("Klaas", new UserPanel("Klaas").getDom());
    
    /**
    END OF DEMO.
    */
    

    $("#userform").dialog({autoOpen: false,
            width: 550,
            modal: true});

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
                                                          .append($("<td>").append($('<a>', {style: 'cursor: pointer'}).data('user', user).text('change password').click(function() {

                                                                var user = $(this).data('user');
                                                                $("#userform input").removeClass("ui-state-error").val('');
                                                                $("#userform").find("#name").attr("disabled", true).val(user);
                                                                var $dialog = $("#userform").dialog("option", "title", "Edit User");
                                                                $("#userform").dialog("option", "buttons", {"Change Password": function(){
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
                                                                $("#userform").keydown(function(e) {
                                                                    if (e.keyCode == 13) {
                                                                        var buttons = $( "#userform" ).dialog( "option", "buttons" );
                                                                        var button = buttons["Change Password"];
                                                                        button();
                                                                    }
                                                                });
                                                              })))
                                                          .append($("<td>").append($('<a>', {style: 'cursor: pointer'}).data('user', user).text('delete').click(function(){
                                                                var user = $(this).data('user');
                                                                $.confirm("Are you sure you want to delete user '" + user + "'?", {title: "Delete User",
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
        var $dialog = $("#userform").dialog("option", "title", "Create User");
        $("#userform").find("#name").attr("disabled", false);
        $("#userform  input").removeClass("ui-state-error").val("");
        $("#userform").dialog("option", "buttons", {"Create User": function(){
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

        $("#userform").keydown(function(e) {
            if (e.keyCode == 13) {
                var buttons = $( "#userform" ).dialog( "option", "buttons" );
                var button = buttons["Create User"];
                button();
            }
        });
    });


    render();
});

</script>

<div id='test'>
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

<script id='user-panel' type='text/x-jquery-tmpl'>
    <div>
        <button class='user-edit'>Edit</button>
        <button class='user-delete'>Delete</button>
        <table style='margin-top: 5px; margin-buttom: 5px;'>
            <thead>
                <tr>
                    <th>Group Name</th>
                    <th>Unassign</th>
                </tr>
            </thead>
            <tbody class='user-groups'>
            </tbody>
        </table>
        <button class='user-assign'>Assign Group</button>
    </div>
</script>
