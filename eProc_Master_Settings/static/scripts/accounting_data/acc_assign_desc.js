var aad_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var aad={};
var corresponding_values = {};

//*********************************************************
function account_assignment_value_find(company_num) {
    corresponding_values = {};
    corresponding_values.acc_ass_dropdwn = '';
    corresponding_values.acc_ass_val_dropdwn = '';
    corresponding_values.other_dropdn = '';
    company_list = company_list;
    unique_acct_cat= [];
    unique_acct_assmt_val = [];
    for (var i = 0; i < company_list.length; i++) {
        compare_dict = {};
        compare_dict = company_list[i]
        if (company_num == compare_dict.company_id) {
            unique_acct_cat.push(compare_dict.account_assign_cat);
            unique_acct_assmt_val.push(compare_dict.account_assign_value);
        }
    }
     for (var i = 0; i < arrDistinct.length; i++) {
        corresponding_values.other_dropdn += '<option value="'+arrDistinct[i]+'">' + arrDistinct[i] + '</option>'
     }
     assmtCatDistinct = [];
     $(unique_acct_cat).each(function (index, item) {
     if ($.inArray(item, assmtCatDistinct) == -1)
        assmtCatDistinct.push(item);
     });
     for (var i = 0; i < assmtCatDistinct.length; i++) {
        corresponding_values.acc_ass_dropdwn += '<option value="'+assmtCatDistinct[i]+'">' + assmtCatDistinct[i] + '</option>'
     }
     assmtValDistinct = [];
     $(unique_acct_assmt_val).each(function (index, item) {
     if ($.inArray(item, assmtValDistinct) == -1)
        assmtValDistinct.push(item);
     });
     for (var i = 0; i < assmtValDistinct.length; i++) {
        corresponding_values.acc_ass_val_dropdwn += '<option value="'+assmtValDistinct[i]+'">' + assmtValDistinct[i] + '</option>'
     }
    return corresponding_values
}
function account_assignment_cat(acct_cat, comp_num) {
    corresponding_values = {};
    corresponding_values.acc_ass_val_dropdwn = '';
    company_list = company_list;
    unique_acct_assmt_val = [];
    var assmtValDistinct = [];
     for (var i = 0; i < company_list.length; i++) {
        compare_dict = {};
        compare_dict = company_list[i]
        if ((acct_cat == compare_dict.account_assign_cat) && (comp_num == compare_dict.company_id)) {
            unique_acct_assmt_val.push(compare_dict.account_assign_value);
        }
        assmtValDistinct = [];
        $(unique_acct_assmt_val).each(function (index, item) {
        if ($.inArray(item, assmtValDistinct) == -1)
            assmtValDistinct.push(item);
        });
    }
    for (var i = 0; i < assmtValDistinct.length; i++) {
            corresponding_values.acc_ass_val_dropdwn += '<option value="'+assmtValDistinct[i]+'">'+assmtValDistinct[i]+'</option>'
    }
    return corresponding_values
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "aad_upload"
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

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("UPDATE")
    document.getElementById("id_del_add_button").style.display = "none";
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    new_row_data();   // Add a new row in popup
    var company_num = '';
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        row.find("TD").eq(2).find("select").empty()
        row.find("TD").eq(3).find("select").empty()
        company_num = row.find("TD").eq(1).find("select option:selected").val();
        var assign_val = account_assignment_value_find(company_num)
        row.find("TD").eq(2).find("select").append(assign_val.acc_ass_dropdwn)
        row.find("TD").eq(3).find("select").append(assign_val.acc_ass_val_dropdwn)
        $(row.find("TD").eq(1).find("select")).change(function () {
              company_dropdwn_change(row);
        })
        $(row.find("TD").eq(2).find("select")).change(function () {
            company_num = row.find("TD").eq(1).find("select option:selected").val();
            acc_ass_cat_dropdwn(row,company_num);
        })
    })
    if (GLOBAL_ACTION == "aad_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
}

function company_dropdwn_change(row){
    row.find("TD").eq(2).find("select").empty()
    row.find("TD").eq(3).find("select").empty()
    company_num = row.find("TD").eq(1).find("select option:selected").val();
    var comp_val = account_assignment_value_find(company_num)
    row.find("TD").eq(2).find("select").append(comp_val.acc_ass_dropdwn)
    row.find("TD").eq(3).find("select").append(comp_val.acc_ass_val_dropdwn)
}

function acc_ass_cat_dropdwn(row,company_num){
    acct_cat = row.find("TD").eq(2).find("select option:selected").val();
    row.find("TD").eq(3).find("select").empty();
    var acct_cat_val = account_assignment_cat(acct_cat,company_num)
    row.find("TD").eq(3).find("select").append(acct_cat_val.acc_ass_val_dropdwn)
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Acc_desc_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_aad_code").prop("hidden", true);
    $("#id_error_msg_aad_name").prop("hidden", true);
    $("#id_error_msg_aad_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_aad_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_accdatadescs_data, function (i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
        '<td >' + item.company_id + '</td>'+
        '<td> ' + item.account_assign_cat + '</td>'+
        '<td>' + item.account_assign_value + '</td>'+
        '<td>' + item.description + '</td>'+
        '<td>' + item.language_id + '</td>'+
        '<td hidden>' + item.acc_desc_guid + '</td></tr>';
    });
    $('#id_aad_tbody').append(edit_basic_data);
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

//********************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var aad_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        company_id = row.find("TD").eq(1).find("select option:selected").val();
        account_assign_cat = row.find("TD").eq(2).find("select option:selected").val();
        account_assign_value = row.find("TD").eq(3).find("select option:selected").val();
        description = (row.find("TD").eq(4).find('input[type="text"]').val()).toUpperCase();
        language_id = row.find("TD").eq(5).find("select option:selected").val();
        var compare = account_assign_value + '-' + account_assign_cat + '-' + company_id + '-' + language_id
        if (aad_code_check.includes(compare)) {
            $(row).remove();
        }
        aad_code_check.push(compare);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data();
}

//********************************************
function delete_invalid_aav() {
    $('#id_popup_table').DataTable().destroy();
    var aad_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        company_id = row.find("TD").eq(1).find("select option:selected").val();
        account_assign_cat = row.find("TD").eq(2).find("select option:selected").val();
        account_assign_value = row.find("TD").eq(3).find("select option:selected").val();
        description = (row.find("TD").eq(4).find('input[type="text"]').val()).toUpperCase();
        language_id = row.find("TD").eq(5).find("select option:selected").val();
        check_value = row.find("TD").eq(8).html()
        if (check_value == "0") {
            $(row).remove();
        }
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

//********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Acc_desc_Modal').modal('show');

}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#Acc_desc_Modal').modal('hide');
    aad_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    aad_data = new Array();
    validate_add_attributes = [];
    var desc='';
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        aad = {};
        aad.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        aad.company_id = row.find("TD").eq(1).find("select option:selected").val();
        aad.account_assign_cat = row.find("TD").eq(2).find("select option:selected").val();
        aad.account_assign_value = row.find("TD").eq(3).find("select option:selected").val();
        aad.description = (row.find("TD").eq(4).find('input[type="text"]').val()).toUpperCase();
        aad.language_id = row.find("TD").eq(5).find("select option:selected").val();
        aad.acc_desc_guid = row.find("TD").eq(6).find('input[type="text"]').val();
        if (aad == undefined) {
            aad.company_id = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        if(aad.acc_desc_guid == undefined) {
                aad.acc_desc_guid = ''
            }
        var compare = aad.account_assign_value + '-' + aad.account_assign_cat + '-' + aad.company_id + '-' + aad.language_id
        validate_add_attributes.push(compare);
        aad_data.push(aad);
    }); 
    return aad_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr> <td><input class="input" type="checkbox" required></td>'+
    '<td><select id="comp_id" class="form-control">' + company_dropdwn + ' </select></td>'+
    '<td><select class="form-control"></select></td>'+
    '<td><select class="form-control"></select></td>'+
    '<td><input class="form-control check_special_char" type="text"  maxlength="255" ></td>'+
    '<td><select class="form-control">' + language_dropdwn + '</select></td>'+
    '<td hidden><input value="GUID" hidden></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td> <td hidden></td>'+
     '</tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

 // Function to get main table data
 function get_main_table_data() {
    main_table_low_value = [];
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html()
        main_attribute.account_assign_cat = row.find("TD").eq(2).html()
        main_attribute.account_assign_value = row.find("TD").eq(3).html()
        main_attribute.language_id = row.find("TD").eq(5).html()
        var compare_maintable = main_attribute.account_assign_value+'-'+main_attribute.account_assign_cat+'-'+main_attribute.company_id+'-'+main_attribute.language_id;
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter('display_basic_table');
 }
 
 // Function to get the selected row data
 function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var aad_arr_obj = {};
        aad_arr_obj.del_ind =  row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(aad_arr_obj.del_ind) {
            aad_arr_obj.company_id = row.find("TD").eq(1).html()
            aad_arr_obj.account_assign_cat = row.find("TD").eq(2).html()
            aad_arr_obj.account_assign_value = row.find("TD").eq(3).html()
            aad_arr_obj.description = (row.find("TD").eq(4).html()).toUpperCase()
            aad_arr_obj.language_id = row.find("TD").eq(5).html()
            aad_arr_obj.acc_desc_guid = row.find("TD").eq(6).html()
            main_table_aad_checked.push(aad_arr_obj);
        }
    });
}