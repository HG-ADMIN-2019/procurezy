var po_split_criteria_data = new Array();
var validate_add_attributes = [];
var po_split_criteria={};
//**************************************


//**********************************
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "client_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

//******************
// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}

//***********************************
// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//**********************************************************
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
            var activate = row.cells[3].innerHTML
            dropdown_val.push([ activate])
            if(GLOBAL_ACTION == "UPDATE"){
                 guid = row.cells[4].innerHTML;
              edit_basic_data += '<tr ><td hidden><input type="checkbox" required></td><td><input class="form-control" id ="' + row.cells[1].id + '"   value="' + row.cells[1].innerHTML + '" type="text" disabled></td><td><input class="form-control"  value="' + row.cells[2].innerHTML + '" type="text" disabled></td><td><select type="text" class="input form-control">'+ activate_dropdown +'</select></td><td hidden><input type="text" class= "form-control" value="' +  guid  + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';

               $("#header_select").prop("hidden", true);
            }
            else{
               unique_input = '<input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="client code" onkeypress="return /[A-Z0-9]/i.test(event.key)" maxlength="8" style="text-transform:uppercase" required>'

               edit_basic_data += '<tr ><td ><input type="checkbox" required></td><td>'+unique_input+'</td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z 0-9]/i.test(event.key)" name="description"  maxlength="30"  required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
               $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_tbody').append(edit_basic_data);
   var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
       var activate = dropdown_val[i][0]

       $(row.find("TD").eq(3).find("select option[value=" + activate + "]")).attr('selected', 'selected');


        i++;
    })
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
    $("#id_error_msg_client").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_client_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();

});





//deletes he duplicate data
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var po_split_criteria_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
        company_code_id = row.find("TD").eq(2).find('select[type="text"]').val();
        activate = row.find("TD").eq(3).find('select[type="text"]').val();
        checked_box = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked')


        if (po_split_criteria_check.includes(po_split_criteria)) {
            $(row).remove();
        }

        po_split_criteria_check.push(po_split_criteria);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}
// //Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    po_split_criteria_data = new Array();
     validate_add_attributes = [];

         if(GLOBAL_ACTION == "UPDATE"){
             $("#id_popup_table TBODY TR").each(function () {
                    var row = $(this);
                    po_split_criteria={};
                    po_split_criteria.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
                    po_split_criteria.activate = row.find("TD").eq(3).find('select[type="text"]').val();
                    var data = '';
                    if (po_split_criteria.activate == 'Activate'){
                        data = true
                    } else{
                        data = false
                    }

                    po_split_criteria.activate  = data;
                    po_split_criteria.company_code_id = row.find("TD").eq(2).find('input[type="text"]').val();
                    po_split_criteria.po_split_type = row.find("TD").eq(1).find('input[type="text"]').attr('id');
                    po_split_criteria.po_split_criteria_guid = row.find("TD").eq(4).find('input[type="text"]').val();

                    if (po_split_criteria == undefined){
                        po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
                    }


                    var compare = po_split_criteria.po_split_type + '-' + po_split_criteria.company_code_id + '-' + po_split_criteria.activate
                    validate_add_attributes.push(compare);
                    po_split_criteria_data.push(po_split_criteria);
                });

         }
         else{
            $("#id_popup_table TBODY TR").each(function () {
                    var row = $(this);
                    po_split_criteria={};
                    po_split_criteria.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
                    po_split_criteria.activate = row.find("TD").eq(3).find('select[type="text"]').val();
                    po_split_criteria.company_code_id = row.find("TD").eq(2).find('select[type="text"]').val();
                    po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
                    po_split_criteria.po_split_criteria_guid = row.find("TD").eq(4).find('input[type="text"]').val();

                    if (po_split_criteria == undefined){
                        po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
                    }
                       var data = '';
                    if (po_split_criteria.activate == 'Activate'){
                        data = true
                    } else{
                        data = false
                    }
                    po_split_criteria.activate  = data;

                    var compare = po_split_criteria.po_split_type + '-' + po_split_criteria.company_code_id + '-' + po_split_criteria.activate
                    validate_add_attributes.push(compare);
                    po_split_criteria_data.push(po_split_criteria);
                });
         }




    $('#id_save_confirm_popup').modal('show');
});
function display_error_message(error_message){

        $('#error_message').text(error_message);
        //$("p").css("color", "red");
        //document.getElementById("error_message").innerHTML = error_message;
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}

