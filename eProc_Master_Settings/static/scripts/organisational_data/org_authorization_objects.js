var authobj_data = new Array();
var validate_add_attributes = [];
var auth_obj={};


/// on click copy icon display the selected checkbox data
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


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_auth_obj_code").prop("hidden", true);
    $("#id_error_msg_auth_obj_level").prop("hidden", true);
    $("#id_error_msg_auth_obj_length").prop("hidden", true);
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

// on click add icon display the row in to add the new entries
function add_popup_row() {
    dropdown_value();
     $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    var getid = $(".authobject:last").attr("id");
    var getindex = getid.split("-")[1]
    var inc_index = Number(getindex)+1
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control authobject" id="authobject-'+inc_index+'" name="authobject" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ auth_obj_id_dropdown +'</select></td>'+
   '<td><input class="form-control description" type="text" id="description-'+inc_index+'" name="description" disabled></td>'+'<td><select id="authobject_type" name="authobject_type"  class="input form-control">'+auth_type_dropdown+'</select></td>'+
   '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "auth_obj_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_auth_obj_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_auth_obj_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.auth_obj_id + '</td><td>' + item.auth_level_ID + '</td><td>' + item.auth_level + '</td><td hidden>'+ item.del_ind +'</td>/tr>';
    });
    $('#id_auth_obj_tbody').append(edit_basic_data);
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

function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var auth_obj_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        auth_obj_id = row.find("TD").eq(1).find("select option:selected").val().toUpperCase();


        if (auth_obj_code_check.includes(auth_obj_id)) {
            $(row).remove();
        }

        auth_obj_code_check.push(auth_obj_id);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        auth_obj = {};
        auth_obj.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        auth_obj.auth_obj_id = row.find("TD").eq(1).find("select option:selected").val();
        auth_obj.auth_level_ID = row.find("TD").eq(2).find("input").val();
        auth_obj.auth_level = row.find("TD").eq(3).find("select option:selected").val();

        if (auth_obj == undefined) {
            auth_obj.auth_obj_id = row.find("TD").eq(1).find("select option:selected").val();
        }
        validate_add_attributes.push(auth_obj.auth_obj_id);
        authobj_data.push(auth_obj);
    });


    $('#id_save_confirm_popup').modal('show');
});

