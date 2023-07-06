"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    purchaser_cockpit.py
Usage:
    Purchase assist role user data
Author:
    Deepika K
"""
from django.shortcuts import render
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data
from eProc_Purchaser_Cockpit.Utilities.purchaser_cockpit_specific import filter_based_on_sc_item_field


# purchaser_cockpit_search


def incomplete_form(request, guid=None):
    """

    :param request:
    :param guid:
    :return:
    """
    context = {
        'inc_nav': True,
        'shopping': True,
    }

    return render(request, 'Purchaser_Cockpit/incomplete_form.html', context)


def sc_item_field_filter(request):
    supplier_id = False
    comp_code = False
    prod_cat = False
    client = getClients(request)
    order_list = []
    search_fields = {}
    sc_header_item_details = ''
    sc_header_item_details = filter_based_on_sc_item_field(client, order_list)
    if request.method == 'POST':
        inp_comp_code = request.POST.get('company_code')
        inp_doc_type = 'SC'
        inp_doc_num = request.POST.get('sc_number')
        inp_from_date = request.POST.get('from_date')
        inp_to_date = request.POST.get('to_date')
        inp_supl = None
        inp_created_by = None
        inp_requester = None
        prod_cat = request.POST.get('product_category')
        # results
        sc_item_details = get_hdr_data(inp_doc_type,
                                       inp_doc_num,
                                       inp_from_date,
                                       inp_to_date,
                                       prod_cat,
                                       inp_created_by,
                                       inp_requester, client, False)
        supplier_id = request.POST.get('supplier_id')
        comp_code = request.POST.get('comp_code')
        if prod_cat:
            order_list.append(prod_cat)
        # if inp_doc_num:
        #     order_list.append(inp_doc_num)
        if comp_code:
            order_list.append(comp_code)

        result = filter_based_on_sc_item_field(client, order_list)
        for item in result:
            if inp_doc_num == item[0]:
                sc_header_item_details = [item]

    context = {
        'sc_header_item_details': sc_header_item_details,
        'prod_cat': prod_cat,
        'supplier_id': supplier_id,
        'comp_code': comp_code,
        'inc_nav': True,
        'shopping': True,
        'is_slide_menu': True
    }

    return render(request, 'Purchaser_Cockpit/sourcing_cockpit.html', context)
