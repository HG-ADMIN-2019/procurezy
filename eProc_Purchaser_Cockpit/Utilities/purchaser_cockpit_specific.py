import datetime
import re

from django.db.models import Q

from eProc_Basic.Utilities.constants.constants import CONST_SC_HEADER_ORDERED, CONST_SC_HEADER_APPROVED
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgCompanies
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data
from eProc_Shopping_Cart.models import ScItem, ScHeader
from eProc_Supplier_Order_Management.models import get_som_po_details_by_fields

django_query_instance = DjangoQueries()


def filter_based_on_sc_item_field(client, order_list):
    """

    :param client:
    :param order_list:
    :return:
    """
    sc_header_item_details = []
    sc_header_list = django_query_instance.django_filter_value_list_query(ScHeader,
                                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                                           'status': CONST_SC_HEADER_ORDERED,
                                                                           'ordered_at': datetime.date.today()},
                                                                          'guid')
    sc_item_details = django_query_instance.django_filter_only_query(ScItem,
                                                                     {'client': client, 'grouping_ind': True}).order_by(
        *order_list)
    for sc_item in sc_item_details:
        guid = sc_item.header_guid_id
        scheader_details = django_query_instance.django_filter_only_query(ScHeader,
                                                                          {'guid': guid,
                                                                           'client': client,
                                                                           'status': CONST_SC_HEADER_APPROVED,
                                                                           }).values('doc_number')
        for scheader_detail in scheader_details:
            sc_header_item_detail = [scheader_detail['doc_number'], sc_item.prod_cat_desc, sc_item.supplier_id,
                                     sc_item.comp_code, sc_item.item_del_date, sc_item.unit, sc_item.quantity,
                                     sc_item.prod_cat_id]

            sc_header_item_details.append(sc_header_item_detail)
    return sc_header_item_details


def item_search(**kwargs):
    client = global_variables.GLOBAL_CLIENT
    prod_cat_query = Q()
    company_query = Q()
    sc_obj = ScItem
    sc_item_inst = ScItem()
    hdr_obj = ScHeader
    sc_hdr_inst = ScHeader()
    args_list = {}
    order_list = []
    doc_num_query = Q()
    sc_header_item_details = []
    from_date_val = ''
    for key, value in kwargs.items():
        value_list = []
        if value:
            if key == 'doc_number':
                if '*' in value:
                    doc_num_match = re.search(r'[a-zA-Z0-9]+', value)
                    if value[0] == '*' and value[-1] == '*':
                        doc_num_query = Q(doc_number__in=value) | Q(doc_number__icontains=doc_num_match.group(0))
                    elif value[0] == '*':
                        doc_num_query = Q(doc_number__in=value) | Q(doc_number__iendswith=doc_num_match.group(0))
                    else:
                        doc_num_query = Q(doc_number__in=value) | Q(doc_number__istartswith=doc_num_match.group(0))
                else:
                    doc_list = sc_hdr_inst.get_hdr_data_by_fields(hdr_obj, value, client)
                    args_list['doc_number__in'] = doc_list
                result = sc_hdr_inst.get_hdr_data_for_docnum(client, hdr_obj,
                                                             doc_num_query,
                                                             **args_list)
                sc_item_details = django_query_instance.django_filter_only_query(ScItem,
                                                                                 {'client': client,
                                                                                  'grouping_ind': True}).order_by(
                    *order_list)
                for sc_item in sc_item_details:
                    guid = sc_item.header_guid_id
                    for guid_val in result:
                        if guid_val['guid'] == guid:
                            sc_header_item_detail = [guid_val['doc_number'], sc_item.prod_cat_desc,
                                                     sc_item.supplier_id,
                                                     sc_item.comp_code, sc_item.item_del_date, sc_item.unit,
                                                     sc_item.quantity,
                                                     sc_item.prod_cat_id]
                            sc_header_item_details.append(sc_header_item_detail)
            else:
                if key == 'prod_cat_id':
                    if '*' not in value:
                        value_list = [value]
                    prod_cat_query = django_q_query(value, value_list, 'prod_cat_id')
                if key == 'comp_code':
                    if '*' not in value:
                        value_list = [value]
                        company_query = django_q_query(value, value_list, 'comp_code')
                    if value == '*':
                        args_list['comp_code__in'] = django_query_instance.django_filter_value_list_query(OrgCompanies,
                                                                                                          {
                                                                                                              'client': global_variables.GLOBAL_CLIENT,
                                                                                                              'del_ind': False},
                                                                                                          'company_id')
                    else:
                        args_list['comp_code'] = value

                sc_details_query = list(sc_item_inst.get_item_data_by_fields(client,
                                                                             sc_obj,
                                                                             prod_cat_query,
                                                                             company_query,
                                                                             **args_list
                                                                             ))
                for sc_item in sc_details_query:
                    guid = sc_item['header_guid_id']
                    scheader_details = django_query_instance.django_filter_only_query(ScHeader,
                                                                                      {'guid': guid,
                                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                                       'status': CONST_SC_HEADER_ORDERED,
                                                                                       }).values('doc_number')
                    for scheader_detail in scheader_details:
                        sc_header_item_detail = [scheader_detail['doc_number'], sc_item['prod_cat_desc'],
                                                 sc_item['supplier_id'],
                                                 sc_item['comp_code'], sc_item['item_del_date'], sc_item['unit'],
                                                 sc_item['quantity'],
                                                 sc_item['prod_cat_id']]

                        sc_header_item_details.append(sc_header_item_detail)

    return sc_header_item_details

