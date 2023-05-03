var address_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var address={};

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

// on click copy icon display the selected checkbox data
function onclick_upload_button() {
    GLOBAL_ACTION = "address_upload"    
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}
//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");   
    $("#id_error_msg").empty();
    $('#address_details').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_address").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// on click edit icon display the data in edit mode
function onclick_edit_button() {
    //display the add,cancel and upload buttons and select all checkbox,select heading and checkboxes for each row
    $('#display_basic_table').DataTable().destroy();
    $("#hg_select_checkbox").prop("hidden", false);
    $(".class_select_checkbox").prop("hidden", false);
    //hide the edit,delete,copy and update buttons
    $('#id_cancel_data').show();
    $('#id_edit_data').hide();
    $('#id_check_all').show();
    table_sort_filter('display_basic_table');
}

//**************************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');

}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#address_add_details').modal('hide');
    $('#id_popup_table').DataTable().destroy();
    validate_add_attributes = [];
    address_data = new Array();
    var user_data_dict = {}
    user_data_dict.address_number = $('#id_add_addresses_address_number').val();
    user_data_dict.title = $('#id_add_addresses_title').val();
    user_data_dict.name1= $('#id_add_addresses_name1').val();
    user_data_dict.name2= $('#id_add_addresses_name2').val();
    user_data_dict.street= $('#id_add_addresses_street').val();
    user_data_dict.area= $('#id_add_addresses_area').val();
    user_data_dict.landmark=$('#id_add_addresses_landmark').val();
    user_data_dict.city= $('#id_add_addresses_city').val();
    user_data_dict.address_partner_type= $('#id_add_addresses_partnertype').val();
    user_data_dict.org_address_source_system= $('#id_add_addresses_source').val();
    user_data_dict.postal_code= $('#id_add_addresses_postalcode').val();
    user_data_dict.region= $('#id_add_addresses_region').val();
    user_data_dict.mobile_number= $('#id_add_addresses_mobile_number').val();
    user_data_dict.telephone_number= $('#id_add_addresses_telephone_number').val();
    user_data_dict.fax_number= $('#id_add_addresses_fax_number').val();
    user_data_dict.email= $('#id_add_addresses_email').val();
    user_data_dict.country_code= $('#id_add_addresses_country_code').val();
    user_data_dict.language_id= $('#id_add_addresses_language_id').val();
    user_data_dict.time_zone= $('#id_add_addresses_time_zone').val();
    user_data_dict.del_ind= $('#id_add_addresses_del_ind_flag').val();
    var user_data_dict_compare =  user_data_dict.address_number
    if(user_data_dict.del_ind = 'false'){
        user_data_dict.del_ind = 'False'
    }
    user_data_dict.address_guid= $('#id_add_addresses_address_guid').val();
    if (user_data_dict == undefined) {
        user_data_dict.address_number = $('#id_addresses_address_number').val();
    }
    if(user_data_dict.address_guid== undefined) {
        user_data_dict.address_guid= ''
    }
    validate_add_attributes.push(user_data_dict_compare);
    address_data.push(user_data_dict);
    $('#id_save_confirm_popup').modal('show');
    table_sort_filter('id_popup_table');
});

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $.each(rendered_address_data, function (i, item) {
        var main_attribute = {};
        main_attribute.address_number = item.address_number;
        var main_compare =  main_attribute.address_number
        main_table_low_value.push(main_compare);
    });
    table_sort_filter('display_basic_table');
}


