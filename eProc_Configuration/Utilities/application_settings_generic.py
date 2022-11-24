from re import sub

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.constants.constants import CONST_SC_TRANS_TYPE
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import FieldTypeDescription, TransactionTypes, OrgCompanies, PoSplitType, \
    PoSplitCriteria

django_query_instance = DjangoQueries()


def get_configuration_data(db_name, filter_query, value_list):
    """

    """
    result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
    return result


def get_configuration_data_image(db_name, filter_query, value_list):
    """

    """
    result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
    return result


class FieldTypeDescriptionUpdate:
    @staticmethod
    def update_usedFlag(field_type_id):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription, {
                'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
            }).update(used_flag=True)

    @staticmethod
    def reset_usedFlag(field_type_id):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription, {
                'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
            }).update(used_flag=False)

    @staticmethod
    def get_field_type_desc_values(db_name, filter_query, value_list):
        result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
        return result

    @staticmethod
    def reset_used_flag(field_type_id, field_name):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription,
                                                           {'del_ind': False,
                                                            'field_type_id': field_type_id,
                                                            'field_name': field_name,
                                                            'client': global_variables.GLOBAL_CLIENT}).update(
                used_flag=False)

    @staticmethod
    def update_used_flag(field_type_id, field_name):
        if django_query_instance.django_existence_check(FieldTypeDescription, {
            'del_ind': False, 'field_type_id': field_type_id, 'client': global_variables.GLOBAL_CLIENT
        }):
            django_query_instance.django_filter_only_query(FieldTypeDescription, {
                'del_ind': False, 'field_type_id': field_type_id, 'field_name': field_name,
                'client': global_variables.GLOBAL_CLIENT
            }).update(used_flag=True)


def get_product_criteria():
    """

    """
    upload_account_assign_cat = get_configuration_data(PoSplitCriteria,
                                                       {'del_ind': False,
                                                        'client': global_variables.GLOBAL_CLIENT},
                                                       ['po_split_criteria_guid', 'company_code_id', 'activate',
                                                        'po_split_type'])
    data = get_po_split_creteria_dropdown(upload_account_assign_cat)
    data['upload_account_assign_cat'] = upload_account_assign_cat
    return data


def get_po_split_creteria_dropdown(upload_account_assign_cat):
    """

    """
    po_split_types = django_query_instance.django_filter_query(PoSplitType, {'del_ind': False}, None, None)
    for po_criteria in upload_account_assign_cat:
        for po_split_type in po_split_types:
            if po_split_type['po_split_type'] == po_criteria['po_split_type']:
                po_criteria['po_split_type_desc'] = str(po_split_type['po_split_type']) + ' - ' + po_split_type[
                    'po_split_type_desc']

    po_split_typ = get_configuration_data(PoSplitType, {'del_ind': False},
                                          ['po_split_type', 'po_split_type_desc'])
    for po_dropdown in po_split_typ:
        po_dropdown['po_split_type_desc'] = str(po_dropdown['po_split_type']) + ' - ' + po_dropdown[
            'po_split_type_desc']

    dropdown_activate = list(
        FieldTypeDescription.objects.filter(field_name='activate', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values(
            'field_type_id',
            'field_type_desc'
        ))

    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))

    data = {'po_split_typ': po_split_typ,
            'dropdown_activate': dropdown_activate,
            'upload_data_company': upload_data_company}
    return data
