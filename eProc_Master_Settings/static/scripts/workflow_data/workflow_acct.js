var wfacc_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var wfacc = {};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "workflowacc_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}

//*********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block");
    $('#id_save_confirm_popup').modal('hide');
    $('#Wf_Acc_Modal').modal('show');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Wf_Acc_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_wfacc").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#Wf_Acc_Modal').modal('hide');
    wfacc_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    wfacc_data = new Array();
    validate_add_attributes = [];
    var wfacc = {};
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        wfacc = {};
        wfacc.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        wfacc.company_id = row.find("TD").eq(1).find('select[type="text"]').val();
        wfacc.account_assign_cat = row.find("TD").eq(2).find('select[type="text"]').val();
        wfacc.acc_value = row.find("TD").eq(3).find('input[type="number"]').val();
        wfacc.app_username = row.find("TD").eq(4).find('select[type="text"]').val();
        wfacc.sup_company_id = row.find("TD").eq(5).find('select[type="text"]').val();
        wfacc.sup_account_assign_cat = row.find("TD").eq(6).find('select[type="text"]').val();
        wfacc.sup_acc_value = row.find("TD").eq(7).find('input[type="number"]').val();
        wfacc.sup_currency_id = row.find("TD").eq(8).find('select[type="text"]').val();
        wfacc.workflow_acc_guid = row.find("TD").eq(9).find('input[type="text"]').val();
        if (wfacc == undefined) {
            wfacc.app_username = row.find("TD").eq(4).find('select[type="text"]').val();
        }
        if(wfacc.workflow_acc_guid == undefined) {
            wfacc.workflow_acc_guid = ''
        }
        var wfacc_compare = wfacc.company_id +'-'+  wfacc.account_assign_cat +'-'+ wfacc.acc_value +'-'+ wfacc.app_username +'-'+ wfacc.sup_company_id +'-'+wfacc.sup_account_assign_cat +'-'+ wfacc.sup_acc_value +'-'+ wfacc.sup_currency_id
        validate_add_attributes.push(wfacc_compare);
        wfacc_data.push(wfacc);
    });
    return wfacc_data;
}

// Function for add a new row data
function new_row_data()  {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="form-control">'+ company_id_dropdown +'</select></td>'+
    '<td><select type="text" class="form-control">'+ acc_ass_dropdwn+'</select></td>'+
    '<td><input class="form-control" type="number" maxlength="40"  name="acc_value" required></td>'+
    '<td><select type="text" class="form-control">'+ user_dropdwn +'</select></td>'+
    '<td><select type="text" class="form-control">'+ supcompany_dropdwn +'</select></td>'+
    '<td><select type="text" class="form-control">'+ sup_acc_ass_dropdwn +'</select></td>'+
    '<td><input class="form-control" type="number" maxlength="40"  name="sup_acc_value"  required></td>'+
    '<td><select type="text" class="form-control">'+ currency_dropdwn +'</select></td>'+
    '<td class="class_del_checkbox" hidden> <input type="checkbox" required> </td>'+
    '<td hidden><input type="text" id="workflow_acc_guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}


// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.account_assign_cat = row.find("TD").eq(2).html();
        main_attribute.acc_value = row.find("TD").eq(3).html();
        main_attribute.app_username = row.find("TD").eq(4).html();
        main_attribute.sup_company_id = row.find("TD").eq(5).html();
        main_attribute.sup_account_assign_cat = row.find("TD").eq(6).html();
        main_attribute.sup_acc_value = row.find("TD").eq(7).html();
        main_attribute.sup_currency_id = row.find("TD").eq(8).html();
        var wfacc_compare_maintable = main_attribute.company_id+'-'+main_attribute.account_assign_cat+'-'+main_attribute.acc_value+'-'+main_attribute.app_username+'-'+main_attribute.sup_company_id+'-'+main_attribute.sup_account_assign_cat+'-'+main_attribute.sup_acc_value+'-'+main_attribute.sup_currency_id
        main_table_low_value.push(wfacc_compare_maintable);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var workflowaccounting_arr_obj ={};
        workflowaccounting_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(workflowaccounting_arr_obj.del_ind){
            workflowaccounting_arr_obj.company_id = row.find("TD").eq(1).html();
            workflowaccounting_arr_obj.account_assign_cat = row.find("TD").eq(2).html();
            workflowaccounting_arr_obj.acc_value = row.find("TD").eq(3).html();
            workflowaccounting_arr_obj.app_username = row.find("TD").eq(4).html();
            workflowaccounting_arr_obj.sup_company_id = row.find("TD").eq(5).html();
            workflowaccounting_arr_obj.sup_account_assign_cat = row.find("TD").eq(6).html();
            workflowaccounting_arr_obj.sup_acc_value = row.find("TD").eq(7).html();
            workflowaccounting_arr_obj.sup_currency_id = row.find("TD").eq(8).html();
            workflowaccounting_arr_obj.workflow_acc_guid = row.find("TD").eq(9).html();
            main_table_workflowaccounting_checked.push(workflowaccounting_arr_obj);
        }
    });
}