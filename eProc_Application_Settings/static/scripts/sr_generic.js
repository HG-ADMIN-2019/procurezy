var sr_generic_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var sr_generic = {};
var hidden_prod_cat_IDs = [];

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_pc_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_sr_generic_data, function (i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.prod_cat_id_from + '</td><td>' + item.prod_cat_id_to + '</td><td>' + item.company_id + '</td><td>' + item.call_off + '</td><td>' + item.rule_type + '</td><td>' + item.sourcing_flag + '</td><td hidden>' + item.sourcing_rule_guid + '</td><td hidden>' + item.del_ind + '</td></tr>';
    });
    $('#id_pc_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $(" input:checkbox ").prop('checked', false);
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

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#purchase_ctrl_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_pc_code").prop("hidden", true);
    $("#id_error_msg_pc_name").prop("hidden", true);
    $("#id_error_msg_pc_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message) {
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#purchase_ctrl_Modal').modal('show');
}

// Function to delete duplicates
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var pur_contrl_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        call_off = row.find("TD").eq(2).find('input[type="text"]').val();
        purchase_ctrl_flag = row.find("TD").eq(3).find('input[type="checkbox"]').val();
        company_id = row.find("TD").eq(1).find('input[type="text"]').val();
        checked_box = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked')
        if (pur_contrl_check.includes(company_id)) {
            $(row).remove();
        }
        pur_contrl_check.push(company_id);
    })
    table_sort_filter('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#sr_generic_Modal').modal('hide');
    sr_generic_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    sr_generic_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        sr_generic = {};
        sr_generic.del_ind = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        sr_generic.prod_cat_id_from = row.find("TD").eq(1).find('select[type="text"]').val();
        sr_generic.prod_cat_id_to = row.find("TD").eq(2).find('select[type="text"]').val();
        sr_generic.company_id = row.find("TD").eq(3).find('select option:selected').val();
        sr_generic.call_off = row.find("TD").eq(4).find('select[type="text"]').val();
        sr_generic.rule_type = row.find("TD").eq(5).find('select[type="text"]').val();
        sr_generic.sourcing_flag = row.find("TD").eq(6).find('select[type="text"]').val();
        sr_generic.sourcing_rule_guid = row.find("TD").eq(7).find('input[type="text"]').val();
        var data = '';
        if (sr_generic.sourcing_flag == 'Activate'){
            data = true
        } else{
            data = false
        }
        sr_generic.sourcing_flag  = data;
        var compare = sr_generic.prod_cat_id_from + '-' + sr_generic.prod_cat_id_to + '-' + sr_generic.company_id+ '-' +
                    sr_generic.call_off + '-' + sr_generic.rule_type + '-' + sr_generic.sourcing_flag
        validate_add_attributes.push(compare);
        sr_generic_data.push(sr_generic);
    });
    table_sort_filter('id_popup_table');
    return sr_generic_data;
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.prod_cat_id_from = row.find("TD").eq(1).html();
        main_attribute.prod_cat_id_to = row.find("TD").eq(2).html();
        main_attribute.company_id = row.find("TD").eq(3).html();
        main_attribute.call_off = row.find("TD").eq(4).html();
        main_attribute.rule_type = row.find("TD").eq(5).html();
         main_attribute.sourcing_flag = row.find("TD").eq(6).html();
        var data = '';
        if (main_attribute.sourcing_flag == 'Activate') {
            data = true
        } else {
            data = false
        }
        main_attribute.sourcing_flag = data;
        main_attribute.purchase_control_guid = row.find("TD").eq(5).html();
        var compare_maintable = main_attribute.prod_cat_id_from + '-' + main_attribute.prod_cat_id_to + '-' +
                                main_attribute.company_id + '-' + main_attribute.call_off + '-' + main_attribute.rule_type + '-' + main_attribute.sourcing_flag
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter_page('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var purchase_contrl_type_dic = {};
        purchase_contrl_type_dic.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
         if (purchase_contrl_type_dic.del_ind) {
            purchase_contrl_type_dic.company_code_id = row.find("TD").eq(1).html();
            purchase_contrl_type_dic.call_off = row.find("TD").eq(2).html().split("-")[0];
            purchase_contrl_type_dic.prod_cat_id = row.find("TD").eq(3).html();
            purchase_contrl_type_dic.purchase_ctrl_flag = row.find("TD").eq(4).html();
            purchase_contrl_type_dic.purchase_control_guid = row.find("TD").eq(5).html();
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
        <td><select class="input form-control" type="text">${prod_cat_dropdown}</select></td>
        <td><select class="input form-control" type="text">${prod_cat_dropdown}</select></td>
        <td><select class="input form-control" type="text">${pc_company_dropdown}</select></td>
        <td><select class="input form-control" type="text">${call_off_dropdown}</select></td>
        <td><select class="input form-control" type="text">${rule_type_dropdown}</select></td>
        <td><select type="text" class="input form-control">${activate_dropdown}</select></td>
        <td hidden><input  type="text" class="form-control"  name="guid"></td>
        <td class="class_del_checkbox" hidden><input type="checkbox" required></td>
    </tr>`
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}