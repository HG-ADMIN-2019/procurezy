import datetime

from django.db.models import Q

from eProc_Basic.Utilities.constants.constants import CONST_SC_HEADER_ORDERED
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
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
                                                                     {'client': client, 'grouping_ind': True}).order_by(*order_list)
    for sc_item in sc_item_details:
        guid = sc_item.header_guid_id
        scheader_details = django_query_instance.django_filter_only_query(ScHeader,
                                                                          {'guid': guid,
                                                                           'client': client}).values('doc_number')
        for scheader_detail in scheader_details:
            sc_header_item_detail = [scheader_detail['doc_number'], sc_item.prod_cat_desc, sc_item.supplier_id,
                                     sc_item.comp_code, sc_item.item_del_date, sc_item.unit, sc_item.quantity,
                                     sc_item.prod_cat_id]

            sc_header_item_details.append(sc_header_item_detail)
    return sc_header_item_details


