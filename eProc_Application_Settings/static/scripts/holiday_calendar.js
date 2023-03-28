var calendar_data_array = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];

// to fetch current date
const date = new Date();
let day = date.getDate();
let month = date.getMonth() + 1;
let year = date.getFullYear();
let currentDate = `${year}-${month}-${day}`; 

//Date picker format
var GLOBAL_CALENDER_ID = '';
function DatePicker() {
    $('#yearPicker').datepicker({
        format: "yyyy",
        viewMode: "years",
        minViewMode: "years"
    });
}

function MultipleSelect() {
    $('#working_days').selectpicker();
}

var dateToday = new Date();
function HolidayDatePicker() {
    $('#from_date, #to_date,.from_date,.to_date').datepicker({
        format: "yyyy-mm-dd",
        startDate: new Date()
    });
}

// on click edit icon display the data in edit mode
 function onclick_holiday_edit_button() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_cancel_data').show();
    $('#id_edit_data').hide();
    $(".maintain-calendar-holiday-config").prop("hidden", false);
    $('.view-calendar-holiday-config').hide();
    table_sort_filter('display_basic_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#holidayModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_calendar_code").prop("hidden", true);
    $("#id_error_msg_calendar_name").prop("hidden", true);
    $("#id_error_msg_calendar_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function check_date(calendar) {
    var validDate = 'Y';
    var error_message = ''
    $.each(calendar, function (i, item) {
        if ((Date.parse(item.to_date) < Date.parse(item.from_date)) == true) {
            $("#id_error_msg").prop("hidden", false)
            get_message_details("JMSG017"); // Get message details
            $('#id_save_confirm_popup').modal('hide');
            onclick_copy_update_button(item.calender_id);
            $('#holidayModal').modal('show');
            validDate = 'N'
        }
    });
    return [validDate,error_message]
}

function display_error_message(error_message){
    table_sort_filter('render_holiday_data');
    $("#error_msg_id").css("display", "none")
    $('#error_message').text(error_message);
    document.getElementById("error_msg_id").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#holidayModal').modal('show');
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $("#error_msg_id").prop("hidden", true)
    $(".modal").on("hidden.bs.modal", function () {
        $("#error_msg_id").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" name="hg_checkbox">' +
        '<td><input class="holiday_description input" type="text" id="holiday_description" name="holiday_description" onkeypress="return /[a-z 0-9]/i.test(event.key)"></td>' +
        '<td><input type="text" class="from_date input"   name="from_date"></td>' +
        '<td><input  type="text" class="to_date input"  name="to_date"></td>' +
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
        '<td hidden><input class="input" type="text"  name="calender_holiday_guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    HolidayDatePicker();
    if (GLOBAL_ACTION == "calendar_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    MultipleSelect();
}

//onclick of cancel display the table in display mode............
 function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_cancel_data').hide();
    $('#id_edit_data').show();
    $(".maintain-calendar-holiday-config").prop("hidden", true);
    $('.view-calendar-holiday-config').show();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    table_sort_filter('display_basic_table');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    calendar_data_array = read_popup_data(); 
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    calendar_data_array = new Array();
    $('#holidayModal').modal('hide');
    $("#id_popup_table tbody tr").each(function (index) {
        var row = $(this);
        var calendar_object = {};
        guid = row.find("TD").eq(5).find('input[type="text"]').val()
        calendar_object.calender_holiday_guid = row.find("TD").eq(5).find('input[type="text"]').val();
        calendar_object.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        calendar_object.holiday_description = row.find("TD").eq(1).find('input[type="text"]').val();
        calendar_object.from_date = row.find("TD").eq(2).find('input[type="text"]').val();
        calendar_object.to_date = row.find("TD").eq(3).find('input[type="text"]').val();
        calendar_object.calender_id = GLOBAL_CALENDER_ID;
        if (calendar_object.calender_holiday_guid == undefined) {
            calendar_object.calender_holiday_guid = '';
        }
        if (calendar_object == undefined) {
            calendar.holiday_description = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(calendar_object.holiday_description);

        calendar_data_array.push(calendar_object);
    });
    return calendar_data_array;
}

//onclick of delete,delete the row.
function application_settings_delete_Row1(myTable) {
   try {
       var table = document.getElementById(myTable);
       var rowCount = table.rows.length;
       for (var i = 0; i < rowCount; i++) {
           var row = table.rows[i];
           var chkbox = row.cells[0].childNodes[0];
           console.log(chkbox);
           if ( true == chkbox.checked) {
               table.deleteRow(i);
               rowCount--;
               i--;
           }
       }
       $("#id_delete_currency").hide();
       $("#id_copy_currency").hide();
       $("#id_update_currency").hide();
       $("#error_msg_id").css("display", "none");
       return rowCount;
   } catch (e) {
       alert(e);
   }
}

// Function to get main table data
function get_main_table_data() {
    $("#display_basic_table TBODY TR").each(function () {
        main_table_low_value = [];
        var row = $(this);
        var main_attribute = {};
        main_attribute.holiday_description = row.find("TD").eq(2).html();
        main_table_low_value.push(main_attribute.holiday_description);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var calendar_arr_obj = {};
        var isSelect = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(isSelect){
            calendar_arr_obj.holiday_description = row.find("TD").eq(1).find('input[type="text"]').val();
            calendar_arr_obj.from_date = row.find("TD").eq(2).find('input[type="text"]').val();
            calendar_arr_obj.to_date = row.find("TD").eq(3).find('input[type="text"]').val();
            calendar_arr_obj.del_ind = isSelect;
            calendar_arr_obj.calender_holiday_guid = row.find("TD").eq(5).find('input[type="text"]').val();
            calendar_arr_obj.calender_id = GLOBAL_CALENDER_ID;
            main_table_calendar_checked.push(calendar_arr_obj);
        }
    });
}

// Function to get main table data
function get_main_table_data(){
main_table_low_value = [];
$('#display_basic_table').DataTable().destroy();
        var calendar = {};
        $('#display_basic_table').DataTable().destroy();
        $("#display_basic_table TBODY TR").each(function () {
            var row = $(this);
            var main_attribute = {};
            main_attribute.holiday_description = row.find("TD").eq(2).html();
            main_table_low_value.push(main_attribute.holiday_description);
        });
        table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data(){
$("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var calendar_arr_obj = {};
        var isSelect = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(isSelect){
            calendar_arr_obj.holiday_description = row.find("TD").eq(1).find('input[type="text"]').val();
            calendar_arr_obj.from_date = row.find("TD").eq(2).find('input[type="text"]').val();
            calendar_arr_obj.to_date = row.find("TD").eq(3).find('input[type="text"]').val();
            calendar_arr_obj.del_ind = isSelect;
            calendar_arr_obj.calender_holiday_guid = row.find("TD").eq(5).find('input[type="text"]').val();
            calendar_arr_obj.calender_id = GLOBAL_CALENDER_ID;
            main_table_calendar_checked.push(calendar_arr_obj);
        }
    });
}