var auth_group_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var auth_group={};

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_auth_group_code").prop("hidden", true);
    $("#id_error_msg_auth_group_name").prop("hidden", true);
    $("#id_error_msg_auth_group_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_auth_group_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_auth_group_data, function(i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.auth_obj_grp + '</td><td>' + item.auth_grp_desc + '</td><td>' + item.auth_level + '</td><td>' + item.auth_obj_id + '</td><td hidden>' + item.auth_grp_guid + '</td></tr>';
    });
    $('#id_auth_group_tbody').append(edit_basic_data);
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

//**********************************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var auth_group_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        auth_obj_grp = row.find("TD").eq(1).find("select option:selected").val();
        auth_obj_id = row.find("TD").eq(4).find("select option:selected").val();
        auth_grp_desc = row.find("TD").eq(2).find("select option:selected").val().toUpperCase();
        auth_level = row.find("TD").eq(3).find("select option:selected").val();
        var compare = auth_obj_grp+'-'+auth_grp_desc+'-'+auth_obj_id+'-'+auth_level
        if (auth_group_code_check.includes(compare)) {
            $(row).remove();
        }
        auth_group_code_check.push(compare);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

//**********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');
}

// Onclick of save button in popup
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    auth_group_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    var auth_group = {};
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var row = $(this);
        auth_group = {};
        auth_group.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        auth_group.auth_obj_grp = row.find("TD").eq(1).find('select[type="text"]').val();
        auth_group.auth_grp_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        auth_group.auth_level = row.find("TD").eq(3).find("select option:selected").val();
        auth_group.auth_obj_id = row.find("TD").eq(4).find("select option:selected").val();
        auth_group.auth_grp_guid = row.find("TD").eq(5).find('input[type="text"]').val();
        if (auth_group == undefined) {
            auth_group.auth_obj_grp = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        if (auth_group.auth_grp_guid == undefined) {
            auth_group.auth_grp_guid = ''
        }
        var compare = auth_group.auth_obj_grp + ' - ' + auth_group.auth_grp_desc + ' - ' + auth_group.auth_level+ ' - ' + auth_group.auth_obj_id
        validate_add_attributes.push(compare);
        auth_group_data.push(auth_group);
    });
    return auth_group_data;
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.auth_obj_grp = row.find("TD").eq(1).html();
        main_attribute.auth_grp_desc = row.find("TD").eq(2).html().toUpperCase();
        main_attribute.auth_level = row.find("TD").eq(3).html();
        main_attribute.auth_obj_id = row.find("TD").eq(4).html();
        var main_attribute_compare = main_attribute.auth_obj_grp + ' - ' + main_attribute.auth_grp_desc + ' - ' + main_attribute.auth_level + ' - ' + main_attribute.auth_obj_id
        main_table_low_value.push(main_attribute_compare);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var auth_group_arr_obj = {};
        auth_group_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if( auth_group_arr_obj.del_ind) {
        auth_group_arr_obj.auth_obj_grp = row.find("TD").eq(1).html();
        auth_group_arr_obj.auth_obj_id = row.find("TD").eq(4).html();
        auth_group_arr_obj.auth_grp_desc = row.find("TD").eq(2).html().toUpperCase();
        auth_group_arr_obj.auth_level = row.find("TD").eq(3).html();
        auth_group_arr_obj.auth_grp_guid = row.find("TD").eq(5).html();
        auth_group_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        main_table_auth_group_checked.push(auth_group_arr_obj);
        }
    });
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control authgroup"  id="authgroup-1" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ auth_group_id_dropdown+'</select></td>'+
    '<td><input class="form-control description" type="text"  name="description"  id="description-1" disabled></td>'+
    '<td><select class="form-control">'+auth_level_dropdown+'</select></td>'+
    '<td><select class="form-control">'+auth_obj_id_dropdown+'</select></td>'+
    '<td hidden><input type="text" value="GUID"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}