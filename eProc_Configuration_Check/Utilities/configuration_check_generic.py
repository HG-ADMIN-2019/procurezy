from django.db.models import Q

from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import UnspscCategoriesCustDesc, UnspscCategoriesCust, UnspscCategories, \
    AccountingDataDesc, AccountingData, OrgCompanies, OrgPorg, OrgPGroup, WorkflowSchema, ApproverType, SpendLimitValue, \
    SpendLimitId, ApproverLimitValue, ApproverLimit, WorkflowACC, OrgAddressMap, OrgAddress, Incoterms, Payterms_desc, \
    Payterms, ProductsDetail, Country, Currency, Languages, SupplierMaster, UnitOfMeasures, TimeZone, OrgClients, \
    OrgNodeTypes, OrgAttributes, OrgModelNodetypeConfig, AuthorizationObject, DetermineGLAccount

django_query_instance = DjangoQueries()


def check_unspsc_category_desc_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(UnspscCategoriesCustDesc,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for unspsc_desc in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'prod_cat_id': unspsc_desc['prod_cat_id']}):
            # check for deletion of record
            if unspsc_desc['del_ind'] == '1':
                if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'prod_cat_id': unspsc_desc['prod_cat_id'],
                                                                 'language_id': unspsc_desc['language_id']}
                                                                ):
                    delete_count = delete_count + 1
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'prod_cat_id': unspsc_desc['prod_cat_id'],
                                                                 'category_desc': unspsc_desc['prod_cat_desc'],
                                                                 'language_id': unspsc_desc['language_id']}):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'prod_cat_id': unspsc_desc['prod_cat_id'],
                                                                   'language_id': unspsc_desc['language_id']}):
                    update_count = update_count + 1
                else:
                    # insert check
                    insert_count = insert_count + 1
        else:
            print(unspsc_desc['prod_cat_id'])
            dependent_count = dependent_count + 1

        print(unspsc_desc)
    # append message with count
    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_unspsc_category_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(UnspscCategoriesCust,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for unspsc_desc in ui_data:
        if django_query_instance.django_existence_check(UnspscCategories,
                                                        {'del_ind': False,
                                                         'prod_cat_id': unspsc_desc['prod_cat_id']}):
            if unspsc_desc['del_ind'] == '1':
                if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'prod_cat_id': unspsc_desc['prod_cat_id']
                                                                 }
                                                                ):
                    delete_count = delete_count + 1
                else:
                    invalid_count = invalid_count + 1
            else:
                if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'prod_cat_id': unspsc_desc['prod_cat_id']
                                                                 }):
                    duplicate_count = duplicate_count + 1
                elif django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'prod_cat_id': unspsc_desc['prod_cat_id']
                                                                   }):
                    update_count = update_count + 1
                else:
                    insert_count = insert_count + 1
        else:
            dependent_count = dependent_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_acc_assign_desc_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(AccountingData,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for acc_desc in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(AccountingDataDesc,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'account_assign_value': acc_desc['account_assign_value']}):
            # check for deletion of record
            if acc_desc['del_ind'] == '1':
                if django_query_instance.django_existence_check(AccountingDataDesc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'account_assign_value': acc_desc[
                                                                     'account_assign_value'],
                                                                 'company_id': acc_desc['company_id'],
                                                                 'account_assign_cat': acc_desc['account_assign_cat'],
                                                                 'language_id': acc_desc['language_id']}):
                    delete_count = delete_count + 1
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(AccountingDataDesc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'account_assign_value': acc_desc[
                                                                     'account_assign_value'],
                                                                 'description': acc_desc['description'],
                                                                 'company_id': acc_desc['company_id'],
                                                                 'account_assign_cat': acc_desc['account_assign_cat'],
                                                                 'language_id': acc_desc['language_id']}):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(AccountingDataDesc,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'account_assign_value': acc_desc[
                                                                       'account_assign_value'],
                                                                   'company_id': acc_desc['company_id'],
                                                                   'account_assign_cat': acc_desc[
                                                                       'account_assign_cat'],
                                                                   'language_id': acc_desc['language_id']}):
                    update_count = update_count + 1
                else:
                    # insert check
                    insert_count = insert_count + 1
        else:
            print(acc_desc['account_assign_value'])
            dependent_count = dependent_count + 1

        print(acc_desc)
    # append message with count
    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_acc_assign_values_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(AccountingData,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for acc_value in ui_data:
        if acc_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(AccountingData,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'account_assign_value': acc_value[
                                                                 'account_assign_value']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(AccountingData,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'account_assign_value': acc_value['account_assign_value'],
                                                             'company_id': acc_value['company_id'],
                                                             'account_assign_cat': acc_value['account_assign_cat'],
                                                             'valid_from': acc_value['valid_from'],
                                                             'valid_to': acc_value['valid_to']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(AccountingData,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'account_assign_value': acc_value[
                                                                   'account_assign_value'],
                                                               'company_id': acc_value['company_id'],
                                                               'account_assign_cat': acc_value['account_assign_cat'],
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_company_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgCompanies,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for com_value in ui_data:
        if com_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(OrgCompanies,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'company_id': com_value[
                                                                 'company_id']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgCompanies,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'company_id': com_value['company_id'],
                                                             'name1': com_value['name1'],
                                                             'name2': com_value['name2']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgCompanies,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'company_id': com_value['company_id']
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_purchaseorg_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgPorg,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for prorg_value in ui_data:
        if prorg_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(OrgPorg,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'porg_id': prorg_value[
                                                                 'porg_id']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgPorg,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'porg_id': prorg_value['porg_id'],
                                                             'description': prorg_value['description'],
                                                             'company_id': prorg_value['company_id']
                                                             }):

                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgPorg,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'porg_id': prorg_value[
                                                                   'porg_id'],
                                                               'company_id': prorg_value['company_id']

                                                               }):

                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_purchasegrp_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgPGroup,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for purgrp_value in ui_data:
        if purgrp_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(OrgPGroup,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'pgroup_id': purgrp_value[
                                                                 'pgroup_id']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgPGroup,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'pgroup_id': purgrp_value['pgroup_id'],
                                                             'description': purgrp_value['description'],
                                                             'porg_id': purgrp_value['porg_id'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgPGroup,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'pgroup_id': purgrp_value[
                                                                   'pgroup_id'],
                                                               'porg_id': purgrp_value['porg_id'],
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_approvaltype_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ApproverType,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for app_typ in ui_data:
        if app_typ['del_ind'] == '1':
            if django_query_instance.django_existence_check(ApproverType,
                                                            {'del_ind': False,
                                                             'app_types': app_typ[
                                                                 'app_types']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(ApproverType,
                                                            {'del_ind': False,
                                                             'app_types': app_typ['app_types'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(ApproverType,
                                                              {'del_ind': False,
                                                               'app_types': app_typ[
                                                                   'app_types'],
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_workflowschema_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(WorkflowSchema,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for workflw_schema in ui_data:
        if workflw_schema['del_ind'] == '1':
            if django_query_instance.django_existence_check(WorkflowSchema,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'workflow_schema': workflw_schema[
                                                                 'workflow_schema']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(WorkflowSchema,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'workflow_schema': workflw_schema['workflow_schema'],

                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(WorkflowSchema,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'workflow_schema': workflw_schema[
                                                                   'workflow_schema'],
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_spendlimit_value_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(SpendLimitValue,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for spend_limit_value in ui_data:
        if spend_limit_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(SpendLimitValue,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'spend_code_id': spend_limit_value[
                                                                 'spend_code_id']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(SpendLimitValue,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'spend_code_id': spend_limit_value['spend_code_id'],
                                                             'upper_limit_value': spend_limit_value[
                                                                 'upper_limit_value'],
                                                             'company_id': spend_limit_value['company_id'],
                                                             'currency_id': spend_limit_value['currency_id']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(SpendLimitValue,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'spend_code_id': spend_limit_value[
                                                                   'spend_code_id'],
                                                               'company_id': spend_limit_value['company_id'],
                                                               'currency_id': spend_limit_value['currency_id']
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_spending_limit_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(SpendLimitId,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    valid_data_list = []
    for spending_limit in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(SpendLimitValue,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'spend_code_id': spending_limit['spend_code_id'],
                                                         }):
            # check for deletion of record
            if spending_limit['del_ind'] == '1':
                if django_query_instance.django_existence_check(SpendLimitId,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'spender_username': spending_limit['spender_username'],
                                                                 'company_id': spending_limit['company_id']}
                                                                ):
                    delete_count = delete_count + 1
                    valid_data_list.append(spending_limit)
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(SpendLimitId,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'spend_code_id': spending_limit['spend_code_id'],
                                                                 'spender_username': spending_limit['spender_username'],
                                                                 'company_id': spending_limit['company_id']
                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(SpendLimitId,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'spender_username': spending_limit['spender_username'],
                                                                   'company_id': spending_limit[
                                                                       'company_id']}):
                    update_count = update_count + 1
                    valid_data_list.append(spending_limit)
                else:
                    # insert check
                    insert_count = insert_count + 1
                    valid_data_list.append(spending_limit)
        else:
            print(spending_limit['spend_code_id'])
            dependent_count = dependent_count + 1

        print(spending_limit)
    # append message with count
    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message,valid_data_list


def check_approv_limit_value_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ApproverLimitValue,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for approv_limit_value in ui_data:
        if approv_limit_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(ApproverLimitValue,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'app_code_id': approv_limit_value[
                                                                 'app_code_id']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(ApproverLimitValue,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'app_code_id': approv_limit_value['app_code_id'],
                                                             'company_id': approv_limit_value['company_id'],
                                                             'app_types': approv_limit_value['app_types'],
                                                             'upper_limit_value': approv_limit_value[
                                                                 'upper_limit_value'],
                                                             'currency_id': approv_limit_value['currency_id']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(ApproverLimitValue,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'app_code_id': approv_limit_value[
                                                                   'app_code_id'],
                                                               'company_id': approv_limit_value['company_id'],
                                                               'app_types': approv_limit_value['app_types'],
                                                               'currency_id': approv_limit_value['currency_id']
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_approv_limit_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ApproverLimit,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for approv_limit in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(ApproverLimitValue,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'app_code_id': approv_limit['app_code_id'],
                                                         }):
            # check for deletion of record
            if approv_limit['del_ind'] == '1':
                if django_query_instance.django_existence_check(ApproverLimit,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'app_code_id': approv_limit['app_code_id'],
                                                                 'approver_username': approv_limit['approver_username'],
                                                                 'company_id': approv_limit['company_id']}
                                                                ):
                    delete_count = delete_count + 1
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(ApproverLimit,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'approver_username': approv_limit['approver_username'],
                                                                 'app_code_id': approv_limit['app_code_id'],
                                                                 'company_id': approv_limit['company_id']
                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(ApproverLimit,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'approver_username': approv_limit[
                                                                       'approver_username'],
                                                                   'app_code_id': approv_limit['app_code_id'],
                                                                   'company_id': approv_limit[
                                                                       'company_id']}):
                    update_count = update_count + 1
                else:
                    # insert check
                    insert_count = insert_count + 1
        else:
            print(approv_limit['app_code_id'])
            dependent_count = dependent_count + 1

        print(approv_limit)
    # append message with count
    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_workflow_acc_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(WorkflowACC,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for workflw_acc_value in ui_data:
        if workflw_acc_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(WorkflowACC,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'acc_value': workflw_acc_value[
                                                                 'acc_value']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(WorkflowACC,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'acc_value': workflw_acc_value['acc_value'],
                                                             'company_id': workflw_acc_value['company_id'],
                                                             'app_username': workflw_acc_value['app_username'],
                                                             'sup_company_id': workflw_acc_value[
                                                                 'sup_company_id'],
                                                             'sup_acc_value': workflw_acc_value['sup_acc_value']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(WorkflowACC,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'acc_value': workflw_acc_value['acc_value'],
                                                               'company_id': workflw_acc_value['company_id'],
                                                               'app_username': workflw_acc_value['app_username'],
                                                               'sup_company_id': workflw_acc_value[
                                                                   'sup_company_id'],
                                                               'sup_acc_value': workflw_acc_value['sup_acc_value']
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_address_types_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgAddressMap,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for address_type in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(OrgAddress,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'address_number': address_type['address_number'],
                                                         }):
            # check for deletion of record
            if address_type['del_ind'] == '1':
                if django_query_instance.django_existence_check(OrgAddressMap,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'address_number': address_type['address_number'],
                                                                 'address_type': address_type['address_type']
                                                                 }
                                                                ):
                    delete_count = delete_count + 1
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(OrgAddressMap,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'address_number': address_type['address_number'],
                                                                 'address_type': address_type['address_type'],

                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(OrgAddressMap,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'address_number': address_type['address_number'],
                                                                   'address_type': address_type['address_type']}):
                    update_count = update_count + 1
                else:
                    # insert check
                    insert_count = insert_count + 1
        else:
            print(address_type['address_number'])
            dependent_count = dependent_count + 1

        print(address_type)
    # append message with count
    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_address_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(OrgAddress,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for com_value in ui_data:
        if com_value['del_ind'] == '1':
            if django_query_instance.django_existence_check(OrgAddress,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'address_number': com_value[
                                                                 'address_number']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(OrgAddress,
                                                            {'del_ind': False,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'address_number': com_value['address_number'],
                                                             'title': com_value['title'],
                                                             'name1': com_value['name1'],
                                                             'name2': com_value['name2'],
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(OrgAddress,
                                                              {'del_ind': False,
                                                               'client': global_variables.GLOBAL_CLIENT,
                                                               'address_number': com_value['address_number'],
                                                               'title': com_value['title'],
                                                               'name1': com_value['name1'],
                                                               'name2': com_value['name2'],
                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_paymentterm_desc_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(Payterms,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for payment_term_desc in ui_data:
        # dependent check
        if django_query_instance.django_existence_check(Payterms_desc,
                                                        {'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT,
                                                         'payment_term_key': payment_term_desc['payment_term_key']
                                                         }):
            # check for deletion of record
            if payment_term_desc['del_ind'] == '1':
                if django_query_instance.django_existence_check(Payterms_desc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'payment_term_key': payment_term_desc
                                                                 ['payment_term_key'],
                                                                 'language_id': payment_term_desc['language_id']
                                                                 }
                                                                ):
                    delete_count = delete_count + 1
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(Payterms_desc,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'payment_term_key': payment_term_desc
                                                                 ['payment_term_key'],
                                                                 'description': payment_term_desc['description'],
                                                                 'day_limit': payment_term_desc['day_limit'],
                                                                 'language_id': payment_term_desc['language_id']

                                                                 }):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(Payterms_desc,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'payment_term_key': payment_term_desc
                                                                   ['payment_term_key'],
                                                                   'language_id': payment_term_desc['language_id']}):
                    update_count = update_count + 1
                else:
                    # insert check
                    insert_count = insert_count + 1
        else:
            print(payment_term_desc['payment_term_key'])
            dependent_count = dependent_count + 1

        print(payment_term_desc)
    # append message with count
    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_inco_terms_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(Incoterms,
                                                               {'del_ind': False,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for inco_terms in ui_data:
        if inco_terms['del_ind'] == '1':
            if django_query_instance.django_existence_check(Incoterms,
                                                            {'del_ind': False,
                                                             'incoterm_key': inco_terms[
                                                                 'incoterm_key']}):
                delete_count = delete_count + 1
            else:
                invalid_count = invalid_count + 1
        else:
            if django_query_instance.django_existence_check(Incoterms,
                                                            {'del_ind': False,
                                                             'incoterm_key': inco_terms['incoterm_key'],
                                                             'description': inco_terms['description']
                                                             }):
                duplicate_count = duplicate_count + 1
            elif django_query_instance.django_existence_check(Incoterms,
                                                              {'del_ind': False,
                                                               'incoterm_key': inco_terms[
                                                                   'incoterm_key']

                                                               }):
                update_count = update_count + 1
            else:
                insert_count = insert_count + 1

    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def check_product_detail_data(ui_data):
    """

    """
    db_count = django_query_instance.django_filter_count_query(ProductsDetail,
                                                               {'del_ind': False,
                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                })
    message_type, message_desc = get_message_desc('MSG193')
    db_count_message = message_desc + str(db_count)
    file_count = len(ui_data)
    duplicate_count = 0
    message = {}
    update_count = 0
    insert_count = 0
    delete_count = 0
    invalid_count = 0
    dependent_count = 0
    for productsdetail in ui_data:
        # dependent check
        country_check = django_query_instance.django_existence_check(Country,
                                                                     {'country_code': productsdetail[
                                                                         'country_of_origin']})
        currency_check = django_query_instance.django_existence_check(Currency,
                                                                      {'currency_id': productsdetail[
                                                                          'currency']})
        languages_check = django_query_instance.django_existence_check(Languages,
                                                                       {'language_id': productsdetail[
                                                                           'language']})
        prod_cat_id_check = django_query_instance.django_existence_check(UnspscCategories,
                                                                         {'prod_cat_id': productsdetail[
                                                                             'prod_cat_id']})
        supplier_master_check = django_query_instance.django_existence_check(SupplierMaster,
                                                                             {'supplier_id': productsdetail[
                                                                                 'supplier_id'],
                                                                              'client': global_variables.GLOBAL_CLIENT})
        if country_check and currency_check and languages_check and prod_cat_id_check and supplier_master_check:
            # check for deletion of record
            if productsdetail['del_ind'] == '1':
                if django_query_instance.django_existence_check(ProductsDetail,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'product_id': productsdetail['product_id']}
                                                                ):
                    delete_count = delete_count + 1
                else:
                    # if del is set but record is not found in db then it is consider as invalid count
                    invalid_count = invalid_count + 1
            else:
                # duplicate check
                if django_query_instance.django_existence_check(ProductsDetail,
                                                                {'del_ind': False,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'product_id': productsdetail['product_id']}):
                    duplicate_count = duplicate_count + 1
                # update check
                elif django_query_instance.django_existence_check(ProductsDetail,
                                                                  {'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT,
                                                                   'product_id': productsdetail['product_id']}):
                    update_count = update_count + 1
                else:
                    # insert check
                    insert_count = insert_count + 1
        else:
            print(productsdetail['prod_cat_id'])
            dependent_count = dependent_count + 1

        print(productsdetail)
    # append message with count
    file_count_message = get_message_desc('MSG194')[1] + str(file_count)
    delete_count_message = get_message_desc('MSG197')[1] + str(delete_count)
    invalid_count_message = get_message_desc('MSG199')[1] + str(invalid_count)
    duplicate_count_message = get_message_desc('MSG198')[1] + str(duplicate_count)
    update_count_message = get_message_desc('MSG196')[1] + str(update_count)
    insert_count_message = get_message_desc('MSG195')[1] + str(insert_count)
    dependent_count_message = get_message_desc('MSG200')[1] + str(dependent_count)
    message = [db_count_message, file_count_message, insert_count_message, update_count_message,
               duplicate_count_message, delete_count_message, invalid_count_message, dependent_count_message]
    return message


def get_valid_country_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(country_code=data['country_code'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(Country,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_language_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(language_id=data['language_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(Languages,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_uom_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(uom_id=data['uom_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(UnitOfMeasures,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_uom_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(uom_id=data['uom_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(UnitOfMeasures,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_currency_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(currency_id=data['currency_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(Currency,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_timezone_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(time_zone=data['time_zone'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(TimeZone,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_client_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(client=data['client'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgClients,
                                                                      {'del_ind': True}, filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_unspsc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(prod_cat_id=data['prod_cat_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(UnspscCategories,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      {'del_ind': True}, filter_queue):

                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_node_type_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(node_type=data['node_type'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgNodeTypes,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_attributes_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(attribute_id=data['attribute_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgAttributes,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_nodetype_config_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(org_model_types=data['org_model_types'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgModelNodetypeConfig,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_company_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(company_id=data['company_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgCompanies,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_authorization_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(auth_obj_id=data['auth_obj_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(AuthorizationObject,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_SpendLimitValue_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(company_id=data['company_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(SpendLimitValue,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_SpendLimitId_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(spender_username=data['spender_username'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(SpendLimitId,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_ApprovlLimit_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(approver_username=data['approver_username'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(ApproverLimit,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_ApprovlLimitValue_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(app_code_id=data['app_code_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(ApproverLimitValue,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_workflows_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(acc_value=data['acc_value'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(WorkflowACC,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_incoterms_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(incoterm_key=data['incoterm_key'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(Incoterms,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_payment_desc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(payment_term_key=data['payment_term_key'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(Payterms_desc,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_UnspscCategoriesCust_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(prod_cat_id=data['prod_cat_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(UnspscCategoriesCust,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_UnspscCategoriesCustDesc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(prod_cat_id=data['prod_cat_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(UnspscCategoriesCustDesc,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_org_company_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(company_id=data['company_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgCompanies,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_OrgPGroup_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(pgroup_id=data['pgroup_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgPGroup,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_OrgPorg_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(porg_id=data['porg_id'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(OrgPorg,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_DetermineGLAccount_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(det_gl_acc_guid=data['det_gl_acc_guid'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(DetermineGLAccount,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_AccountingData_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(account_assign_value=data['account_assign_value'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(AccountingData,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},

                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_AccountingDataDesc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(account_assign_value=data['account_assign_value'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(AccountingDataDesc,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_ApproverType_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(app_types=data['app_types'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(ApproverType,
                                                                      {'del_ind': True },
                                                                      filter_queue):

                data_list.append(data)
        else:
            data_list.append(data)
    return data_list

def get_valid_work_flow_schema_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(workflow_schema=data['workflow_schema'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(WorkflowSchema,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_AccountingDataDesc_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(account_assign_value=data['account_assign_value'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(AccountingDataDesc,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_ApproverType_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(app_types=data['app_types'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(ApproverType,
                                                                      {'del_ind': True },
                                                                      filter_queue):

                data_list.append(data)
        else:
            data_list.append(data)
    return data_list


def get_valid_work_flow_schema_data(ui_data):
    data_list = []
    for data in ui_data:
        filter_queue = ~Q(workflow_schema=data['workflow_schema'])
        if data['del_ind']:
            if not django_query_instance.django_queue_existence_check(WorkflowSchema,
                                                                      {'del_ind': True,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      filter_queue):
                data_list.append(data)
        else:
            data_list.append(data)

    return data_list


    return data_list

