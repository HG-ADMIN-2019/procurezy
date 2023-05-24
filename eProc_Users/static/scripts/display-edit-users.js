$(document).ready(function(){
    $("#supplier_form_reset").click(function(){
        $('#configform')[0].reset();
        $('#myModal').modal('hide');
    });
//    set_value();
    get_values();
    $('#nav_menu_items').remove();
    $("body").css("padding-top", "4rem");
});

// Function to make user basic data field editable
function edit_user_basic_info() {
    $('#user_basic_update_success').hide();
    $(".hg_edit_display_mode").prop("disabled", false);
    $("#id_language_id").append(language_opt)
    $("#id_currency_id").append(currency_opt)
    $("#id_time_zone").append(timezone_opt)
    $("#decimal_notation").append(decimal_opt)
    $("#date_format").append(date_format_opt)
    document.getElementById("edit_user_info_btn").style.display = "none"
    document.getElementById("save_cancel_user_info_btn").style.display = "block"
}

// Onlick cancel edit user-basic data 
function cancel_user_basic_info() {
    $(".hg_edit_display_mode").prop("disabled", true);
    document.getElementById("edit_user_info_btn").style.display = "block"
    document.getElementById("save_cancel_user_info_btn").style.display = "none"
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

    // Funtion to save basic detail data
    function save_user_basic_info() {
     var name1_val= $('#first_name').val();
     var phone_num_val = $('#phone_num').val();
     var email_val = $('#email').val();
     var err_flag;
     set_value();
     OpenLoaderPopup();
      is_save_form_valid = save_user_form_validation()
        if (is_save_form_valid) {
            var user_data_dict = {}

        user_data_dict.username = $('#username').val();
        user_data_dict.first_name = $('#first_name').val();
        user_data_dict.last_name= $('#last_name').val();
        user_data_dict.employee_id= $('#employee_id').val();
        user_data_dict.user_type= $('#user_type').val();
        user_data_dict.language_id= $('#id_language_id').val();
        user_data_dict.currency_id=$('#id_currency_id').val();
        user_data_dict.time_zone= $('#id_time_zone').val();
        user_data_dict.email= $('#email').val();
        user_data_dict.phone_num= $('#phone_num').val();
        user_data_dict.date_format= $('#date_format').val();
        user_data_dict.decimal_notation= $('#decimal_notation').val();
        user_data_dict.login_attempts= $('#login_attempts').val();
        user_data_dict.super_user= $('#super_user').prop('checked');
        user_data_dict.user_locke= $('#user_locked').prop('checked');
        user_data_dict.pwd_locked= $('#pwd_locked').prop('checked');

        ajax_update_user_basic_data(user_data_dict)

        document.getElementById('user_basic_update_success').innerHTML = "Saved Successfully";
          $('#save_error_div').hide()
        $('#user_basic_update_success').show();
        $('html, body').animate({ scrollTop: 0 }, 'slow');
        cancel_user_basic_info();
        CloseLoaderPopup();
        }
        else{
            $('#language_id').val(localStorage.getItem("language_id"));
            get_values();
        }

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
                if(temp[i].value == ''){
                    err_text1 = temp[i].parentNode.children[0].innerHTML;
                    $('#temp[i].nextElementSibling.id').prop('hidden', false);
                    $('#temp[i].nextElementSibling.id').html("required");
                    document.getElementById(temp[i].nextElementSibling.id).innerHTML = err_text1 + " required";
                    is_valid = false;
                }
                else{ $('#temp[i].nextElementSibling.id').prop('hidden', true);
                    $(".error_message").prop("hidden", true);
                }
            }
            else{
                if(temp[i].value == ''){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    temp[i].nextElementSibling.innerHTML = err_text + " required";
                   is_valid = false;
                }
            }
        }
        return is_valid
    }

