var orgattr_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var org_attr={};

    // on click update icon display the selected checkbox data to update
    function onclick_update_button() {
        GLOBAL_ACTION = "UPDATE"
        onclick_copy_update_button("UPDATE")
        document.getElementById("id_del_add_button").style.display = "none";
    }

    //******************************
    function onclick_delete_button() {
        GLOBAL_ACTION = "DELETE"
        onclick_copy_update_button("DELETE")
        document.getElementById("id_del_add_button").style.display = "none";
    }

    // //************************************
    // function onclick_copy_update_button(data) {
    //     $('#display_basic_table').DataTable().destroy();
    //     $('#id_popup_table').DataTable().destroy();
    //     $("#id_popup_tbody").empty();
    //     $("#error_msg_id").css("display", "none");
    //     //Reference the Table.
    //     var grid = document.getElementById("display_basic_table");
    //     //Reference the CheckBoxes in Table.
    //     var checkBoxes = document.getElementsByClassName("checkbox_check");
    //     var edit_basic_data = "";
    //     var dropdown_values = [];
    //     dropdown_value();
    //     //Loop through the CheckBoxes.
    //     for (var i = 0; i < checkBoxes.length; i++) {
    //         if (checkBoxes[i].checked) {
    //             var row = checkBoxes[i].parentNode.parentNode;
    //             if(GLOBAL_ACTION == "UPDATE"){
    //                 edit_basic_data +=  '<tr><td hidden><input type="checkbox" required></td>'+
    //                 '<td><select type="text" class="input form-control" id="attributeid"  name="attributeid"  disabled><option>'+ row.cells[1].innerHTML +'</option></select></td>'+
    //                 '<td><input class="form-control attribute_name" type="text" value="' + row.cells[2].innerHTML + '" name="attribute_name" id="attribute_name-1" disabled></td>'+
    //                 '<td><input type="checkbox"  name="range_indicator" required></td>'+
    //                 '<td><input type="checkbox"  name="multiple_value" required></td>'+
    //                 '<td><input type="checkbox" name="allow_defaults" required></td>'+
    //                 '<td><input type="checkbox"  name="inherit_values" required></td>'+
    //                 '<td><input type="number" value="' + row.cells[7].innerHTML + '" name="maxlength"></td>'+
    //                 '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
    //                 '<td class="class_del_checkbox1" hidden><input type="checkbox" required></td></tr>';
    //                  $("#header_select").prop("hidden", true);
    //             }
    //             else if (GLOBAL_ACTION == "DELETE"){
    //                 if ((row.cells[8].innerHTML=="False") || (row.cells[8].innerHTML=="false")){
    //                     check = '<input type="checkbox" disabled>'
    //                     $('#delete_data').prop('disabled', true);
    //                 }
    //                 else
    //                 {
    //                     check = '<input type="checkbox">'
    //                     $('#delete_data').prop('disabled', false);
    //                 }
    //                 unique_input = '<input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="prod_cat_id" onkeypress="return /[0-9]/i.test(event.key)" maxlength="20" style="text-transform:uppercase" required>'
    //                 edit_basic_data += '<tr><td>'+check+'</td><td>'+unique_input+'</td>'+
    //                 '<td><input type="text" class="form-control" value="' + row.cells[2].innerHTML + '" name="prod_cat_desc" onkeypress="return /[a-z ]/i.test(event.key)" maxlength="100" required></td>'+
    //                 '<td><input type="checkbox"  name="range_indicator" required></td><td><input type="checkbox"  name="multiple_value" required></td>'+
    //                 '<td><input type="checkbox" name="allow_defaults" required></td><td><input type="checkbox"  name="inherit_values" required></td>'+
    //                 '<td><input type="number" value="' + row.cells[7].innerHTML + '" name="maxlength"></td>'+
    //                 '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
    //                 '<td class="id_del_ind_checkbox1" hidden><input type="text" name = "del_ind_flag" value="' + row.cells[8].innerHTML + '"></td></tr>';
    //                 $("#header_select").prop("hidden", false);
    //             }
    //             var attribute = row.cells[1].innerHTML;
    //             var range_indicator = row.cells[3].children.range_indicator.checked
    //             var multiple_value = row.cells[4].children.multiple_value.checked
    //             var allow_defaults = row.cells[5].children.allow_defaults.checked
    //             var inherit_values = row.cells[6].children.inherit_values.checked
    //             dropdown_values.push([attribute,range_indicator,multiple_value,allow_defaults,inherit_values])
    //         }
    //     }
    //     $('#id_popup_tbody').append(edit_basic_data);
    //     var i = 0;
    //     $("#id_popup_table TBODY TR").each(function () {
    //         var row = $(this);
    //         var attribute = dropdown_values[i][0];
    //         var range_indicator = dropdown_values[i][1];
    //         var multiple_value = dropdown_values[i][2];
    //         var allow_defaults = dropdown_values[i][3];
    //         var inherit_values = dropdown_values[i][4];
    //         if(range_indicator) {
    //             $(row.find("TD").eq(3).find('input[name="range_indicator"]').attr('checked', 'checked'));
    //         }
    //         if(multiple_value) {
    //             $(row.find("TD").eq(4).find('input[name="multiple_value"]').attr('checked', 'checked'));
    //         }
    //         if(allow_defaults) {
    //             $(row.find("TD").eq(5).find('input[name="allow_defaults"]').attr('checked', 'checked'));
    //         }
    //         if(inherit_values) {
    //             $(row.find("TD").eq(6).find('input[name="inherit_values"]').attr('checked', 'checked'));
    //         }
    //         i++;
    //       });
    //         display_button();
    //         $("#id_del_ind_checkbox").prop("hidden", true);
    //         table_sort_filter("id_popup_table");
    //         table_sort_filter('display_basic_table');
    //         $('#org_attr_Modal').modal('show');
    // }

    //***************************
    function display_button(){
        if(GLOBAL_ACTION == "DELETE"){
            $('#delete_data').show();
            $('#save_id').hide();
        }
        else{
            $('#delete_data').hide();
            $('#save_id').show();
        }
    }

    //onclick of cancel empty the popup table body and error messages
    $(".remove_upload_data").click(() => {
        $("#id_error_msg").html("");
        $("#id_popup_tbody").empty();
        $("#id_error_msg").empty();
        $('#org_attr_Modal').modal('hide');
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

    //**************************************
    function display_error_message(error_message){
        $('#error_message').text(error_message);
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#org_attr_Modal').modal('show');
    }

    //onclick of cancel display the table in display mode............
    function display_basic_db_data() {
        $('#display_basic_table').DataTable().destroy();
        $('#id_org_attr_tbody').empty();
        var edit_basic_data = '';
        $.each(rendered_org_attr_data, function (i, item) {
            var data = '';
            var data1 = '';
            var data2 = '';
            var data3 = '';
            if (item.range_indicator == true){
                data = '<input type="checkbox" name="range_indicator" value="" checked disabled>'
            } else{
                data = '<input type="checkbox" name="range_indicator" value="" disabled>'
            }
            if (item.multiple_value == true){
                data1 = '<input type="checkbox" name="multiple_value" value="" checked disabled>'
            } else{
                data1 = '<input type="checkbox" name="multiple_value" value="" disabled>'
            }
             if (item.allow_defaults == true){
                data2 = '<input type="checkbox" name="allow_defaults" value="" checked disabled>'
            } else{
                data2 = '<input type="checkbox" name="allow_defaults" value="" disabled>'
            }
            if (item.inherit_values == true){
                data3 = '<input type="checkbox" name="inherit_values" value="" checked disabled>'
            } else{
                data3 = '<input type="checkbox" name="inherit_values" value="" disabled>'
            }
            edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.attribute_id + '</td><td>' + item.attribute_name + '</td>'+
            '<td>' + data + '</td>' +
            '<td>' + data1 + '</td>' +
            '<td>' + data2 + '</td>' +
            '<td>' + data3 + '</td>' +
            '<td>' + item.maximum_length + '</td>' +
            '<td hidden> '+ item.del_ind_flag+'</td></tr>';
        });
        $('#id_org_attr_tbody').append(edit_basic_data);
        $("#hg_select_checkbox").prop("hidden", true);
        $(".class_select_checkbox").prop("hidden", true);
        $('input.checkbox_check:checkbox').removeAttr('checked');
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

    //**********************************
    function delete_duplicate() {
        $('#id_popup_table').DataTable().destroy();
        var org_attr_code_check = new Array
        $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            //*************** reading data from the pop-up ***************
            attribute_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
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
        $('#org_attr_Modal').modal('hide');
        orgattr_data = read_popup_data();
        $('#id_save_confirm_popup').modal('show');
    });

    //Read popup table data
    function read_popup_data() {
        $('#id_popup_table').DataTable().destroy();
        validate_add_attributes = [];
        orgattr_data = [];
        $("#id_popup_table TBODY TR").each(function() {
            var row = $(this);
            org_attr = {};
            org_attr.del_ind_flag = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
            org_attr.del_ind = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
            org_attr.attribute_id = row.find("TD").eq(1).find('select[type="text"]').val();
            org_attr.attribute_name = row.find("TD").eq(2).find('input[type="text"]').val();
            org_attr.range_indicator =row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
            org_attr.multiple_value = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
            org_attr.allow_defaults = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            org_attr.inherit_values =row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
            org_attr.maximum_length = row.find("TD").eq(7).find('input[type="number"]').val();
            if (org_attr == undefined) {
                org_attr.attribute_id = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            validate_add_attributes.push(org_attr.attribute_id);
            orgattr_data.push(org_attr);
        });
        table_sort_filter('id_popup_table');
        return orgattr_data;
    }

    // Function to get main table data
    function get_main_table_data() {
        main_table_low_value = [];
        $('#display_basic_table').DataTable().destroy();
        $("#display_basic_table TBODY TR").each(function() {
            var row = $(this);
            var main_attribute = {};
            main_attribute.attribute_id = row.find("TD").eq(1).html();
            main_table_low_value.push(main_attribute.attribute_id);
        });
        table_sort_filter('display_basic_table');
    }

    // Function to get the selected row data
    function get_selected_row_data() {
        $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var org_attr_arr_obj = {};
        var checked_box = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        disable_check = row.find("TD").eq(8).find('input[type="text"]').val();
        if(checked_box)
        {
            org_attr_arr_obj.del_ind_flag = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
            org_attr_arr_obj.del_ind = checked_box;
            org_attr_arr_obj.attribute_id = row.find("TD").eq(1).find('input[type="text"]').val();
            org_attr_arr_obj.attribute_name = row.find("TD").eq(2).find('input[type="text"]').val();
            org_attr_arr_obj.range_indicator = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
            org_attr_arr_obj.multiple_value = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
            org_attr_arr_obj.allow_defaults = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            org_attr_arr_obj.inherit_values = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
            org_attr_arr_obj.maximum_length = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
            main_table_org_attr_checked.push(org_attr_arr_obj);
        }
    });
}

    // Function for add a new row data
    function new_row_data() {
        basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select type="text" class="input form-control attribute" id="attribute-1"  name="attribute">'+ attribute_id_dropdown +'</select></td><td><input class="form-control attribute_name" type="text" name="attribute_name" id="attribute_name-1" disabled></td><td><input type="checkbox" name="range_indicator" required></td><td><input type="checkbox" name="multiple_value" required></td><td><input type="checkbox" name="allow_defaults" required></td><td><input type="checkbox" name="inherit_values" required></td><td><input type="number" name="maxlength"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
        var attributeSelect = $("#attribute-1");
        GetSelectedTextValue(attributeSelect[0]);
    }


    //Get message for check data function
    function get_msg_desc_check_data(msg){
        var msg_type ;
        msg_type = message_config_details(msg);
        $("#error_msg_id").prop("hidden", false);
        return msg_type.messages_id_desc;
    }