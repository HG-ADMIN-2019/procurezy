var addresstype_data = new Array();
var main_table_low_value = [];
var validate_add_attributes = [];
var duplicate_entry = [];
var addresstype={};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "addresstype_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("COPY")
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("UPDATE")
    document.getElementById("id_del_add_button").style.display = "none";
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Adrs_Type_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_address_type").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();


});

//*********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Adrs_Type_Modal').modal('show');
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
    if (GLOBAL_ACTION == "addresstype_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_address_type_tbody').empty();
    var edit_basic_data = '';
    var from_date, to_date;
    $.each(rendered_address_type_data, function (i, item) {
        if(item.valid_from == ''){
            from_date = '';
            to_date = '';
        } else {
            from_date = new Date(item.valid_from).toLocaleDateString('en-CA', {day: '2-digit', month: '2-digit', year: 'numeric'});
            to_date = new Date(item.valid_to).toLocaleDateString('en-CA', {day: '2-digit', month: '2-digit', year: 'numeric'});
        }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>' +
        '<td>'+ item.company_id +'</td>'+
        '<td>' + item.address_type + '</td>' +
        '<td>' + item.address_number + '</td>' +
        '<td>'+ from_date +'</td>'+
        '<td>'+ to_date +'</td>'+
        '<td hidden> <input type="checkbox"></td>' +
        '<td hidden>' + item.address_guid + '</td></tr>';
    });
    $('#id_address_type_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').hide();
    $('#id_delete_confirm_popup').hide();
    $('#id_check_all').hide();
    table_sort_filter('display_basic_table');
}


// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#Adrs_Type_Modal').modal('hide');
    addresstype_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
  validate_add_attributes = [];
  addresstype_data = new Array();
  var check_dates = []
  $("#id_popup_table TBODY TR").each(function () {
    var row = $(this);
    addresstype = {};
    addresstype.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
    addresstype.address_guid = row.find("TD").eq(7).find('input').val();
    addresstype.address_number = row.find("TD").eq(3).find('select').val();
    addresstype.address_type = row.find("TD").eq(2).find('select').val();
    addresstype.company_id = row.find("TD").eq(1).find('select').val();
    addresstype.valid_from = row.find("TD").eq(4).find('input[type="date"]').val();
    addresstype.valid_to = row.find("TD").eq(5).find('input[type="date"]').val();
    if ((addresstype.valid_from == undefined) || (addresstype.valid_from == '')) {
      addresstype.valid_from = '';
    } else {
      var from_date = new Date(addresstype.valid_from).toISOString().slice(0, 10);
      addresstype.valid_from = from_date;
    }
    addresstype.valid_to = row.find("TD").eq(5).find('input[type="date"]').val();
    if ((addresstype.valid_to == undefined) || (addresstype.valid_to == '')) {
      addresstype.valid_to = '';
    } else {
      var to_date = new Date(addresstype.valid_to).toISOString().slice(0, 10);
      addresstype.valid_to = to_date;
    }
    var addresstype_compare = addresstype.address_number + '-' + addresstype.address_type + '-' + addresstype.company_id
    if (addresstype == undefined) {
      addresstype.address_number = row.find("TD").eq(2).find('input').val();
    }
    if (addresstype.address_guid == undefined) {
      addresstype.address_guid = ''
    }
    check_dates.push([addresstype.valid_from, addresstype.valid_to])
    validate_add_attributes.push(addresstype_compare);
    addresstype_data.push(addresstype);
  });
  return addresstype_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
        '<td><select class="form-control">'+company_dropdwn+'</select></td>' +
        '<td><select class="form-control">'+address_type_dropdown+'</select></td>' +
        '<td><select class="form-control">'+address_number_dropdwn+'</select></td>' +
        '<td><input  type="date" name = "valid_from" class="form-control from_to_date"></td>' +
        '<td><input type="date" name = "valid_to"  class="form-control from_to_date"></td>' +
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
        '<td hidden><input  type="text" class="form-control"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
//    DateFormat();
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.address_number = row.find("TD").eq(3).html();
        main_attribute.address_type = row.find("TD").eq(2).html();
        main_attribute.company_id = row.find("TD").eq(1).html();
        var address_compare_maintable = main_attribute.address_number +'-'+ main_attribute.address_type+'-'+main_attribute.company_id
        main_table_low_value.push(address_compare_maintable);
    });
    table_sort_filter('display_basic_table');
}

 // Function to get the selected row data
 function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var address_type_arr_obj = {};
        address_type_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(address_type_arr_obj.del_ind ){
            address_type_arr_obj.address_guid = row.find("TD").eq(7).html();
             address_type_arr_obj.valid_to = row.find("TD").eq(5).html();
              address_type_arr_obj.valid_from = row.find("TD").eq(4).html();
             address_type_arr_obj.company_id = row.find("TD").eq(1).html();
            address_type_arr_obj.address_type = row.find("TD").eq(2).html();
            address_type_arr_obj.address_number = row.find("TD").eq(3).html();
//            fromdate = address_type_arr_obj.valid_from;
//            todate = address_type_arr_obj.valid_to;
//            address_type_arr_obj.valid_from = fromdate
//            address_type_arr_obj.valid_to = todate
            main_table_address_type_checked.push(address_type_arr_obj);
        }
    });
 }
function check_date(addresstype_data) {
    var validDate = 'Y';
    var error_message = ''
    $.each(addresstype_data, function (i, item) {
        if ((Date.parse(item.valid_to) < Date.parse(item.valid_from)) == true) {
            error_message = 'From Date Is Greater Than To Date'; // set the error message
            validDate = 'N';
            return false; // exit the loop as soon as an invalid date range is found
        }
    });
    if (validDate == 'N') {
        display_error_message(error_message); // display the error message
    } else {
        $('#error_msg_id').css('display', 'none'); // hide the error message if no invalid date ranges were found
    }
    return [validDate, error_message];
}

//*******************************************
function check_date_error(check_dates) {
    date_error = "N"
    $.each(check_dates, function(index, value){
        var d1=new Date(value[0]); //yyyy-mm-dd
        var d2=new Date(value[1]); //yyyy-mm-dd
        if (d2< d1) {
            get_message_details("JMSG017"); // Get message details
            var display = msg_type.messages_id_desc;
            document.getElementById("id_error_msg").innerHTML = display;
            document.getElementById("id_error_msg").style.color = "Red";
            $('#id_save_confirm_popup').modal('hide');
            $('#myModal').modal('show');
            date_error = 'Y'
        }
    })
    return date_error
}