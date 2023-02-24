var accasscat_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var aac={};

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_aac_code").prop("hidden", true);
    $("#id_error_msg_aac_name").prop("hidden", true);
    $("#id_error_msg_aac_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_aac_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_aac_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.account_assign_cat + '</td><td>' + item.description + '</td></tr>';
    });
    $('#id_aac_tbody').append(edit_basic_data);
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

// Function to delete duplicates
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var aac_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        account_assign_cat = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')
        if (aac_code_check.includes(account_assign_cat)) {
            $(row).remove();
        }
        aac_code_check.push(account_assign_cat);
    })
    table_sort_filter('id_popup_table')
    check_data()
}

//Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    accasscat_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
        '<td><select type="text" class="input form-control acct_assignment_category" id="acct_assignment_category-1" name="acct_assignment_category" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ aac_dropdown +'</select></td>'+
        '<td><input class="form-control description check_special_char" type="text"  name="description"  id="description-1" disabled></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

//Read popup table data
function read_popup_data(){
    accasscat_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        aac = {};
        aac.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        aac.description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        aac.account_assign_cat = row.find("TD").eq(1).find('select[type="text"]').val();
        if (aac == undefined) {
            aac.account_assign_cat= row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(aac.account_assign_cat);
        accasscat_data.push(aac);
    });
    return accasscat_data;
}

//********************************************
function GetSelectedTextValue(acct_assignment_category) {
    var selectedText = acct_assignment_category.options[acct_assignment_category.selectedIndex].innerHTML;
    var selectedValue = acct_assignment_category.value;
    var selectedId = (acct_assignment_category.id).split('-')[1];
     $.each(rendered_aac_values, function(i, item){
        if(selectedValue == item.field_type_id){
            $('#description-'+selectedId).val(item.field_type_desc);
        }
    });
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var aac_arr_obj = {};
        aac_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(aac_arr_obj.del_ind){
            aac_arr_obj.account_assign_cat = row.find("TD").eq(1).html();
            aac_arr_obj.description = row.find("TD").eq(2).html();
            main_table_aac_checked.push(aac_arr_obj);
        }
    });
}

// Function to get main table data
function get_main_table_data(){
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.account_assign_cat = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.account_assign_cat);
    });
    table_sort_filter_page('display_basic_table');
}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, aac) {
    add_attr_duplicates = false;
    var error_message = ''
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var no_duplicate_value = 'Y'
    $.each(validate_add_attributes, function (index, value) {
        if ($.inArray(value, add_attr_unique_list) == -1) {
            add_attr_unique_list.push(value);
        } else {
            if ($.inArray(value, add_attr_duplicates_list) == -1) {
                add_attr_duplicates_list.push(value);
            }
        }
    });
    if (add_attr_duplicates_list.length != 0) {
        get_message_details("JMSG001"); // Get message details
        no_duplicate_value = 'N'
        return [no_duplicate_value,error_message]
    }
    else {
        $.each(aac, function (i, item) {
            if (item.account_assign_cat.length == 0) {
                get_message_details("JMSG002"); //// Get message details
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
            if (item.description.length == 0) {
                get_message_details("JMSG002"); //// Get message details
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
        });
    }
    return [no_duplicate_value,error_message]
}

//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var error_message =''
    var common = [];
    jQuery.grep(validate_add_attributes, function (el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) {
            common.push(el);
        }
    });
    if (common.length != 0) {
        get_message_details("JMSG001"); // Get message details
        no_duplicate_value = 'N'
        return [no_duplicate_value,error_message]
    }
    return [no_duplicate_entries,error_message]
}