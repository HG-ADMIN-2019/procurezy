var orgnodetyp_data = new Array();
var validate_add_attributes = [];
var org_node_type = {};

// on click Delete icon
function onclick_delete_button() {
    GLOBAL_ACTION = "DELETE";
    $('#delete_data').show();
    $('#save_id').hide();
    onclick_copy_update_button("DELETE");
}

//**********************************************************
function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var res = get_all_checkboxes(); // Function to get all the checkboxes
    var $chkbox_all = $('td input[type="checkbox"]', res);
    //Reference the CheckBoxes in Table.
    var edit_basic_data = "";
    var unique_input = '';
    var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 0; i < $chkbox_all.length; i++) {
        if ($chkbox_all[i].checked) {
            var row = $chkbox_all[i].parentNode.parentNode;
             if (GLOBAL_ACTION == "DELETE"){
                if ((row.cells[4].innerHTML=="False") || (row.cells[4].innerHTML=="false")){
                    check = '<input type="checkbox" disabled>'
                    document.getElementById('delete_data').style.visibility='visible';
                     $('#save_id').hide();
                    $('#delete_data').prop('disabled', true);
                }
                else
                {
                    check = '<input type="checkbox">'
                    document.getElementById('delete_data').style.visibility = 'visible'
                    $('#delete_data').prop('disabled', false);
                }
                var node_type = row.cells[1].innerHTML;
                var node_type_desc = row.cells[2].innerHTML;
                dropdown_values.push([node_type, node_type_desc])
                guid = row.cells[3].innerHTML;
                unique_input = '<input type="text" class="input form-control"  value="' + row.cells[1].innerHTML + '" id="nodetype" name="nodetype">'
                edit_basic_data += '<tr><td>'+check+'</td><td>'+unique_input+'</td><td><input type="text" class="input form-control"  value="' + row.cells[2].innerHTML + '"  id="nodetype" name="nodetype"></td><td hidden><input value"'+guid+'"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
            else {
                $('#save_id').show();
                document.getElementById('save_id').style.visibility = 'visible';
            }
        }
    }
    display_button()
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#org_node_Modal').modal('show');
    table_sort_filter('id_popup_table');
}

//***************************
function display_button(){
    if(GLOBAL_ACTION == "DELETE"){
        $('#delete_data').show();
        $('#save_id').hide();
    }
    else{
        $('#save_id').show();
        document.getElementById('save_id').style.visibility = 'visible';
    }
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#org_node_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_org_node_type_code").prop("hidden", true);
    $("#id_error_msg_org_node_type_name").prop("hidden", true);
    $("#id_error_msg_org_node_type_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//*******************************************
function display_error_message(error_message){
    $("#error_msg_id").css("display", "block");
//    $('#error_message').text(error_message);
    document.getElementById("error_msg_id").innerHTML = error_message;
    document.getElementById("error_msg_id").style.color = "Red";
    $('#id_save_confirm_popup').modal('hide');
    $('#org_node_Modal').modal('show');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#org_node_Modal').modal('hide');
    orgnodetyp_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    orgnodetyp_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        org_node_type = {};
        org_node_type.del_ind_flag = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        org_node_type.node_type = row.find("TD").eq(1).find("select").val();
        org_node_type.description = row.find("TD").eq(2).find("input").val();
        org_node_type.node_type_guid = row.find("TD").eq(3).find('input').val();
        org_node_type.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        if (org_node_type == undefined) {
            org_node_type.node_type = row.find("TD").eq(1).find("select").val();
        }
        if(org_node_type.node_type_guid == undefined) {
            org_node_type.node_type_guid = '';
        }
        validate_add_attributes.push(org_node_type.node_type);
        orgnodetyp_data.push(org_node_type);
    });
     table_sort_filter('id_popup_table');
    return orgnodetyp_data;
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.country_code = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.country_code);
    });
    table_sort_filter('display_basic_table');
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select type="text" class="input form-control nodetype"   name="nodetype" onchange="GetSelectedTextValue(this)">' + node_type_dropdown + '</select></td><td><input class="form-control description" type="text"  name="description" value="'+desc_nodetype+'"  disabled></td><td hidden>guid</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td class="id_del_ind_checkbox1" hidden><input type="checkbox" name="del_ind_flag" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var org_node_type_arr_obj = {};
        var checked_box = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked')
        disable_check = row.find("TD").eq(0).find('input[type="checkbox"]').is(':disabled');
        if(checked_box)
        {
            org_node_type_arr_obj.del_ind_flag = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            org_node_type_arr_obj.del_ind = checked_box;
            org_node_type_arr_obj.description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
            org_node_type_arr_obj.node_type = row.find("TD").eq(1).find('input[type="text"]').val();
            org_node_type_arr_obj.node_type_guid = row.find("TD").eq(3).find('input[type="text"]').val();
            main_table_org_node_type_checked.push(org_node_type_arr_obj);
        }
    });
}

//Get message for check data function
function get_msg_desc_check_data(msg){
    var msg_type ;
    msg_type = message_config_details(msg);
    $("#error_msg_id").prop("hidden", false);
    return msg_type.messages_id_desc;
}