
// Function to make user basic data field editable
function edit_user_basic_info() {
    $('#user_basic_update_success').hide();
    $(".hg_edit_display_mode").prop("disabled", false);
    if(GLOBAL_ACTION != 'CREATE'){
        $('#username').prop("disabled", true);
        $('#employee_id').prop("disabled", true);
        $('#user_type').prop("disabled", true);
        $('#email').prop("disabled", true);
        $('#login_attempts').prop("disabled", true);
        $("#cancel_button").prop("hidden", false);
        $("#save_user_info_btn").prop("hidden", false);
    }
    document.getElementById("edit_user_info_btn").style.display = "none";
    document.getElementById("save_user_info_btn").style.display = "block";
    document.getElementById("cancel_button").style.display = "block";
}

// Onlick cancel edit user-basic data 
function cancel_user_basic_info() {
    $(".hg_edit_display_mode").prop("disabled", true);
    document.getElementById("edit_user_info_btn").style.display = "block"
    document.getElementById("save_user_info_btn").style.display = "none";
    document.getElementById("cancel_button").style.display = "none";
}

function set_value(){
     localStorage.setItem("currency_id", document.getElementById("id_currency_id").value);
     localStorage.setItem("language_id", document.getElementById("id_language_id").value);
     localStorage.setItem("time_zone", document.getElementById("id_time_zone").value);
}
function get_values(){
    $('#id_currency_id').val(localStorage.getItem("currency_id"));
   $('#id_language_id').val(localStorage.getItem("language_id"));
    $('#id_time_zone').val(localStorage.getItem("time_zone"));
}


// Validation function
function save_user_form_validation(){
   var is_valid = true;
        var save_form_errors = ''
        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

        var err_text1 = '';
        var temp = document.getElementsByClassName('mandatory_fields');
        for (var i = 0; i<temp.length; i++) {
            if(temp[i].nodeName == "SELECT"){
                if((temp[i].value == '') || (temp[i].value == null)){
                    err_text1 = temp[i].parentNode.children[0].innerHTML;
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    $('#temp[i].nextElementSibling.id').html("required");
                    document.getElementById(temp[i].nextElementSibling.id).innerHTML = err_text1 + " required";
                    is_valid = false;
                }
                else{ $('#temp[i].nextElementSibling.id').prop('hidden', true);
                }
            }
            else{
                if(temp[i].value == ''){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    temp[i].nextElementSibling.innerHTML = err_text + " required";
                   is_valid = false;
                }
                 else if(temp[i].value.length < 3){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    document.getElementById(display_id).style.display = "block";
                    temp[i].nextElementSibling.innerHTML = "Please enter min 3 chars for "+ err_text;
                    $('#'+temp[i].id).prop("disabled", false);
                   is_valid = false;
                }
                if(temp[i].id == 'email_id'){
                    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                     if (!(temp[i].value).match(mailformat)) {
                            valid_data = false
                             var msg = "JMSG002";
                             var msg_type ;
                             msg_type = message_config_details(msg);
                             var display1 = msg_type.messages_id_desc;
                             $(".error_message").prop("hidden", false);
                            var display_id = temp[i].nextElementSibling.id;
                            $('#'+display_id).prop('hidden', false);
                            document.getElementById(display_id).style.display = "block";
                            temp[i].nextElementSibling.innerHTML = display1 + " for Email Id";
                           is_valid = false;
                     }
                }
                if(temp[i].id == 'phone_num'){
                     if (temp[i].value.length != 10) {
                            valid_data = false
                             var msg = "JMSG002";
                             var msg_type ;
                             msg_type = message_config_details(msg);
                             var display1 = msg_type.messages_id_desc;
                             $(".error_message").prop("hidden", false);
                            var display_id = temp[i].nextElementSibling.id;
                            $('#'+display_id).prop('hidden', false);
                            document.getElementById(display_id).style.display = "block";
                            temp[i].nextElementSibling.innerHTML = display1 + " for Mobile Number";
                           is_valid = false;
                     }
                }
            }
        }
        return is_valid
    }

