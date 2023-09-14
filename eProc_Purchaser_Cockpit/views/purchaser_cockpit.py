"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    purchaser_cockpit.py
Usage:
    Purchase assist role user data
Author:
    Deepika K
"""
from django.http import JsonResponse
from django.shortcuts import render

from eProc_Basic.Utilities.constants.constants import CONST_SC_HEADER_APPROVED
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic_Settings.views import JsonParser_obj
from eProc_Configuration.models import OrgCompanies
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data
from eProc_Emails.Utilities.email_notif_generic import send_po_attachment_email
from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder, check_for_po_creation, check_po
from eProc_Purchaser_Cockpit.Utilities.purchaser_cockpit_specific import filter_based_on_sc_item_field, item_search, \
    get_sourcing_data, filter_rfq

# purchaser_cockpit_search
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScItem, ScHeader

django_query_instance = DjangoQueries()


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
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    order_list = []
    search_fields = {}
    # sc_header_item_details = ''
    sc_header_item = []
    sc_header_item_details = filter_based_on_sc_item_field(client, order_list)
    count = len(sc_header_item_details)
    if request.method == 'POST':
        search_fields = {}
        inp_comp_code = request.POST.get('company_code')
        inp_doc_type = 'SC'
        inp_doc_num = request.POST.get('sc_number')
        inp_from_date = request.POST.get('from_date')
        inp_to_date = request.POST.get('to_date')
        inp_supl = None
        inp_created_by = None
        inp_requester = None
        prod_cat = request.POST.get('product_desc')
        # results
        search_fields['doc_number'] = request.POST.get('sc_number')
        search_fields['prod_cat_id'] = request.POST.get('product_desc')
        if request.POST.get('company_code') == '':
            search_fields['comp_code'] = '*'
        else:
            search_fields['comp_code'] = request.POST.get('company_code')
        sc_item_inst = ScItem()
        sc_header_item_details = item_search(inp_from_date, inp_to_date, **search_fields)
        count = len(sc_header_item_details)

    context = {
        'sc_header_item_details': sc_header_item_details,
        'count': count,
        'prod_cat': prod_cat,
        'supplier_id': supplier_id,
        'comp_code': comp_code,
        'inc_nav': True,
        'shopping': True,
        'is_slide_menu': True
    }

    return render(request, 'Purchaser_Cockpit/sourcing_cockpit.html', context)


def generate_po(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    response = ''
    sc_header_list = []
    sc_header_instance = ''
    doc_num = []
    guid_arr = []
    po_data = JsonParser_obj.get_json_from_req(request)
    # sc_header_details = django_query_instance.django_filter_query(ScHeader,
    #                                                               {'doc_number__in': doc_num_list,
    #                                                                'client': global_variables.GLOBAL_CLIENT,
    #                                                                'del_ind': False},
    #                                                               None,
    #                                                               None)

    for doc in po_data:
        sc_header_list.append(django_query_instance.django_filter_value_list_query(ScHeader,
                                                                                   {
                                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                                       'doc_number': doc['doc_number']},
                                                                                   'guid'))
        doc_num.append(doc['doc_number'])
        sc_header_instance = django_query_instance.django_get_query(ScHeader,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'doc_number': doc['doc_number']})
        guid_arr.append(sc_header_instance.guid)

    # result = check_po(sc_header_list)
    sc_item_details = django_query_instance.django_filter_query(ScItem, {
        'header_guid__in': guid_arr, 'client': client, 'del_ind': False
    }, None, None)

    po_creation_flag = ''
    # for sc_item in sc_item_details:
    desc = sc_item_details[0]['description']
    for i in range(1, len(sc_item_details)):
        if desc == sc_item_details[i]['description']:
            print("same item")
    create_purchase_order = CreatePurchaseOrder(sc_header_instance)
    status = create_purchase_order.create_purchaser_order(sc_item_details, sc_item_details[0]['supplier_id'])
    if not status:
        return False, create_purchase_order.error_message, create_purchase_order.output, create_purchase_order.po_doc_list

    # status, error_message, output, po_doc_list = create_purchase_order.create_po()
    for po_document_number in create_purchase_order.po_doc_list:
        email_supp_monitoring_guid = ''
        send_po_attachment_email(create_purchase_order.output, po_document_number, email_supp_monitoring_guid)

        if create_purchase_order.error_message:
            response = "error"
        else:
            response = "PO generated"

    return JsonResponse(response, safe=False)


def PO_grouping(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    response = ''
    supplier_id = []
    po_flag = False
    po_data = JsonParser_obj.get_json_from_req(request)
    for doc in po_data:
        if doc['supplier_id'] not in supplier_id:
            supplier_id.append(doc['supplier_id'])

    temp = supplier_id[0]
    for supp in supplier_id:
        if supp == temp:
            po_flag = True
        else:
            po_flag = False

    response = po_flag

    return JsonResponse(response, safe=False)


def rfq_details(request):
    supplier_id = False
    comp_code = False
    prod_cat = False
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    order_list = []
    search_fields = {}
    # sc_header_item_details = ''
    sc_header_item = []
    sc_header_item_details = filter_rfq(client, order_list)
    count = len(sc_header_item_details)
    if request.method == 'POST':
        search_fields = {}
        inp_comp_code = request.POST.get('company_code')
        inp_doc_type = 'SC'
        inp_doc_num = request.POST.get('sc_number')
        inp_from_date = request.POST.get('from_date')
        inp_to_date = request.POST.get('to_date')
        inp_supl = None
        inp_created_by = None
        inp_requester = None
        prod_cat = request.POST.get('product_desc')
        # results
        search_fields['doc_number'] = request.POST.get('sc_number')
        # search_fields['from_date'] = request.POST.get('from_date')
        # search_fields['to_date'] = request.POST.get('to_date')
        search_fields['prod_cat_id'] = request.POST.get('product_desc')
        search_fields['comp_code'] = request.POST.get('company_code')
        sc_item_inst = ScItem()
        sc_header_item_details = item_search(inp_from_date, inp_to_date, **search_fields)
        count = len(sc_header_item_details)

    context = {
        'sc_header_item_details': sc_header_item_details,
        'count': count,
        'prod_cat': prod_cat,
        'supplier_id': supplier_id,
        'comp_code': comp_code,
        'inc_nav': True,
        'shopping': True,
        'is_slide_menu': True
    }

    return render(request, 'Purchaser_Cockpit/display_rfq.html', context)
