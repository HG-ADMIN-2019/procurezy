var org_attr_level_data = new Array();
var validate_add_attributes = [];
var org_attr_level = {};
var duplicate_entry = [];


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_org_attr_code").prop("hidden", true);
    $("#id_error_msg_org_attr_name").prop("hidden", true);
    $("#id_error_msg_org_attr_length").prop("hidden", true);
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


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var org_attr_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        node_type = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();

        if (org_attr_code_check.includes(attribute_id)) {
            $(row).remove();
        }
        org_attr_code_check.push(attribute_id);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];
    duplicate_entry = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        org_attr_level.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        org_attr_level.node_type = row.find("TD").eq(1).find('select').val();
        org_attr_level.node_values = row.find("TD").eq(2).find('select').val();
        org_attr_level.org_model_nodetype_config_guid = row.find("TD").eq(3).find('input').val();

        if (org_attr_level == undefined) {
            org_attr_level.node_type = row.find("TD").eq(1).find('input[type="text"]').val();
        }

         if(org_attr_level.org_model_nodetype_config_guid == undefined) {
                org_attr_level.org_model_nodetype_config_guid = '';
            }
           var org_attr_level_dup = {};
            org_attr_level_dup.node_type = org_attr_level.node_type;
            org_attr_level_dup.node_values = org_attr_level.node_values;
            duplicate_entry.push(org_attr_level_dup);

        validate_add_attributes.push(org_attr_level.node_type);
        org_attr_level_data.push(org_attr_level);
    });


    $('#id_save_confirm_popup').modal('show');
});



// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    $("#error_msg_id").css("display", "none")
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html(" ");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+nodetype_dropdown+'</select></td><td><select class="form-control">'+attributelevel_id_dropdown+'</select></td><td hidden>pgroup_guid</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "org_attr_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}



