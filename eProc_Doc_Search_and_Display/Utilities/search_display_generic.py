"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    search_specific.py
Usage:
     get_hdr_data - This function is used to get header details based on user input
Author:
    Shankar / Sanjay
"""
from datetime import datetime

from django.db.models import Q
from django.http import Http404

from eProc_Basic.Utilities.constants.constants import CONST_OTHER_ERROR, CONST_SC_HEADER_APPROVED
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients, getUsername
from eProc_Configuration.models import SupplierMaster, OrgCompanies
from eProc_Purchase_Order.models.purchase_order import PoHeader
from eProc_Shopping_Cart.models import *
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


# Get header data from search inputs
def get_hdr_data(request, doc_type, doc_num, from_date, to_date, supplier, created_by, requester, search_flag):
    client = getClients(request)
    username = getUsername(request)
    if doc_type == 'SC':
        hdr_obj = ScHeader
        hdr_inst = ScHeader()
    elif doc_type == 'PO':
        hdr_obj = PoHeader
        hdr_inst = PoHeader()
    else:
        raise Http404
    result = None
    supp_query = Q()
    creator_query = Q()
    requester_query = Q()
    doc_num_query = Q()
    args_list = {}
    if doc_num is not None and doc_num != '':
        # result = hdr_inst.get_hdr_data_by_objid(hdr_obj, doc_num, client)
        if '*' in doc_num:
            doc_num_match = re.search(r'[0-9]+', doc_num)
            if doc_num[0] == '*' and doc_num[-1] == '*':
                doc_num_query = Q(doc_number__in=doc_num) | Q(doc_number__icontains=doc_num_match.group(0))
            elif doc_num[0] == '*':
                doc_num_query = Q(doc_number__in=doc_num) | Q(doc_number__iendswith=doc_num_match.group(0))
            else:
                doc_num_query = Q(doc_number__in=doc_num) | Q(doc_number__istartswith=doc_num_match.group(0))
        else:
            doc_list = hdr_inst.get_hdr_data_by_objid(hdr_obj, doc_num, client)
            doc_list.append(supplier)
            args_list['doc_number__in'] = doc_list
    else:
        if from_date is not None and to_date is not None and from_date != '' and to_date != '':
            args_list['created_at__gte'] = from_date
            args_list['created_at__lte'] = to_date
            if search_flag:
                args_list['created_by'] = username
        if doc_type == 'PO' and supplier is not None and supplier != '':
            if '*' in supplier:
                supp_list = SupplierMaster.get_suppid_by_first_name(supplier)
                supplier_match = re.search(r'[a-zA-Z0-9]+', supplier)
                if supplier[0] == '*' and supplier[-1] == '*':
                    supp_query = Q(supplier_id__in=supp_list) | Q(supplier_id__icontains=supplier_match.group(0))
                elif supplier[0] == '*':
                    supp_query = Q(supplier_id__in=supp_list) | Q(supplier_id__iendswith=supplier_match.group(0))
                else:
                    supp_query = Q(supplier_id__in=supp_list) | Q(supplier_id__istartswith=supplier_match.group(0))
            else:
                supp_list = SupplierMaster.get_suppid_by_first_name(supplier)
                supp_list.append(supplier)
                args_list['supplier_id__in'] = supp_list
        if created_by is not None and created_by != '':
            if '*' in created_by:
                user_list = UserData.get_usrid_by_first_name(created_by)
                creater_match = re.search(r'[a-zA-Z0-9]+', created_by)
                if created_by[0] == '*' and created_by[-1] == '*':
                    creator_query = Q(created_by__in=user_list) | Q(created_by__contains=creater_match.group(0))
                elif created_by[0] == '*':
                    creator_query = Q(created_by__in=user_list) | Q(created_by__endswith=creater_match.group(0))
                else:
                    creator_query = Q(created_by__in=user_list) | Q(created_by__startswith=creater_match.group(0))
                # args_list['created_by__contains'] = created_by.group(0)
            else:
                user_list = UserData.get_usrid_by_first_name(created_by)
                user_list.append(created_by)
                args_list['created_by__in'] = user_list
        if requester is not None and requester != '':
            if '*' in requester:
                user_list = UserData.get_usrid_by_first_name(requester)
                requester_match = re.search(r'[a-zA-Z0-9]+', requester)
                if requester[0] == '*' and requester[-1] == '*':
                    requester_query = Q(requester__in=user_list) | Q(requester__icontains=requester_match.group(0))
                elif requester[0] == '*':
                    requester_query = Q(requester__in=user_list) | Q(requester__iendswith=requester_match.group(0))
                else:
                    requester_query = Q(requester__in=user_list) | Q(requester__istartswith=requester_match.group(0))
            else:
                user_list = UserData.get_usrid_by_first_name(requester)
                user_list.append(requester)
                args_list['requester__in'] = user_list

    result = hdr_inst.get_hdr_data_by_fields(client, hdr_obj, supp_query, creator_query, requester_query, doc_num_query,
                                                 **args_list)
    return result


def get_hdr_data_app_monitoring(doc_type, doc_num, from_date, to_date, supplier, created_by, requester,
                                search_flag, error_type, inp_comp_code):
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME
    if doc_type == 'SC':
        hdr_obj = ScHeader
        hdr_inst = ScHeader()
    elif doc_type == 'PO':
        hdr_obj = PoHeader
        hdr_inst = PoHeader()
    else:
        raise Http404
    result = None
    supp_query = Q()

    creator_query = Q()
    requester_query = Q()
    doc_num_query = Q()
    args_list = {}
    if doc_num is not None and doc_num != '':
        if '*' in doc_num:
            doc_num_match = re.search(r'[0-9]+', doc_num)
            if doc_num[0] == '*' and doc_num[-1] == '*':
                doc_num_query = Q(doc_number__in=doc_num) | Q(doc_number__icontains=doc_num_match.group(0))
            elif doc_num[0] == '*':
                doc_num_query = Q(doc_number__in=doc_num) | Q(doc_number__iendswith=doc_num_match.group(0))
            else:
                doc_num_query = Q(doc_number__in=doc_num) | Q(doc_number__istartswith=doc_num_match.group(0))
        else:
            doc_list = hdr_inst.get_hdr_data_by_objid_app_monitoring(hdr_obj, doc_num, error_type, client)
            doc_list.append(supplier)
            args_list['doc_number__in'] = doc_list
    else:
        if from_date is not None and to_date is not None and from_date != '' and to_date != '':
            args_list['created_at__gte'] = datetime.combine(datetime.strptime(from_date, '%Y-%m-%d'),
                                                            datetime.min.time())
            args_list['created_at__lte'] = datetime.combine(datetime.strptime(to_date, '%Y-%m-%d'), datetime.max.time())
            if search_flag:
                args_list['created_by'] = username
        if doc_type == 'PO' and supplier is not None and supplier != '':
            if '*' in supplier:
                supp_list = SupplierMaster.get_suppid_by_first_name(supplier)
                supplier_match = re.search(r'[a-zA-Z0-9]+', supplier)
                if supplier[0] == '*' and supplier[-1] == '*':
                    supp_query = Q(supplier_id__in=supp_list) | Q(supplier_id__icontains=supplier_match.group(0))
                elif supplier[0] == '*':
                    supp_query = Q(supplier_id__in=supp_list) | Q(supplier_id__iendswith=supplier_match.group(0))
                else:
                    supp_query = Q(supplier_id__in=supp_list) | Q(supplier_id__istartswith=supplier_match.group(0))
            else:
                supp_list = SupplierMaster.get_suppid_by_first_name(supplier)
                supp_list.append(supplier)
                args_list['supplier_id__in'] = supp_list
        if created_by is not None and created_by != '':
            if '*' in created_by:
                user_list = UserData.get_usrid_by_first_name(created_by)
                creater_match = re.search(r'[a-zA-Z0-9]+', created_by)
                if created_by[0] == '*' and created_by[-1] == '*':
                    creator_query = Q(created_by__in=user_list) | Q(created_by__contains=creater_match.group(0))
                elif created_by[0] == '*':
                    creator_query = Q(created_by__in=user_list) | Q(created_by__endswith=creater_match.group(0))
                else:
                    creator_query = Q(created_by__in=user_list) | Q(created_by__startswith=creater_match.group(0))
                # args_list['created_by__contains'] = created_by.group(0)
            else:
                user_list = UserData.get_usrid_by_first_name(created_by)
                user_list.append(created_by)
                args_list['created_by__in'] = user_list
        if requester is not None and requester != '':
            if '*' in requester:
                user_list = UserData.get_usrid_by_first_name(requester)
                requester_match = re.search(r'[a-zA-Z0-9]+', requester)
                if requester[0] == '*' and requester[-1] == '*':
                    requester_query = Q(requester__in=user_list) | Q(requester__icontains=requester_match.group(0))
                elif requester[0] == '*':
                    requester_query = Q(requester__in=user_list) | Q(requester__iendswith=requester_match.group(0))
                else:
                    requester_query = Q(requester__in=user_list) | Q(requester__istartswith=requester_match.group(0))
            else:
                user_list = UserData.get_usrid_by_first_name(requester)
                user_list.append(requester)
                args_list['requester__in'] = user_list
        if error_type != CONST_OTHER_ERROR:
            args_list['transmission_error_type'] = error_type
        else:
            args_list['status'] = CONST_SC_HEADER_APPROVED
            args_list['follow_on_doc_type'] = None
            args_list['transmission_error'] = False
        company_code = django_query_instance.django_get_query(OrgCompanies,
                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                               'company_guid': inp_comp_code})
        if company_code:
            if company_code == '*':
                args_list['co_code__in'] = django_query_instance.django_filter_value_list_query(OrgCompanies,
                                                                                                {
                                                                                                    'client': global_variables.GLOBAL_CLIENT,
                                                                                                    'del_ind': False})
            else:
                args_list['co_code'] = company_code.company_id

    result = hdr_inst.get_hdr_data_by_fields_value(client, hdr_obj, supp_query, creator_query, requester_query,
                                                   doc_num_query,
                                                   **args_list)
    return result
