var roles_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var roles={};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value role_desc
function onclick_upload_button() {
    GLOBAL_ACTION = "roles_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

//*************************************************
function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    $('#display_basic_table').DataTable().destroy();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");
    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
     var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td>'+
                '<td><select type="text" class="input form-control" id="roles" name="roles" disabled>'+ roles_type_dropdown +'</select></td>'+
                '<td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="roles_desc"  maxlength="30" style="text-transform:uppercase" required></td>'+
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            else{
                edit_basic_data += '<tr><td><input type="checkbox" required></td>'+
                '<td><select type="text" class="input form-control roles" id="roles-1"  name="roles" onchange="GetSelectedTextValue(this)">'+ roles_type_dropdown +'</select></td>'+
                '<td><input class="input form-control description" id="description-1" value="' + row.cells[2].innerHTML + '" type="text"  name="roles_desc" disabled></td>'+
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
            var roles_type_value = row.cells[1].innerHTML
            dropdown_values.push([roles_type_value])
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
        $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var roletype_value = dropdown_values[i][0]
        $(row.find("TD").eq(1).find("select option[value="+roletype_value+"]")).attr('selected','selected');
        i++;
    });
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#myModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_roles_code").prop("hidden", true);
    $("#id_error_msg_roles_name").prop("hidden", true);
    $("#id_error_msg_roles_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    var getid = $(".roles:last").attr("id");
    var getindex = getid.split("-")[1]
    var inc_index = Number(getindex)+1
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    new_row_data(); // Function for add a new row data
    if (GLOBAL_ACTION == "roles_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_roles_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_roles_data, function (i, item) {
     edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.role + '</td><td>' + item.role_desc + '</td></tr>';
    });
    $('#id_roles_tbody').append(edit_basic_data);
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

//*********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    roles_data = 
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    validate_add_attributes = [];
    var roles = {};
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        roles = {};
        roles.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        roles.role = row.find("TD").eq(1).find('select[type="text"]').val();
        roles.role_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        if (roles == undefined) {
            roles.role = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(roles.role);
        roles_data.push(roles);
    });
    return roles_data;
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.role = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.role);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var roles_arr_obj = {};
        roles_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(roles_arr_obj.del_ind){
            roles_arr_obj.role = row.find("TD").eq(1).html();
            roles_arr_obj.role_desc = row.find("TD").eq(2).html();
            main_table_roles_checked.push(roles_arr_obj);
        }
    });
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html='<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control roles" id="roles-1"  name="role" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ roles_type_dropdown +'</select></td>'+
    '<td><input class="form-control description" type="text"  name="role_desc"  id="description-1" disabled></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}