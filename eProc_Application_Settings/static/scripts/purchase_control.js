var purhcase_control_data = new Array();
var validate_add_attributes = [];
var purchase_control = {};


// on click copy icon display the selected checkbox data
//function onclick_copy_button() {
//    GLOBAL_ACTION = "COPY"
//    onclick_copy_update_button("copy")
//    document.getElementById("id_del_add_button").style.display = "block";
//}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    $('#display_basic_table').DataTable().destroy();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();

    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var unique_input = '';
    var dropdown_val = [];

    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            var Status = row.cells[3].innerHTML;
            dropdown_val.push([ Status ])
            if (GLOBAL_ACTION == "UPDATE") {
                   guid = row.cells[4].innerHTML;
               edit_basic_data += 
               `<tr>
                    <td hidden><input type="checkbox" required></td>
                    <td>
                        <select type="text" class="input form-control" value= ${row.cells[1].innerHTML} disabled>
                            <option>${row.cells[1].innerHTML}</option>
                        </select>
                    </td>
                    <td>
                        <select type="text" class="input form-control" value= ${row.cells[2].innerHTML} disabled>
                            <option>${row.cells[2].innerHTML}</option>
                        </select>
                    </td>
                    <td><select type="text" class="input form-control">${activate_dropdown}</select></td>
                    <td hidden><input type="text" class= "form-control" value= ${guid}></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td>
                </tr>`;
                
                $("#header_select").prop("hidden", true);
            }
            else {

                unique_input = '<select class="form-control">' + row.cells[1].innerHTML + '</select>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td><td><select type="text" class="input form-control">'+unique_input+'</select></td><td><select type="text" class="input form-control">' + row.cells[2].innerHTML + '</select></td><td hidden></td></tr>';
                $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var Status = dropdown_val[i][0]

        $(row.find("TD").eq(3).find("select option[value=" + Status + "]")).attr('selected', 'selected');


        i++;
    });
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#myModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
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
    //$("p").css("color", "red");
    //document.getElementById("error_message").innerHTML = error_message;
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
            purchase_contrl.company_id = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(purchase_contrl.company_id);
        purhcase_control_data.push(purchase_contrl);
    });
    $('#id_save_confirm_popup').modal('show');
});