
var encrypted_supplier

// Global variable - supplier id
var global_supplier_id = document.getElementById('supplier_id').value

// Global variable - delete supplier purchasing info
var delete_supp_purch_data = []

// Global variable - supplier purchasing data
var supplier_org_data = new Array();
$("#display_basic_org_table TBODY TR").each(function() {
    var row = $(this);
    var save_supp_org_data = {};
    save_supp_org_data.supp_id = global_supplier_id;
    save_supp_org_data.supp_org_guid = row.find("TD").eq(0).text().trim();
    save_supp_org_data.porg_id = row.find("TD").eq(1).text().trim();
    save_supp_org_data.currency_id = row.find("TD").eq(2).text().trim();
    save_supp_org_data.payment_term = row.find("TD").eq(3).text().trim();
    save_supp_org_data.incoterm = row.find("TD").eq(4).text().trim();
    save_supp_org_data.gr_inv_vrf = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.inv_conf_exp = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.gr_conf_exp = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.po_resp = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.ship_notif_exp = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.purch_block = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
    supplier_org_data.push(save_supp_org_data)
    console.log(save_supp_org_data)
})


// Makes the supplier basic data fields editable
function edit_basic_supp_data(){
    $('#supplier_basic_update_success').hide();
    $(".hg_edit_display_mode").prop( "disabled", false );
//    $(".hg_edit_display_mode").prop("disabled", true);
    if(GLOBAL_ACTION != 'CREATE'){
            $("#supplier_id").prop( "disabled", true );
            $("#sbd_edit_button").prop("hidden", true);
            document.getElementById('sbd_save_cancel_button').style.display = 'block';
            $("#working_days").show();
    }
    $("#edit_mode").show();
    $("#working_days").hide();
     $("#edit_mode").prop("hidden", false);
    document.getElementById('sbd_edit_button').style.display = 'none' ;
    $("#sbd_edit_button").prop("hidden", true);
    document.getElementById('sbd_save_cancel_button').style.display = 'block';
    $("#sbd_save_cancel_button").prop("hidden", false);
}

// onclick of cancel button functionality
function cancel_basic_details(){
    $(".hg_edit_display_mode").prop( "disabled", true );
    document.getElementById('sbd_save_cancel_button').style.display = 'none'
    document.getElementById('sbd_edit_button').style.display = 'block'
    $("#sbd_edit_button").prop("hidden", false);
    $('#image-preview').hide();
    $('#image-preview3').show();
    var output = document.getElementById('image-preview3');
    output.src = img_url;
}

// Function to edit supplier purchasing details data
function edit_supp_org(){
    var supp_org_body_data = '';
// -----------------------------------------------
    $('#display_basic_org_table').DataTable().destroy();
    $('#supp_org_body').empty();
    var edit_basic_data = '';
    $.each(rendered_supp_org_data, function (i, item) {
         var gr_inv_vrf_checkbox = '';
        if (item.ir_gr_ind){
            gr_inv_vrf_checkbox += '<input type="checkbox"  checked disabled>'
        } else gr_inv_vrf_checkbox += '<input type="checkbox" disabled>'

        var inv_conf_exp_checkbox = '';
        if(item.ir_ind){
            inv_conf_exp_checkbox += '<input type="checkbox"  checked disabled>'
        } else inv_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var gr_conf_exp_checkbox = '';
        if(item.gr_ind){
            gr_conf_exp_checkbox += '<input type="checkbox"  checked disabled>'
        } else gr_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var po_resp_checkbox = '';
        if(item.po_resp){
            po_resp_checkbox += '<input type="checkbox"  checked disabled>'
        } else po_resp_checkbox += '<input type="checkbox" disabled>'

        var ship_notif_exp_checkbox = ''
        if(item.ship_notif_exp){
            ship_notif_exp_checkbox += '<input type="checkbox"  checked disabled>'
        } else ship_notif_exp_checkbox += '<input type="checkbox" disabled>'

        var purch_block_checkbox = ''
        if(item.purch_block){
            purch_block_checkbox += '<input type="checkbox"  checked disabled>'
        } else purch_block_checkbox += '<input type="checkbox" disabled>'

        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check"  onclick="valueChanged()" type="checkbox"></td>'+
         '<td hidden>'+item.guid+'</td>'+
         '<td>'+item.porg_id+'</td>'+
         '<td>'+item.currency_id_id+'</td>'+
         '<td>'+item.payment_term_key+'</td>'+
         '<td>'+item.incoterm_key_id+'</td>'+
         '<td>'+gr_inv_vrf_checkbox+'</td>'+
         '<td>'+inv_conf_exp_checkbox+'</td>'+
         '<td>'+gr_conf_exp_checkbox+'</td>'+
         '<td>'+po_resp_checkbox+'</td>'+
         '<td>'+ship_notif_exp_checkbox+'</td>'+
         '<td>'+purch_block_checkbox+'</td></tr>';
    });
    $('#supp_org_body').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $("#id_check_all").prop("hidden", false);
    $(".class_select_checkbox").prop("hidden", true);
//    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    table_sort_filter('display_basic_org_table');
}

// Function to cancel Edit operation
function cancel_supp_org_data(){
    display_supp_org_header = ''
    display_supp_org_body = ''
    $('#supp_org_header').empty();
    $('#supp_org_body').empty();
    display_supp_org_header = '<tr> <th>Purchasing organisation</th> <th>PO Currency</th> <th>Payment Terms</th> <th>Incoterm</th> <th>GR based invoice verification</th> <th>Invoice confirmation expected</th> <th>GR confirmation expected</th> <th>PO response</th> <th>Shipping notification expected</th> <th>Purchase block</th></tr>'
    $.each(supplier_org_data, function(index, data){
        var gr_inv_vrf_checkbox = ''
        if (data.gr_inv_vrf==true){
            gr_inv_vrf_checkbox += '<input type="checkbox" checked disabled>'
        } else gr_inv_vrf_checkbox += '<input type="checkbox" disabled>'

        var inv_conf_exp_checkbox = ''
        if(data.inv_conf_exp==true){
            inv_conf_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else inv_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var gr_conf_exp_checkbox = ''
        if(data.gr_conf_exp==true){
            gr_conf_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else gr_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var po_resp_checkbox = ''
        if(data.po_resp==true){
            po_resp_checkbox += '<input type="checkbox" checked disabled>'
        } else po_resp_checkbox += '<input type="checkbox" disabled>'

        var ship_notif_exp_checkbox = ''
        if(data.ship_notif_exp==true){
            ship_notif_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else ship_notif_exp_checkbox += '<input type="checkbox">'

        var purch_block_checkbox = ''
        if(data.purch_block==true){
            purch_block_checkbox += '<input type="checkbox" checked disabled>'
        } else purch_block_checkbox += '<input type="checkbox" disabled>'

        display_supp_org_body += '<tr> <td hidden>'+data.supp_org_guid+'</td> <td>'+data.porg_id+'</td> <td>'+data.currency_id+'</td> <td>'+data.payment_term+'</td> <td>'+data.incoterm+'</td> <td>'+gr_inv_vrf_checkbox+'</td> <td>'+inv_conf_exp_checkbox+'</td> <td>'+gr_conf_exp_checkbox+'</td> <td>'+po_resp_checkbox+'</td> <td>'+ship_notif_exp_checkbox+'</td> <td>'+purch_block_checkbox+'</td></tr> '
    });

    $('#supp_org_header').append(display_supp_org_header);
    $('#supp_org_body').append(display_supp_org_body);
    document.getElementById("id_edit_data").style.display = "block";
    document.getElementById("supp_org_cancel_save").style.display = "none";
}


var supplierid = global_supplier_id;

   // Validation function
   function save_basic_form_validation(name1,name2, city_id, email_id, mobile,search_term1, search_term2){
        var is_valid = true
        var save_form_errors = ''
        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (name1 == '') {
            is_valid = false
             var msg = "JMSG007";
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc + " First name ";
            save_form_errors += display1;
        }
        else if (name2 == '') {
            is_valid = false
             var msg = "JMSG007";
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc+ " Last name";
            save_form_errors += display1;
        }
        else if (city_id == '') {
            is_valid = false
              var msg = "JMSG007" ;
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc;
            save_form_errors += display1 + "City";
        }
        else if ((email_id == '') || !(email_id.match(mailformat))) {
            is_valid = false
              var msg = "JMSG002";
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc;
            save_form_errors += display1 + "Email Id";
        }
        else if (mobile == '') {
            is_valid = false
              var msg = "JMSG007" ;
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc;
            save_form_errors += display1 + " Mobile Number";
        }
        else if (search_term1 == '') {
            is_valid = false
              var msg = "JMSG007";
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc;
            save_form_errors += display1 + " Search Term1";
        }
        else if (search_term2 == '') {
            is_valid = false
              var msg = "JMSG007";
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc;
            save_form_errors += display1 + " Search Term2";
        }
        return [is_valid, save_form_errors]
    }

function enable_disable(action){
    $(".dummy_ft_button_class").hide();
    if(action == 'EDIT'){
        $("#ft_save").show();
        $("#ft_cancel").show();
        $('.toggle_mode').prop('disabled', false)
    }
    else{
        $("#ft_edit").show();
        $('.toggle_mode').prop('disabled', true)
    }
}


// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" class="checkbox_check" onclick="valueChanged();" required></td>'+
    '<td hidden><input type="text" name="supp_org_guid"></td>'+
    '<td><select class="form-control"  type="text"  name="porg_id" style="text-transform:uppercase;">'+porg_opt+'</select></td>'+
    '<td><select class="form-control" type="text"  name="currency_id">'+currency_opt1+'</select></td>'+
    '<td><select class="form-control" type="text"  name="payment_term">'+payterm_opt+'</select></td>'+
    '<td><select class="form-control" type="text"  name="incoterm">'+incoterm_opt+'</select></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="gr_inv_vrf_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="inv_conf_exp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="gr_conf_exp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="po_resp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="ship_notif_exp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="purch_block_checkbox" required></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
}
//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_org_table').DataTable().destroy();
    $('#supp_org_body').empty();
    var edit_basic_data = '';
    $.each(rendered_supp_org_data, function (i, item) {
        var gr_inv_vrf = '', inv_conf_exp = '', gr_conf_exp = '', po_resp = '', ship_notif_exp='', purch_block='';
        if (item.gr_ind == true){
                gr_inv_vrf = '<input type="checkbox" name="gr_inv_vrf" value="" checked disabled>'
        } else{
                gr_inv_vrf = '<input type="checkbox" name="gr_inv_vrf" value="" disabled>'
        }
        if (item.ir_ind == true){
                inv_conf_exp = '<input type="checkbox" name="inv_conf_exp" value="" checked disabled>'
        } else{
                inv_conf_exp = '<input type="checkbox" name="inv_conf_exp" value="" disabled>'
        }
         if (item.ir_gr_ind == true){
                gr_conf_exp = '<input type="checkbox" name="gr_conf_exp" value="" checked disabled>'
        } else{
                gr_conf_exp = '<input type="checkbox" name="gr_conf_exp" value="" disabled>'
        }
         if (item.po_resp == true){
                po_resp = '<input type="checkbox" name="po_resp" value="" checked disabled>'
        } else{
                po_resp = '<input type="checkbox" name="po_resp" value="" disabled>'
        }
        if (item.ship_notif_exp == true){
                ship_notif_exp = '<input type="checkbox" name="ship_notif_exp" value="" checked disabled>'
        } else{
                ship_notif_exp = '<input type="checkbox" name="ship_notif_exp" value="" disabled>'
        }
        if (item.purch_block == true){
                purch_block = '<input type="checkbox" name="purch_block" value="" checked disabled>'
        } else{
                purch_block = '<input type="checkbox" name="purch_block" value="" disabled>'
        }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
        '<td>' + item.porg_id + '</td>'+
        '<td>' + item.currency_id + '</td>'+
        '<td>' + item.payment_term_key + '</td>'+
        '<td>' + item.incoterm_key + '</td>'+
        '<td>' + gr_inv_vrf + '</td>'+
        '<td>' + inv_conf_exp + '</td>'+
        '<td>' + gr_conf_exp+ '</td>'+
        '<td>' + po_resp + '</td>'+
        '<td>' + ship_notif_exp + '</td>'+
        '<td>' + purch_block + '</td>'+
        '</tr>';
    });
    $('#supp_org_body').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
//    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    $('#id_check_all').hide();
    table_sort_filter('display_basic_org_table');
}
// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_org_table TBODY TR").each(function () {
        var row = $(this);
        var supp_arr_obj ={};
        supp_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(supp_arr_obj.del_ind){
            supp_arr_obj.supp_id = supplierid;
        supp_arr_obj.supp_org_guid = row.find("TD").eq(1).html();
        supp_arr_obj.porg_id = row.find("TD").eq(2).html();
        supp_arr_obj.currency_id = row.find("TD").eq(3).html();
        supp_arr_obj.payment_term = row.find("TD").eq(4).html();
        supp_arr_obj.incoterm = row.find("TD").eq(5).html();
        supp_arr_obj.gr_inv_vrf = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.inv_conf_exp = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.gr_conf_exp = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.po_resp = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.ship_notif_exp = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.purch_block = row.find("TD").eq(11).find('input[type="checkbox"]').is(':checked');
            main_table_supp_checked.push(supp_arr_obj);
        }
    });
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("UPDATE")
    document.getElementById("id_del_add_button").style.display = "none";
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html(" ");
    });
    new_row_data();   // Add a new row in popup
    if (GLOBAL_ACTION == "country_upload") {
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    table_sort_filter('id_popup_table');
    $('#delete_data').hide()
}
