
var auth_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var auth={};

//**************************************************
// function corresponding_auth_group(auth_type_val) {
//     corresponding_values = {};
//     corresponding_values.auth_group_dropdown = '';
//     for (var i = 0; i < auth_val_list.length; i++) {
//         compare_dict = {};
//         compare_dict = auth_val_list[i]
//         if (auth_type_val == compare_dict.auth_type) {
//             corresponding_values.auth_group_dropdown += '<option value="' + compare_dict.auth_obj_grp + '">' + compare_dict.auth_obj_grp + '</option>'
//         }
//     }
//     return corresponding_values
// }

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#auth_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_auth_code").prop("hidden", true);
    $("#id_error_msg_auth_name").prop("hidden", true);
    $("#id_error_msg_auth_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    $("#error_msg_id").css("display", "none")
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    new_row_data();   // Add a new row in popup
    if (GLOBAL_ACTION == "auth_upload") {
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    // var auth_type_val = '';
    // $("#id_popup_table TBODY TR").each(function () {
    //     var row = $(this);
    //     row.find("TD").eq(2).find("select").empty()
    //     var assign_val = corresponding_auth_group(auth_type_val)
    //     row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)
    //     $(row.find("TD").eq(1).find("select")).change(function () {
    //         row.find("TD").eq(2).find("select").empty()
    //         var assign_val = corresponding_auth_group(auth_type_val)
    //         row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)
    //     })
    // })
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_auth_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_auth_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.role + '</td><td>' + item.auth_obj_grp + '</td><td hidden>' + item.auth_guid + '</td></tr>';
    });
    $('#id_auth_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    $('#id_check_all').hide();
    table_sort_filter('display_basic_table');
}

//*************************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var auth_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        role = row.find("TD").eq(1).find("select option:selected").val();
        auth_obj_grp = row.find("TD").eq(2).find("select option:selected").val(); 
        checked_box = row.find("TD").eq(1).find('input[type="checkbox"]').is(':checked')
        var compare = auth_obj_grp + '-' + role
        if (auth_code_check.includes(role)) {
            $(row).remove();
        }
        auth_code_check.push(role);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

//************************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#auth_Modal').modal('show');

}

//Onclick of save button 
$('#save_id').click(function () {
    $('#auth_Modal').modal('hide');
    auth_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    var auth = {};
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        auth = {};
        auth.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        auth.role = row.find("TD").eq(1).find("select option:selected").val();
        auth.auth_obj_grp = row.find("TD").eq(2).find("select option:selected").val();
        auth.auth_guid = row.find("TD").eq(3).find('input[type="text"]').val();
        if (auth == undefined) {
            auth.auth_obj_grp = row.find("TD").eq(2).find('input[type="text"]').val();
        }
        if (auth.auth_guid == undefined) {
            auth.auth_guid = ''
        }
        validate_add_attributes.push( auth.auth_obj_grp);
        auth_data.push(auth);
    });
    return auth_data;
}

//****************************************
function onclick_copy_update_button() {
    OpenLoaderPopup();
    $("#error_msg_id").css("display", "none")
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var res = get_all_checkboxes(); // Function to get all the checkboxes
    var $chkbox_all = $('td input[type="checkbox"]', res);
    //Reference the CheckBoxes in Table.
    var edit_basic_data = "";
    var dropdown_values = [];
    dropdown_value();
    //Loop through the CheckBoxes.
    for (var i = 0; i < $chkbox_all.length; i++) {
        if ($chkbox_all[i].checked) {
            var row = $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                guid = row.cells[3].innerHTML;
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><select class="form-control" disable>'+roles_dropdown+'</select></td><td><select class="form-control">'+auth_group_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>'
                var role = row.cells[1].innerHTML
                var auth_obj_grp = row.cells[2].innerHTML
                dropdown_values.push([role, auth_obj_grp])
            }
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var role = dropdown_values[i][0]
        var auth_obj_grp = dropdown_values[i][1]
        $(row.find("TD").eq(1).find("select option[value="+role+"]")).attr('selected','selected');
        $(row.find("TD").eq(2).find("select option[value="+auth_obj_grp+"]")).attr('selected','selected'); 
        i++;
    });
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#auth_Modal').modal('show');
    table_sort_filter('id_popup_table');
    CloseLoaderPopup();
}

// Function for add a new row data
// function new_row_data() {
//     basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">' + roles_dropdown + '</select></td><td><select class="form-control">' + auth_group_dropdown + '</select></td><td hidden><input class="input" type="text"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
//     $('#id_popup_tbody').append(basic_add_new_html);
//     table_sort_filter('id_popup_table');
// }

function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select type="text" class="input form-control roles_dropdon" id="roles_dropdon-1"  name="roles_dropdon" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ roles_dropdown +'</select></td><td><input class="form-control auth_obj_grp" type="text"  name="auth_obj_grp"  id="auth_obj_grp-1" disabled></td><td hidden>guid</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.auth_obj_grp = row.find("TD").eq(1).html();
        main_table_low_value.push( main_attribute.auth_obj_grp);
    });
    table_sort_filter('display_basic_table');
}

 // Function to get the selected row data
 function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var auth_arr_obj = {};
        auth_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(auth_arr_obj.del_ind){
            auth_arr_obj.role = row.find("TD").eq(1).html();
            auth_arr_obj.auth_obj_grp = row.find("TD").eq(2).html();
            auth_arr_obj.auth_guid = row.find("TD").eq(3).html();
            main_table_auth_checked.push(auth_arr_obj);
        }
    });
 }