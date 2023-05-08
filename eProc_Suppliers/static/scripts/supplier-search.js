// Script to generate sort and filter feature for tables
$(document).ready( function() {
//  table_sort_filter_export_excel();
  $('#name1').val(localStorage.getItem("name1"));
  $('#name2').val(localStorage.getItem("name2"));
  $('#supplier_id').val(localStorage.getItem("supplier_id"));
  $('#email').val(localStorage.getItem("email"));
  $('#supplier_type').val(localStorage.getItem("supplier_type"));
  $('#city').val(localStorage.getItem("city"));
  $('#country_code').val(localStorage.getItem("country_code"));
  $('#porg').val(localStorage.getItem("porg"));
  if(localStorage.getItem("purchase_block") == "true"){
        $('#purchase_block').prop("checked", true)
   }
   else{ $('#purchase_block').prop("checked", false)}
  nav_bar_admin();
});

$("#porg").change(function () {
    if(document.getElementById("porg").value != '*'){

    }
})