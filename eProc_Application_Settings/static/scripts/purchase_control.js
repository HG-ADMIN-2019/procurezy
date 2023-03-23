var purhcase_control_data = new Array();
var validate_add_attributes = [];
var purchase_control = {};

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
    $.each(rendered_pc_data, function (i, item) {
        var data = '';
        if (item.purchase_ctrl_flag == true) {
            data = 'Activate'
        } else {
            data = 'Deactivate'
        }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.company_code_id + '</td><td>' + item.call_off + '</td><td>' + data + '</td><td hidden>' + item.purchase_control_guid + '</td><td hidden>' + item.del_ind_flag + '</td></tr>';
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
    $('#myModal').modal('hide');
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
    $('#myModal').modal('show');
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
    $('#myModal').modal('hide');
    purhcase_control_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        purchase_contrl = {};
        purchase_contrl.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        purchase_contrl.purchase_control_guid = row.find("TD").eq(4).find('input[type="text"]').val();
        purchase_contrl.company_code_id = row.find("TD").eq(1).find('select[type="text"]').val();
        purchase_contrl.call_off = row.find("TD").eq(2).find('select[type="text"]').val();
        purchase_contrl.purchase_ctrl_flag = row.find("TD").eq(3).find('select[type="text"]').val();
        var data = '';
        if (purchase_contrl.purchase_ctrl_flag == 'Activate'){
            data = true
        } else{
            data = false
        }
        purchase_contrl.purchase_ctrl_flag  = data;
        if (purchase_contrl == undefined) {
            purchase_contrl.company_code_id = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(purchase_contrl.company_code_id);
        purhcase_control_data.push(purchase_contrl);
    });
    $('#id_save_confirm_popup').modal('show');
});

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