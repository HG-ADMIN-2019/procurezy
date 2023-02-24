var po_split_criteria_data = new Array();
var validate_add_attributes = [];
var po_split_criteria={};
var split_type_array = new Array();;

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_client").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_client_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    po_split_criteria_data = new Array();
    validate_add_attributes = [];
    split_type_array = [];
    if(GLOBAL_ACTION == "UPDATE"){
        $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            po_split_criteria={};
            po_split_criteria.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            po_split_criteria.activate = row.find("TD").eq(3).find('select[type="text"]').val();
            var data = '';
            if (po_split_criteria.activate == 'Activate'){
                data = true
            } else{
                data = false
            }
            po_split_criteria.activate  = data;
            po_split_criteria.company_code_id = row.find("TD").eq(2).find('input[type="text"]').val();
            po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
            po_split_criteria.po_split_criteria_guid = row.find("TD").eq(4).find('input[type="text"]').val();
            if (po_split_criteria == undefined){
                po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
            }
            var compare = po_split_criteria.po_split_type + '-' + po_split_criteria.company_code_id + '-' + po_split_criteria.activate
            validate_add_attributes.push(compare);
            split_type_array = (po_split_criteria.po_split_type).split(" -");
            po_split_criteria.po_split_type = split_type_array[0];
            po_split_criteria_data.push(po_split_criteria);
        });
    }
    else{
        $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            po_split_criteria={};
            po_split_criteria.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            po_split_criteria.activate = row.find("TD").eq(3).find('select[type="text"]').val();
            po_split_criteria.company_code_id = row.find("TD").eq(2).find('select[type="text"]').val();
            po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
            po_split_criteria.po_split_criteria_guid = row.find("TD").eq(4).find('input[type="text"]').val();
            if (po_split_criteria == undefined){
                po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
            }
            var data = '';
            if (po_split_criteria.activate == 'Activate'){
                data = true
            } else{
                data = false
            }
            po_split_criteria.activate  = data;
            var compare = po_split_criteria.po_split_type + '-' + po_split_criteria.company_code_id + '-' + po_split_criteria.activate
            validate_add_attributes.push(compare);
            po_split_criteria_data.push(po_split_criteria);
        });
    }
    $('#id_save_confirm_popup').modal('show');
});

//************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var aac_arr_obj = {};
        split_type_array = [];
        aac_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(aac_arr_obj.del_ind) {
            aac_arr_obj.po_split_type = row.find("TD").eq(1).html();
            aac_arr_obj.company_code_id = row.find("TD").eq(2).html();
            aac_arr_obj.activate = row.find("TD").eq(3).html();
            aac_arr_obj.po_split_criteria_guid = row.find("TD").eq(4).html();
            var data = '';
            if (aac_arr_obj.activate == 'Activate') {
                data = true
            } else{
                data = false
            }
            aac_arr_obj.activate  = data;
            split_type_array = (aac_arr_obj.po_split_type).split(" -");
            aac_arr_obj.po_split_type = split_type_array[0];
            main_table_po_crt_checked.push(aac_arr_obj);
        }
    });
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_code_id = row.find("TD").eq(1).html();
        main_attribute.call_off = row.find("TD").eq(2).html();
        main_attribute.purchase_ctrl_flag = row.find("TD").eq(3).html();
        var data = '';
        if (main_attribute.purchase_ctrl_flag == 'Activate') {
            data = true
        } else {
            data = false
        }
        main_attribute.purchase_ctrl_flag = data;
        main_attribute.purchase_control_guid = row.find("TD").eq(4).html();
        main_table_low_value.push(main_attribute);
    });
    table_sort_filter_page('display_basic_table');
}

    // Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var purchase_contrl_type_dic = {};
        purchase_contrl_type_dic.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
         if (purchase_contrl_type_dic.del_ind) {
            purchase_contrl_type_dic.company_code_id = row.find("TD").eq(1).html();
            purchase_contrl_type_dic.call_off = row.find("TD").eq(2).html();
            purchase_contrl_type_dic.purchase_ctrl_flag = row.find("TD").eq(3).html();
            purchase_contrl_type_dic.purchase_control_guid = row.find("TD").eq(4).html();
            var data = '';
            if (purchase_contrl_type_dic.purchase_ctrl_flag == 'Activate'){
                data = true
            } else{
                data = false
            }
            purchase_contrl_type_dic.purchase_ctrl_flag  = data;
            main_table_purchase_contrl_checked.push(purchase_contrl_type_dic);
        }
    });
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html +=
    `<tr>
        <td><input type="checkbox" required></td>
        <td><select class="input form-control" type="text">${pc_company_dropdown}</select></td>
        <td>
            <select class="input form-control" type="text">
                <option value="1">Catalog</option>
                <option value="2">Free text</option>
                <option value="3">PR</option>
                <option value="4">Limit</option>
            </select>
        </td>
        <td><select type="text" class="input form-control">${activate_dropdown}</select></td>
        <td hidden><input  type="text" class="form-control"  name="guid"></td>
        <td class="class_del_checkbox" hidden><input type="checkbox" required></td>
    </tr>`
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}