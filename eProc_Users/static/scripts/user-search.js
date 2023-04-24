 // Script to generate sort and filter feature for tables
 $(document).ready( function() {
   nav_bar_admin();
   $('#username').val(localStorage.getItem("username"));
   $('#first_name').val(localStorage.getItem("first_name"));
   $('#last_name').val(localStorage.getItem("last_name"));
   $('#email').val(localStorage.getItem("email"));
   $('#user_type').val(localStorage.getItem("user_type"));
   $('#employee_id').val(localStorage.getItem("employee_id"));
//   $('#user_locked_id').val(localStorage.getItem("user_locked"));
//   $('#pwd_locked_id').val(localStorage.getItem("pwd_locked"));
//   $('#is_active_id').val(localStorage.getItem("is_active"));
   const form = document.getElementById("search_form");
//   form.addEventListener("submit", validateForm);
   table_sort_filter_basic("table_sort_filter_basic")
});

function validateForm(event) {
    var temp = $('#username').val();
    if($('#username').val() == ''){
        if($('#first_name').val() == ''){
            if($('#last_name').val() == ''){
                $('#error_message_search').text("Please enter Username or First name or Last name");
                document.getElementById("error_message_search").style.color = "Red";
                $("#error_msg").css("display", "block")
                CloseLoaderPopup();
                event.preventDefault();
                return false;
            }
        }
    }
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "employee_upload"
  //  $("#user_tab_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}