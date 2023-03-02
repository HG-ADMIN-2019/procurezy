var detgl_data = new Array();
var main_table_low_value = [];
var validate_add_attributes = [];
var detgl={};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "detgl_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";

}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button('copy')
    document.getElementById("id_del_add_button").style.display = "block";
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
    if (GLOBAL_ACTION == "detgl_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $("#Detgl_Modal").modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_Prod_cat_id").prop("hidden", true);
    $("#id_error_Fromvalue_lesserthan_Tovalue").prop("hidden", true);
    $("#id_error_FromvalueTovalue_positive_num").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//**********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Detgl_Modal').modal('show');
}

//****************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var detgl_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        gl_acc_num = row.find("TD").eq(4).find("select option:selected").val();
        gl_acc_default = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        account_assign_cat = row.find("TD").eq(3).find("select option:selected").val();
        company_id = row.find("TD").eq(1).find("select option:selected").val();
        from_value = row.find("TD").eq(6).find('input[type="number"]').val();
        to_value = row.find("TD").eq(7).find('input[type="number"]').val();
        currency_id = row.find("TD").eq(8).find("select option:selected").val();
        checked_box = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        var compare = gl_acc_num + '-' + company_id + '-' + account_assign_cat
        if (detgl_code_check.includes(compare)) {
            $(row).remove();
        }
        detgl_code_check.push(compare);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#Detgl_Modal').modal('hide');
    detgl_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    detgl_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        detgl = {};
        detgl.del_ind = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        detgl.prod_cat_id = row.find("TD").eq(1).find('select').val();
        detgl.gl_acc_num = row.find("TD").eq(4).find("select option:selected").val();
        detgl.gl_acc_default = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        detgl.account_assign_cat = row.find("TD").eq(3).find("select option:selected").val();
        detgl.company_id = row.find("TD").eq(2).find("select option:selected").val();
        detgl.from_value = row.find("TD").eq(6).find('input[type="number"]').val();
        detgl.to_value = row.find("TD").eq(7).find('input[type="number"]').val();
        detgl.currency_id = row.find("TD").eq(8).find("select option:selected").val();
        detgl.det_gl_acc_guid = row.find("TD").eq(9).find('input[type="text"]').val();
        var compare = detgl.gl_acc_num + '-' + detgl.account_assign_cat + '-' + detgl.company_id
        if (detgl == undefined) {
            detgl.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(compare);
        detgl_data.push(detgl);
    });
    return detgl_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><select class="form-control">' + prod_cat_dropdown + '</select></td>'+
    '<td><select class="form-control">' + company_dropdown + '</select></td>'+
    '<td><select class="form-control">' + accasscat_dropdown + '</select></td>'+
    '<td><select class="form-control">' + glacc_dropdown + '</select></td>'+
    '<td><input type="checkbox" name="gl_acc_default" required></td>'+
    '<td><input class="form-control" type="number"  min="1" name="From_value"  required></td>'+
    '<td><input class="form-control" type="number"  min="1" name="To_value"  required></td>'+
    '<td><select class="form-control">' + currency_dropdown + '</select></td><td hidden><input type="text" class="form-control"  value="GUID"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.prod_cat_id = row.find("TD").eq(1).html();
        main_attribute.company_id = row.find("TD").eq(2).html();
        main_attribute.account_assign_cat = row.find("TD").eq(3).html();
        main_attribute.gl_acc_num= row.find("TD").eq(4).html();
        main_attribute.item_from_value = row.find("TD").eq(6).html();
        main_attribute.item_to_value = row.find("TD").eq(7).html();
        main_attribute.currency_id = row.find("TD").eq(8).html();
        var detgl_compare = main_attribute.gl_acc_num + '-' + main_attribute.account_assign_cat + '-' + main_attribute.company_id
        main_table_low_value.push(detgl_compare);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var detgl_arr_obj = {};
        detgl_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if( detgl_arr_obj.del_ind){
            detgl_arr_obj.prod_cat_id = row.find("TD").eq(1).html();
            detgl_arr_obj.gl_acc_num= row.find("TD").eq(4).html();
            detgl_arr_obj.gl_acc_default = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            detgl_arr_obj.account_assign_cat = row.find("TD").eq(3).html();
            detgl_arr_obj.company_id = row.find("TD").eq(2).html();
            detgl_arr_obj.from_value = row.find("TD").eq(6).html();
            detgl_arr_obj.to_value = row.find("TD").eq(7).html();
            detgl_arr_obj.currency_id = row.find("TD").eq(8).html();
            detgl_arr_obj.det_gl_acc_guid = row.find("TD").eq(9).html();
            main_table_detgl_checked.push(detgl_arr_obj);
        }
    });
}