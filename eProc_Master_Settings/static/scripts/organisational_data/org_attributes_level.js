var org_attr_level_data = new Array();
var validate_add_attributes = [];
var org_attr_level = {};
var main_table_low_value = [];

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#org_attr_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_org_attr_code").prop("hidden", true);
    $("#id_error_msg_org_attr_name").prop("hidden", true);
    $("#id_error_msg_org_attr_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//*************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#org_attr_Modal').modal('show');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#org_attr_Modal').modal('hide');
    org_attr_level_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    validate_add_attributes = [];
    duplicate_entry = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        org_attr_level.node_type = row.find("TD").eq(1).find('select').val();
        org_attr_level.node_values = row.find("TD").eq(2).find('select').val();
        org_attr_level.org_model_nodetype_config_guid = row.find("TD").eq(3).find('input').val();
        org_attr_level.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        if (org_attr_level == undefined) {
            org_attr_level.node_type = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        if(org_attr_level.org_model_nodetype_config_guid == undefined) {
            org_attr_level.org_model_nodetype_config_guid = '';
        }
        var compare = org_attr_level.node_type + '-' + org_attr_level.node_values
        validate_add_attributes.push(compare);
        org_attr_level_data.push(org_attr_level);
    });
    return org_attr_level_data;
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    $("#error_msg_id").css("display", "none")
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html(" ");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+nodetype_dropdown+'</select></td><td><select class="form-control">'+attributelevel_id_dropdown+'</select></td><td hidden>pgroup_guid</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "org_attr_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var org_attr_arr_obj = {};
        org_attr_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(org_attr_arr_obj.del_ind){
            org_attr_arr_obj.node_type = row.find("TD").eq(1).html();
            org_attr_arr_obj.node_values = row.find("TD").eq(2).html();
            org_attr_arr_obj.org_model_nodetype_config_guid = row.find("TD").eq(3).html();
            org_attr_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
            main_table_org_attrlevel_checked.push(org_attr_arr_obj);
        }
    });
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+nodetype_dropdown+'</select></td><td><select class="form-control">'+attributelevel_id_dropdown+'</select></td><td hidden>pgroup_guid</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.node_type = row.find("TD").eq(1).html();
        main_attribute.node_values = row.find("TD").eq(2).html();
        var compare_maintable = main_attribute.node_type + '-' + main_attribute.node_values
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter('display_basic_table');
}