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
from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder
from eProc_Purchaser_Cockpit.Utilities.purchaser_cockpit_specific import filter_based_on_sc_item_field, item_search, \
    get_sourcing_data

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
        # search_fields['from_date'] = request.POST.get('from_date')
        # search_fields['to_date'] = request.POST.get('to_date')
        search_fields['prod_cat_id'] = request.POST.get('product_desc')
        search_fields['comp_code'] = request.POST.get('company_code')
        sc_item_inst = ScItem()
        # temp = sc_item_inst.get_prod_cat_id(prod_cat)
        # if inp_from_date or inp_to_date:
        #     sc_details_query = list(ScItem.objects.filter(
        #         item_del_date__lte=inp_to_date,
        #         item_del_date__gte=inp_from_date
        #     ).values())
        #     for sc_item in sc_details_query:
        #         guid = sc_item['header_guid_id']
        #         scheader_details = django_query_instance.django_filter_only_query(ScHeader,
        #                                                                           {'guid': guid,
        #                                                                            'client': client}).values(
        #             'doc_number')
        #         for scheader_detail in scheader_details:
        #             sc_header_item_detail = [scheader_detail['doc_number'], sc_item['prod_cat_desc'],
        #                                      sc_item['supplier_id'],
        #                                      sc_item['comp_code'], sc_item['item_del_date'], sc_item['unit'],
        #                                      sc_item['quantity'],
        #                                      sc_item['prod_cat_id']]
        #
        #             sc_header_item.append(sc_header_item_detail)
        #     sc_header_item_details = sc_header_item
        # sc_header_item_details = item_search(**search_fields)
        sc_header_item_details = get_sourcing_data(inp_doc_num, inp_from_date, inp_to_date, prod_cat, inp_comp_code)

        for sc_item in sc_header_item_details:
            guid = sc_item['header_guid_id']
            scheader_details = django_query_instance.django_filter_only_query(ScHeader,
                                                                              {'guid': guid,
                                                                               'client': client,
                                                                               'status': CONST_SC_HEADER_APPROVED}).values(
                'doc_number')
            for scheader_detail in scheader_details:
                sc_header_item_detail = [scheader_detail['doc_number'], sc_item['description'],
                                         sc_item['supplier_id'],
                                         sc_item['comp_code'], sc_item['item_del_date'], sc_item['unit'],
                                         sc_item['quantity'],
                                         sc_item['prod_cat_id']]
                sc_header_item.append(sc_header_item_detail)
        sc_header_item_details = sc_header_item

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
    po_data = JsonParser_obj.get_json_from_req(request)
    for doc in po_data:
        sc_header_list.append(django_query_instance.django_filter_value_list_query(ScHeader,
                                                                                   {
                                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                                       'doc_number': doc['doc_number']},
                                                                                   'guid'))
        sc_header_instance = django_query_instance.django_get_query(ScHeader,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'doc_number': doc['doc_number']})
        if sc_header_instance:
            create_purchase_order = CreatePurchaseOrder(sc_header_instance)
            status, error_message, output, po_doc_list = create_purchase_order.create_po()
            for po_document_number in po_doc_list:
                email_supp_monitoring_guid = ''
                send_po_attachment_email(output, po_document_number, email_supp_monitoring_guid)

            if error_message:
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
