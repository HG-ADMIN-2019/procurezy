from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import get_country_id, getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.messages_config import get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import SupplierMaster, SupplierMasterHistory
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScItem, CartItemDetails
from eProc_Suppliers.Utilities.supplier_generic import supplier_detail_search
from eProc_Suppliers.Utilities.supplier_specific import update_block_status, get_supplier_data
from eProc_Suppliers.models import OrgSuppliers, OrgSuppliersHistory

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def delete_supplier(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    supplier_data = JsonParser_obj.get_json_from_req(request)
    success_message = ''
    for supplier_id in supplier_data['data']:
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'supplier_id': supplier_id,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False}) and not \
                django_query_instance.django_existence_check(OrgSuppliers,
                                                             {'supplier_id': supplier_id,
                                                              'client': global_variables.GLOBAL_CLIENT,
                                                              'del_ind': False}):
            create_supplier_history_data(supplier_id)
            django_query_instance.django_filter_delete_query(SupplierMaster,
                                                             {'supplier_id': supplier_id,
                                                              'client': global_variables.GLOBAL_CLIENT,
                                                              'del_ind': False})
            success_message = get_message_desc('MSG206')[1]
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'supplier_id': supplier_id,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False}):
            if django_query_instance.django_existence_check(OrgSuppliers,
                                                            {'supplier_id': supplier_id,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False}):
                # create_Orgsupplier_history_data(supplier_id)
                django_query_instance.django_filter_delete_query(OrgSuppliers,
                                                                 {'supplier_id': supplier_id,
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  'del_ind': False})
                create_supplier_history_data(supplier_id)
                django_query_instance.django_filter_delete_query(SupplierMaster,
                                                                 {'supplier_id': supplier_id,
                                                                  'client': global_variables.GLOBAL_CLIENT,
                                                                  'del_ind': False})
                success_message = get_message_desc('MSG206')[1]

    supplier_results = get_supplier_data()
    response = {'supplier_results': supplier_results, 'success_message': success_message}
    return JsonResponse(response, safe=False)


def supplier_blocking(request):
    """

    """
    update_user_info(request)
    supplier_block_data = JsonParser_obj.get_json_from_req(request)
    update_block_status(supplier_block_data)
    response = {'success_message': "Changed Successfully"}

    return JsonResponse(response, safe=False)


def create_supplier_history_data(supplier_id):
    supplier_info = django_query_instance.django_filter_query(SupplierMaster,
                                                              {'supplier_id': supplier_id,
                                                               'del_ind': False}, None, None)
    django_query_instance.django_create_query(SupplierMasterHistory, supplier_info[0])


def create_Orgsupplier_history_data(supplier_id):
    supplier_info = django_query_instance.django_filter_query(OrgSuppliers,
                                                              {'supplier_id': supplier_id,
                                                               'del_ind': False}, None, None)
    for supplier in supplier_info:
        django_query_instance.django_create_query(OrgSuppliersHistory, supplier)
