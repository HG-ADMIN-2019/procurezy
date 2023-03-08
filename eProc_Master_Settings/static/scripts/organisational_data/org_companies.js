var company_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var orgcompany={};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "orgcompany_upload"
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
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//onclick of add button display companyModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#companyModal').modal('show');
    new_row_data(); // Add a new row in popup
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("");
    });
    new_row_data(); // Add a new row in popup
    if (GLOBAL_ACTION == "orgcompany_upload") {
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    table_sort_filter('id_popup_table');
}

//**********************************************************
function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    var dropdown_select_array = []
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var guid= '';
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
        var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                edit_basic_data += '<tr><td><input type="checkbox"></td><td><input class="form-control check_special_char" type="text" value="' + row.cells[1].innerHTML + '" minlength="4" maxlength="08" name="company_id" required></td><td><input class="form-control check_special_char" type="text" value="' + row.cells[2].innerHTML + '" maxlength="100" name="name1" required></td><td><input class="form-control check_special_char" type="text" value="' + row.cells[3].innerHTML + '" maxlength="100" name="name2" required></td><td hidden><input value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';;
                $("#header_select").prop("hidden",false);
            }
            else{
                guid = row.cells[5].innerHTML;

                edit_basic_data += '<tr><td hidden><input type="checkbox"></td><td><input class="form-control check_special_char" type="text" value="' + row.cells[1].innerHTML + '" minlength="4" maxlength="08" name="company_id" disabled></td><td><input class="form-control" type="text" value="' + row.cells[2].innerHTML + '" maxlength="100" name="name1" required></td><td><input class="form-control" type="text" value="' + row.cells[3].innerHTML + '" maxlength="100" name="name2" required><td hidden><input value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';

                $("#header_select").prop("hidden",true);
            }
            var row = checkBoxes[i].parentNode.parentNode;
            var company_id = row.cells[1].innerHTML
            dropdown_select_array.push([company_id])
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#companyModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#companyModal').modal('hide');
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

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#companyModal').modal('hide');
    company_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    validate_add_attributes = [];
    company_data = new Array();
    var orgcompany = {};
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        orgcompany = {};
        orgcompany.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        orgcompany.object_id = row.find("TD").eq(4).find('input').val();
        orgcompany.name1 = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        orgcompany.name2= row.find("TD").eq(3).find('input[type="text"]').val();
        orgcompany.company_id = row.find("TD").eq(1).find('input[type="text"]').val();
        orgcompany.company_guid = row.find("TD").eq(5).find('input[type="text"]').val();
        if (orgcompany == undefined) {
            orgcompany.company_id=row.find("TD").eq(3).find('input[type="text"]').val();
        }
        if(orgcompany.company_guid == undefined) {
            orgcompany.company_guid = ''
        }
        if(orgcompany.object_id == undefined) {
            orgcompany.object_id = '';
        }
        if(orgcompany.object_id == null) {
         orgcompany.object_id = '';
        }
        validate_add_attributes.push(orgcompany.company_id);
        company_data.push(orgcompany);
    });
    return company_data;
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_company_tbody').empty();
     $('#display_data').empty();
    var edit_basic_data = '';
    $.each(rendered_orgcompany_data, function(i, item) {
        var data = '';
        if (item.object_id == null){
            data = ''
        }
        else{
            data = item.object_id
        }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.company_id + '</td><td>' + item.name1 + '</td><td>' + item.name2 + '</td><td>' + data + '</td><td hidden>'+item.company_guid+'</td><td hidden>'+item.del_ind+'</td></tr>';
    });
    $('#id_company_tbody').append(edit_basic_data);
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

//*******************************************************
function display_error_message(error_message) {
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#companyModal').modal('show');
}

//**********************************************
function update_check_message(messages) {
    $.each(messages, function (i, message) {
        $("#id_check_success_messages").append('<p>' + message + '</p>')
    });
    $("#id_check_success_messages").prop("hidden",false)
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr> <td><input class="input" type="checkbox" required></td><td><input class="form-control check_special_char color_change" type="text"  name= "company_id"  minlength="4" maxlength="8"></td><td><input class="form-control check_special_char" type="text" name="name1"  maxlength="100"></td><td><input class="form-control check_special_char" type="text" name="name2" maxlength="100"></td><td hidden><input value="GUID" hidden></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.company_id);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var orgcompany_arr_obj = {};
        orgcompany_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(orgcompany_arr_obj.del_ind){
        orgcompany_arr_obj.object_id = row.find("TD").eq(4).html();
        orgcompany_arr_obj.name1 = row.find("TD").eq(2).html();
        orgcompany_arr_obj.name2 = row.find("TD").eq(3).html();
        orgcompany_arr_obj.company_id = row.find("TD").eq(1).html();
        orgcompany_arr_obj.company_guid = row.find("TD").eq(5).html();
        main_table_orgcompany_checked.push(orgcompany_arr_obj);
        }
    });
}