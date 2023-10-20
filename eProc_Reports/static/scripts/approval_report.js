    // Script to generate sort and filter feature for tables
    $(document).ready(function () {
        nav_bar_admin();
        table_sort_filter_export_excel();
        // Loader implementation on search button
        $('#hg_approval_report_search').click(function () {
            $('#hg_loader').modal('show');
        });
        $('.multiple_select').selectpicker();
        $('.multiple_select').selectpicker('val', selected_status_value);
//        $('#id_comp_code_app').val(selected_comp_value).attr('selected', 'selected');
        $('#acc_assgn_cat').val(selected_status_value).attr('selected', 'selected');
    });

    // Function to store the data into the session
    window.onbeforeunload = function () {
        sessionStorage.setItem("COMP_CODE", $('#id_comp_code_app').val());
        sessionStorage.setItem("ACC_ASSGN_CAT", $('#acc_assgn_cat').val());
    }

    // Function to retrieve data from session storage
    window.onload = function () {
        comp_code = sessionStorage.getItem("COMP_CODE");
        acc_assgn_cat = sessionStorage.getItem("ACC_ASSGN_CAT");
        $('#id_comp_code_app').val(comp_code).attr('selected', 'selected');
        $('#acc_assgn_cat').val(acc_assgn_cat).attr('selected', 'selected');
    }
function resetCompanyCodeDropdown() {
        var companyCodeDropdown = document.getElementById('id_comp_code_app');
        if (companyCodeDropdown) {
            companyCodeDropdown.selectedIndex = 0;
        }
    }

    // Call the function on page load to reset the dropdown
    window.onload = function () {
        resetCompanyCodeDropdown();
    }
    //*********************************************
    $('#hg_approval_report_search').click(function () {
        OpenLoaderPopup();
    })

    $(document).ready(function () {
    // Initialize selectpicker
    $('.multiple_select').selectpicker();

    // Event handler for the "search" button
    $('#hg_approval_report_search').click(function () {
        // Display the table container (including table and pagination)
        $('#table-container').show();

        // Optional: Open a loader modal
        OpenLoaderPopup();

        // Store the selected values in local storage
        var selectedCompany = $('#id_comp_code_app').val();
        var selectedCategories = $('#acc_assgn_cat').val();

        // Create an object to hold the selected values
        var selectedData = {
            company: selectedCompany,
            categories: selectedCategories
        };

        // Store the selected data as a JSON string in local storage
        localStorage.setItem("selectedData", JSON.stringify(selectedData));
    });

    // Retrieve and set the selected data from local storage on page load
    var selectedDataJSON = localStorage.getItem("selectedData");
    if (selectedDataJSON) {
        var selectedData = JSON.parse(selectedDataJSON);

        if (selectedData.company) {
            $('#id_comp_code_app').val(selectedData.company);
        }

        if (selectedData.categories) {
            $('#acc_assgn_cat').selectpicker('val', selectedData.categories);
        }
    }

    // Rest of your code...
});