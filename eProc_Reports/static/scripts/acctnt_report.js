    // Script to generate sort and filter feature for tables
    $(document).ready(function () {
        table_sort_filter_export_excel();
        nav_bar_admin();
        // Loader implementation on search button
        $('#hg_accnt_report_search').click(function () {
            $('#hg_loader').modal('show');
        });
//        var sel = document.getElementById('id_comp_code_app');
//        sel.selectedIndex = 1;
    });


    // Function to store the data into the session
    window.onbeforeunload = function () {
        sessionStorage.setItem("COMP_CODE", $('#id_comp_code_app').val());
        sessionStorage.setItem("ACC_ASSGN_CAT", $('#id_acc_assgn_cat').val());
        sessionStorage.setItem("LANG", $('#id_language').val());
    }


    //*******************************************
    $('#hg_accnt_report_search').click(function () {
        OpenLoaderPopup();
    })

    //clear filters
    $(document).ready(function () {
    $('#clear_filters_button').click(function () {
        // Clear the selected values in the dropdowns
        $('#id_comp_code_app').val(null);
        $('#id_acc_assgn_cat').val(null);
        $('#id_language').val(null);
        // Clear the local storage values
        localStorage.removeItem("COMP_CODE");
        localStorage.removeItem("ACC_ASSGN_CAT");
        localStorage.removeItem("LANG");
        // Refresh the selectpicker to reflect the changes
        $('.multiple_select').selectpicker('refresh');
    });
});
