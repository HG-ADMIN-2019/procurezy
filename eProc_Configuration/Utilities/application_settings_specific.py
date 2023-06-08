from calendar import weekday
from datetime import datetime
import datetime

from django.db.models.aggregates import Max

from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.get_db_query import get_country_data
from eProc_Basic.Utilities.messages.messages import MSG112, MSG113
from eProc_Basic.Utilities.functions.camel_case import convert_to_camel_case
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.range_check import range_check
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.Utilities.application_settings_generic import *
from eProc_Configuration.models import *
from eProc_Configuration.models.application_data import *
from eProc_Configuration.models.basic_data import *
from eProc_Configuration.models.development_data import *
from eProc_Configuration.models.development_data import OrgClients
from eProc_Configuration.models.development_data import DocumentType

from eProc_Basic.Utilities.functions.guid_generator import guid_generator, random_int
from eProc_Configuration.models.development_data import MessagesId
from eProc_Configuration.models.master_data import *

django_query_instance = DjangoQueries()
fieldtypedesc_instance = FieldTypeDescriptionUpdate()


class ApplicationSettingsSave:
    def __init__(self):
        self.current_date_time = datetime.today()
        self.username = global_variables.GLOBAL_LOGIN_USERNAME
        self.client = global_variables.GLOBAL_CLIENT

    def save_unspsc(self, prodcat_data):
        """

        """
        prodcat_db_list = []
        for prodcat_detail in prodcat_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UnspscCategories,
                                                                {'prod_cat_id': prodcat_detail['prod_cat_id']}):
                prodcat_db_dictionary = {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                         'prod_cat_desc': convert_to_camel_case(prodcat_detail['prod_cat_desc']),
                                         'unspsc_categories_created_at': self.current_date_time,
                                         'unspsc_categories_created_by': self.username,
                                         'unspsc_categories_changed_at': self.current_date_time,
                                         'unspsc_categories_changed_by': self.username,
                                         }
                prodcat_db_list.append(prodcat_db_dictionary)
            else:
                django_query_instance.django_update_query(UnspscCategories,
                                                          {'prod_cat_id': prodcat_detail['prod_cat_id']},
                                                          {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                           'prod_cat_desc': convert_to_camel_case(
                                                               prodcat_detail['prod_cat_desc']),
                                                           'unspsc_categories_changed_at': self.current_date_time,
                                                           'unspsc_categories_changed_by': self.username,
                                                           'del_ind': prodcat_detail['del_ind']})
        if prodcat_db_list:
            bulk_create_entry_db(UnspscCategories, prodcat_db_list)

    def save_prodcat_data_into_db(self, prodcat_data):
        """
        """

        self.save_unspsc(prodcat_data['data'])

        # message based on button action
        message = get_message_detail_based_on_action(prodcat_data['action'])

        upload_response = get_unspsc_data()
        return upload_response, message

    def save_client_data(self, client_data):
        client_db_list = []
        for client_detail in client_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgClients,
                                                                {'client': client_detail['client']}):
                client_db_dictionary = {'client': client_detail['client'],
                                        'description': convert_to_camel_case(client_detail['description']),
                                        'org_clients_created_at': self.current_date_time,
                                        'org_clients_created_by': self.username,
                                        'org_clients_changed_at': self.current_date_time,
                                        'org_clients_changed_by': self.username,
                                        }
                client_db_list.append(client_db_dictionary)
            else:
                django_query_instance.django_update_query(OrgClients,
                                                          {'client': client_detail['client']},
                                                          {'client': client_detail['client'],
                                                           'description': convert_to_camel_case(
                                                               client_detail['description']),
                                                           'org_clients_changed_at': self.current_date_time,
                                                           'org_clients_changed_by': self.username,
                                                           'del_ind': client_detail['del_ind']})
        if client_db_list:
            bulk_create_entry_db(OrgClients, client_db_list)

    def save_client_data_into_db(self, client_data):
        """

        """
        # save user entered data on db
        self.save_client_data(client_data)

        # message based on button action
        message = get_message_detail_based_on_action(client_data['action'])

        upload_response = get_configuration_data(OrgClients, {'del_ind': False}, ['client', 'description'])

        return upload_response, message

    def save_number_range_data(self, number_range_data):

        number_range_db_list = []
        range_check_flag = False
        doc_type = ''
        for number_range_detail in number_range_data['data']:
            doc_type = number_range_detail['document_type']
            delete_flag = True
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(NumberRanges,
                                                                {'sequence': number_range_detail['sequence'],
                                                                 'client': self.client,
                                                                 'document_type': number_range_detail[
                                                                     'document_type'],
                                                                 }):
                number_ranges = django_query_instance.django_filter_query(NumberRanges,
                                                                          {'client': self.client,
                                                                           'del_ind': False,
                                                                           'document_type': number_range_detail[
                                                                               'document_type']}, None, None)
                for number_range in number_ranges:
                    range_check_flag = range_check(number_range_detail['starting'], number_range['starting'],
                                                   number_range['ending'])
                    if range_check_flag:
                        break
                    else:
                        range_check_flag = range_check(number_range_detail['ending'], number_range['starting'],
                                                       number_range['ending'])
                        if range_check_flag:
                            break
                if not range_check_flag:
                    num_guid = guid_generator()
                    number_range_db_dictionary = {'guid': num_guid,
                                                  'sequence': number_range_detail['sequence'],
                                                  'starting': number_range_detail['starting'],
                                                  'ending': number_range_detail['ending'],
                                                  'current': number_range_detail['current'],
                                                  'del_ind': False,
                                                  'client': self.client,
                                                  'document_type': DocumentType.objects.get
                                                  (document_type=number_range_detail[
                                                      'document_type']),
                                                  'number_ranges_changed_at': self.current_date_time,
                                                  'number_ranges_changed_by': self.username,
                                                  'number_ranges_created_at': self.current_date_time,
                                                  'number_ranges_created_by': self.username, }
                    number_range_db_list.append(number_range_db_dictionary)

            else:
                if number_range_detail['del_ind']:
                    if django_query_instance.django_existence_check(TransactionTypes,
                                                                    {'sequence': number_range_detail['sequence'],
                                                                     'client': self.client,
                                                                     'document_type':
                                                                         number_range_detail[
                                                                             'document_type'],
                                                                     }):
                        delete_flag = False
                if delete_flag:
                    django_query_instance.django_update_query(NumberRanges,
                                                              {'sequence': number_range_detail
                                                              ['sequence'],
                                                               'client': self.client,
                                                               'document_type': number_range_detail[
                                                                   'document_type'],
                                                               },
                                                              {'sequence': number_range_detail['sequence'],
                                                               'starting': number_range_detail['starting'],
                                                               'ending': number_range_detail['ending'],
                                                               'current': number_range_detail['current'],
                                                               'document_type': DocumentType.objects.get(
                                                                   document_type=number_range_detail[
                                                                       'document_type']),

                                                               'number_ranges_changed_at': self.current_date_time,
                                                               'number_ranges_changed_by': self.username,
                                                               'client': self.client,
                                                               'del_ind': number_range_detail['del_ind']})

        if number_range_db_list:
            bulk_create_entry_db(NumberRanges, number_range_db_list)

        return doc_type

    def save_number_range_data_into_db(self, number_range_data):
        """

        """
        doc_type = self.save_number_range_data(number_range_data)

        message = get_message_detail_based_on_action(number_range_data['action'])

        upload_response = get_configuration_data(NumberRanges,
                                                 {'del_ind': False, 'document_type': doc_type, 'client': self.client},
                                                 ['guid', 'sequence', 'starting', 'ending',
                                                  'current', 'document_type',
                                                  ])
        sequence = NumberRanges.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=doc_type,
                                               del_ind=False).aggregate(
            Max('sequence'))
        sequence_max = sequence['sequence__max']
        data = {'upload_response': upload_response, 'sequence_max': sequence_max}
        return data, message

    def save_document_type_data(self, documenttype_data):
        documenttype_db_list = []
        used_flag_set = []
        used_flag_reset = []
        for documenttype_detail in documenttype_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(DocumentType,
                                                                {'document_type': documenttype_detail[
                                                                    'document_type']}):
                documenttype_db_dictionary = {'document_type': (documenttype_detail['document_type']).upper(),
                                              'document_type_desc': convert_to_camel_case(
                                                  documenttype_detail['document_type_desc']),
                                              'document_type_created_at': self.current_date_time,
                                              'document_type_created_by': self.username,
                                              'document_type_changed_at': self.current_date_time,
                                              'document_type_changed_by': self.username}
                documenttype_db_list.append(documenttype_db_dictionary)
            else:
                django_query_instance.django_update_query(DocumentType,
                                                          {'document_type': documenttype_detail['document_type']},
                                                          {'document_type': documenttype_detail['document_type'],
                                                           'document_type_desc': convert_to_camel_case(
                                                               documenttype_detail[
                                                                   'document_type_desc']),
                                                           'document_type_changed_at': self.current_date_time,
                                                           'document_type_changed_by': self.username,
                                                           'del_ind': documenttype_detail['del_ind']})
            if documenttype_detail['del_ind']:
                used_flag_reset.append(documenttype_detail['document_type'])
            else:
                used_flag_set.append(documenttype_detail['document_type'])

        if documenttype_db_list:
            bulk_create_entry_db(DocumentType, documenttype_db_list)

        set_reset_field(used_flag_reset, used_flag_set, 'document_type')

    def save_documenttype_data_into_db(self, documenttype_data):
        self.save_document_type_data(documenttype_data)
        message = get_message_detail_based_on_action(documenttype_data['action'])

        upload_response = get_configuration_data(DocumentType, {'del_ind': False},
                                                 ['document_type', 'document_type_desc'])

        return upload_response, message

    def save_transaction_data(self, transactiontype_data):
        transactiontype_db_list = []
        doc_type = ''
        for transactiontype_detail in transactiontype_data['data']:
            doc_type = transactiontype_detail['document_type']
            active_inactive_field = transactiontype_detail['active_inactive']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(TransactionTypes,
                                                                {'transaction_type': transactiontype_detail[
                                                                    'transaction_type'],
                                                                 'sequence': transactiontype_detail['sequence'],
                                                                 'client': self.client
                                                                 }):
                guid = guid_generator()
                transactiontype_db_dictionary = {'guid': guid,
                                                 'transaction_type': (
                                                     transactiontype_detail['transaction_type']).upper(),
                                                 'description': convert_to_camel_case(
                                                     transactiontype_detail['description']),
                                                 'sequence': transactiontype_detail['sequence'],
                                                 'active_inactive': transactiontype_detail['active_inactive'],
                                                 'document_type': DocumentType.objects.get(
                                                     document_type=transactiontype_detail['document_type']),
                                                 'del_ind': False,
                                                 'client': self.client,
                                                 'transaction_types_created_at': self.current_date_time,
                                                 'transaction_types_created_by': self.username,
                                                 'transaction_types_changed_at': self.current_date_time,
                                                 'transaction_types_changed_by': self.username,
                                                 }
                transactiontype_db_list.append(transactiontype_db_dictionary)
            else:
                delete_flag = True
                if django_query_instance.django_existence_check(OrgAttributesLevel,
                                                                {'client': self.client,
                                                                 'low': transactiontype_detail['transaction_type'],
                                                                 'del_ind': False,
                                                                 'attribute_id': CONST_SC_TRANS_TYPE}):
                    delete_flag = False
                if delete_flag:
                    django_query_instance.django_update_query(TransactionTypes,
                                                              {'transaction_type': transactiontype_detail[
                                                                  'transaction_type'],
                                                               'sequence': transactiontype_detail['sequence'],
                                                               'client': self.client},
                                                              {'transaction_type': transactiontype_detail[
                                                                  'transaction_type'],
                                                               'description': convert_to_camel_case(
                                                                   transactiontype_detail[
                                                                       'description']),
                                                               'sequence': transactiontype_detail['sequence'],
                                                               'active_inactive': transactiontype_detail[
                                                                   'active_inactive'],
                                                               'document_type': DocumentType.objects.get(
                                                                   document_type=transactiontype_detail[
                                                                       'document_type']),
                                                               'transaction_types_changed_at': self.current_date_time,
                                                               'transaction_types_changed_by': self.username,
                                                               'client': self.client,
                                                               'del_ind': transactiontype_detail['del_ind']})
                else:
                    django_query_instance.django_update_query(TransactionTypes,
                                                              {'transaction_type': transactiontype_detail[
                                                                  'transaction_type'],
                                                               'sequence': transactiontype_detail['sequence'],
                                                               'client': self.client},
                                                              {'description': convert_to_camel_case(
                                                                  transactiontype_detail[
                                                                      'description']),
                                                                  'del_ind': transactiontype_detail['del_ind']
                                                              })

        if transactiontype_db_list:
            bulk_create_entry_db(TransactionTypes, transactiontype_db_list)
        return doc_type

    def save_transactiontype_data_into_db(self, transactiontype_data):
        doc_type = self.save_transaction_data(transactiontype_data)

        message = get_message_detail_based_on_action(transactiontype_data['action'])

        upload_response = get_configuration_data(TransactionTypes, {'del_ind': False, 'document_type': doc_type,
                                                                    'client': self.client},
                                                 ['guid', 'transaction_type', 'description', 'document_type',
                                                  'sequence',
                                                  'active_inactive'])

        return upload_response, message

    def save_calendar_data(self, calendar_data):
        calendar_db_list = []
        for calendar_detail in calendar_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(CalenderConfig,
                                                                {'calender_id': calendar_detail[
                                                                    'calender_id'],
                                                                 'client': self.client,
                                                                 }):
                guid = guid_generator()
                calendar_db_dictionary = {'calender_config_guid': guid,
                                          'calender_id': calendar_detail['calender_id'],
                                          'description': convert_to_camel_case(calendar_detail['description']),
                                          'year': calendar_detail['year'],
                                          'working_days': calendar_detail['working_days'],
                                          'del_ind': False,
                                          'client': self.client,
                                          'country_code': Country.objects.get(
                                              country_code=calendar_detail['country']),
                                          'calender_config_created_at': self.current_date_time,
                                          'calender_config_created_by': self.username,
                                          'calender_config_changed_at': self.current_date_time,
                                          'calender_config_changed_by': self.username
                                          }
                calendar_db_list.append(calendar_db_dictionary)
            else:
                django_query_instance.django_update_query(CalenderConfig,
                                                          {'calender_id': calendar_detail[
                                                              'calender_id'], 'client': self.client},
                                                          {'calender_id': calendar_detail['calender_id'],
                                                           'description': convert_to_camel_case(
                                                               calendar_detail['description']),
                                                           'year': calendar_detail['year'],
                                                           'working_days': calendar_detail['working_days'],
                                                           'country_code': Country.objects.get(
                                                               country_code=calendar_detail['country']),
                                                           'calender_config_changed_at': self.current_date_time,
                                                           'calender_config_changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': calendar_detail['del_ind']})
        if calendar_db_list:
            bulk_create_entry_db(CalenderConfig, calendar_db_list)

    def save_calendar_data_into_db(self, calendar_data):
        """

        """
        self.save_calendar_data(calendar_data)
        message = get_message_detail_based_on_action(calendar_data['action'])

        upload_response = get_configuration_data(CalenderConfig,
                                                 {'del_ind': False, 'client': self.client},
                                                 ['calender_config_guid', 'calender_id', 'description',
                                                  'year', 'working_days', 'country_code'])
        return upload_response, message

    def save_calendar_holiday(self, calendar_data):
        calendar_db_list = []
        for calendar_detail in calendar_data['data']:
            # if entry is not exists in db
            delete_holiday_data(calendar_detail['calender_id'])
            if not django_query_instance.django_existence_check(CalenderHolidays,
                                                                {'calender_holiday_guid': calendar_detail[
                                                                    'calender_holiday_guid']}):
                guid = guid_generator()
                calendar_db_dictionary = {'calender_holiday_guid': guid,
                                          'calender_id': calendar_detail['calender_id'],
                                          'holiday_description': convert_to_camel_case(
                                              calendar_detail['holiday_description']),
                                          'from_date': calendar_detail['from_date'],
                                          'to_date': calendar_detail['to_date'],
                                          'del_ind': False,
                                          'client': self.client,
                                          'created_at': self.current_date_time,
                                          'created_by': self.username,
                                          'changed_at': self.current_date_time,
                                          'changed_by': self.username
                                          }
                calendar_db_list.append(calendar_db_dictionary)
            else:
                django_query_instance.django_update_query(CalenderHolidays,
                                                          {'calender_holiday_guid': calendar_detail[
                                                              'calender_holiday_guid']},
                                                          {'calender_holiday_guid': calendar_detail[
                                                              'calender_holiday_guid'],
                                                           'calender_id': calendar_detail['calender_id'],
                                                           'holiday_description': convert_to_camel_case(
                                                               calendar_detail[
                                                                   'holiday_description']),
                                                           'from_date': calendar_detail['from_date'],
                                                           'to_date': calendar_detail['to_date'],
                                                           'changed_at': self.current_date_time,
                                                           'changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': calendar_detail['del_ind']})
        bulk_create_entry_db(CalenderHolidays, calendar_db_list)

    def save_calendarholiday_data_into_db(self, calendar_data):
        """

        """
        self.save_calendar_holiday(calendar_data)

        message = get_message_detail_based_on_action(calendar_data['action'])

        upload_response = get_configuration_data(CalenderHolidays,
                                                 {'del_ind': False,
                                                  'client': self.client},
                                                 ['calender_holiday_guid', 'calender_id', 'holiday_description',
                                                  'from_date', 'to_date'])
        return upload_response, message

    def save_acc_asg_data(self, accasscat_data):
        accasscat_db_list = []
        fieldtypedesc_instance = FieldTypeDescriptionUpdate()
        acct_assmt_field = ''
        used_flag_set = []
        used_flag_reset = []
        for accasscat_detail in accasscat_data['data']:
            acct_assmt_field = accasscat_detail['account_assign_cat']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                                {'account_assign_cat': accasscat_detail[
                                                                    'account_assign_cat']}):
                accasscat_db_dictionary = {'account_assign_cat': (accasscat_detail['account_assign_cat']).upper(),
                                           'description': convert_to_camel_case(accasscat_detail['description']),
                                           'del_ind': False,
                                           'account_assignment_category_created_at': self.current_date_time,
                                           'account_assignment_category_created_by': self.username,
                                           'account_assignment_category_changed_at': self.current_date_time,
                                           'account_assignment_category_changed_by': self.username
                                           }
                accasscat_db_list.append(accasscat_db_dictionary)
            else:
                django_query_instance.django_update_query(AccountAssignmentCategory,
                                                          {'account_assign_cat': accasscat_detail[
                                                              'account_assign_cat']},
                                                          {'account_assign_cat': accasscat_detail[
                                                              'account_assign_cat'],
                                                           'description': convert_to_camel_case(
                                                               accasscat_detail['description']),
                                                           'account_assignment_category_changed_at': self.current_date_time,
                                                           'account_assignment_category_changed_by': self.username,
                                                           'del_ind': accasscat_detail['del_ind']})
            if accasscat_detail['del_ind']:
                used_flag_reset.append(accasscat_detail['account_assign_cat'])
            else:
                used_flag_set.append(accasscat_detail['account_assign_cat'])
        bulk_create_entry_db(AccountAssignmentCategory, accasscat_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'acct_assignment_category')

    def save_actasmt_data_into_db(self, accasscat_data):
        """

        """
        self.save_acc_asg_data(accasscat_data)

        message = get_message_detail_based_on_action(accasscat_data['action'])

        upload_response = get_configuration_data(AccountAssignmentCategory, {'del_ind': False},
                                                 ['account_assign_cat', 'description'])

        return upload_response, message

    def save_po_split_type(self, po_split_types):
        accasscat_db_list = []
        used_flag_set = []
        used_flag_reset = []
        acct_assmt_field = ''
        for po_split_type in po_split_types['data']:
            acct_assmt_field = po_split_type['po_split_type']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(PoSplitType,
                                                                {'po_split_type': po_split_type[
                                                                    'po_split_type']}):
                accasscat_db_dictionary = {'po_split_type': (po_split_type['po_split_type']).upper(),
                                           'po_split_type_desc': convert_to_camel_case(
                                               po_split_type['description']),
                                           'del_ind': False,
                                           'po_split_type_created_at': self.current_date_time,
                                           'po_split_type_created_by': self.username,
                                           'po_split_type_changed_at': self.current_date_time,
                                           'po_split_type_changed_by': self.username
                                           }
                accasscat_db_list.append(accasscat_db_dictionary)
            else:
                django_query_instance.django_update_query(PoSplitType,
                                                          {'po_split_type': po_split_type[
                                                              'po_split_type']},
                                                          {'po_split_type': po_split_type[
                                                              'po_split_type'],
                                                           'po_split_type_desc': convert_to_camel_case(
                                                               po_split_type['po_split_type_desc']),
                                                           'po_split_type_changed_at': self.current_date_time,
                                                           'po_split_type_changed_by': self.username,
                                                           'del_ind': po_split_type['del_ind']})
            if po_split_type['del_ind']:
                used_flag_reset.append(po_split_type['po_split_type'])
            else:
                used_flag_set.append(po_split_type['po_split_type'])
        bulk_create_entry_db(PoSplitType, accasscat_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'split_type')

    def save_po_split_type_into_db(self, po_split_type):
        """

        """
        self.save_po_split_type(po_split_type)

        message = get_message_detail_based_on_action(po_split_type['action'])

        upload_response = get_configuration_data(PoSplitType,
                                                 {'del_ind': False},
                                                 ['po_split_type', 'po_split_type_desc'])

        return upload_response, message

    def save_po_split_creteria(self, po_split_creteria):
        accasscat_db_list = []
        for po_split in po_split_creteria['data']:

            # if entry is not exists in db
            if not django_query_instance.django_existence_check(PoSplitCriteria,
                                                                {'po_split_type': int(po_split[
                                                                                          'po_split_type']),
                                                                 'company_code_id':
                                                                     po_split['company_code_id'],
                                                                 'client': self.client
                                                                 }):

                guid = guid_generator()
                accasscat_db_dictionary = {'po_split_criteria_guid': guid,
                                           'po_split_type': PoSplitType.objects.get(
                                               po_split_type=int(po_split['po_split_type'])),
                                           'company_code_id': po_split['company_code_id'],
                                           'activate': po_split['activate'],
                                           'del_ind': False,
                                           'client': self.client,
                                           'po_split_criteria_created_at': self.current_date_time,
                                           'po_split_criteria_created_by': self.username,
                                           'po_split_criteria_changed_at': self.current_date_time,
                                           'po_split_criteria_changed_by': self.username
                                           }
                accasscat_db_list.append(accasscat_db_dictionary)
            else:
                django_query_instance.django_update_query(PoSplitCriteria,
                                                          {
                                                              'po_split_type':
                                                                  int(po_split['po_split_type']),
                                                              'company_code_id':
                                                                  po_split['company_code_id'],
                                                              'client': self.client
                                                          },

                                                          {'po_split_type': PoSplitType.objects.get(
                                                              po_split_type=int(po_split['po_split_type'])),
                                                              'company_code_id':
                                                                  po_split['company_code_id'],
                                                              'activate':
                                                                  po_split['activate'],
                                                              'po_split_criteria_changed_at': self.current_date_time,
                                                              'po_split_criteria_changed_by': self.username,
                                                              'del_ind': po_split['del_ind'],
                                                              'client': OrgClients.objects.get(client=self.client)})
        bulk_create_entry_db(PoSplitCriteria, accasscat_db_list)

    def save_po_split_criteria_into_db(self, accasscat_data):
        """

        """
        self.save_po_split_creteria(accasscat_data)

        message = get_message_detail_based_on_action(accasscat_data['action'])

        upload_response = get_product_criteria()

        return upload_response, message

    def save_purchase_control(self, purhcase_control_data):
        pur_ctrl_db_list = []

        for pur_crtl_detail in purhcase_control_data['data']:

            # if entry is not exists in db
            if not django_query_instance.django_existence_check(PurchaseControl,
                                                                {
                                                                    'company_code_id':
                                                                        pur_crtl_detail['company_code_id'],
                                                                    'call_off':
                                                                        pur_crtl_detail['call_off'],
                                                                    'client': self.client
                                                                }):

                guid = guid_generator()
                pur_crtl_db_dictionary = {'purchase_control_guid': guid,
                                          'company_code_id': pur_crtl_detail['company_code_id'],
                                          'call_off': pur_crtl_detail['call_off'],
                                          'purchase_ctrl_flag': pur_crtl_detail['purchase_ctrl_flag'],
                                          'del_ind': False,
                                          'client': self.client,
                                          'purchase_control_created_at': self.current_date_time,
                                          'purchase_control_created_by': self.username,
                                          'purchase_control_changed_at': self.current_date_time,
                                          'purchase_control_changed_by': self.username
                                          }
                pur_ctrl_db_list.append(pur_crtl_db_dictionary)
            else:
                django_query_instance.django_update_query(PurchaseControl,
                                                          {
                                                              'company_code_id':
                                                                  pur_crtl_detail['company_code_id'],
                                                              'call_off':
                                                                  pur_crtl_detail['call_off'],
                                                              'client': self.client
                                                          },

                                                          {
                                                              'company_code_id':
                                                                  pur_crtl_detail['company_code_id'],
                                                              'call_off':
                                                                  pur_crtl_detail['call_off'],
                                                              'purchase_ctrl_flag':
                                                                  pur_crtl_detail['purchase_ctrl_flag'],
                                                              'purchase_control_changed_at': self.current_date_time,
                                                              'purchase_control_changed_by': self.username,
                                                              'del_ind': pur_crtl_detail['del_ind'],
                                                              'client': OrgClients.objects.get(client=self.client)})
        bulk_create_entry_db(PurchaseControl, pur_ctrl_db_list)

    def save_purchase_control_into_db(self, purhcase_control_data):
        """

        """
        self.save_purchase_control(purhcase_control_data)
        message = get_message_detail_based_on_action(purhcase_control_data['action'])

        upload_response = get_configuration_data(PurchaseControl,
                                                 {'del_ind': False},
                                                 ['purchase_control_guid', 'company_code_id', 'call_off',
                                                  'purchase_ctrl_flag'])

        return upload_response, message

    def save_messageId_data_into_db(self, messageId_data):
        """

        """

        self.save_message_id(messageId_data['data'])
        message = get_message_detail_based_on_action(messageId_data['action'])

        upload_response = get_configuration_data(MessagesId,
                                                 {'del_ind': False,
                                                  'client': self.client},
                                                 ['msg_id_guid', 'messages_id', 'messages_type'])
        return upload_response, message

    def save_message_id(self, messageId_data):
        """

        """
        messageId_db_list = []
        for messageId_detail in messageId_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(MessagesId,
                                                                {'messages_id': messageId_detail[
                                                                    'message_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                messageId_db_dictionary = {'msg_id_guid': guid,
                                           'messages_id': messageId_detail['message_id'],
                                           'messages_type': messageId_detail['message_type'],
                                           'del_ind': False,
                                           'client': self.client,
                                           'messages_id_created_at': self.current_date_time,
                                           'messages_id_created_by': self.username,
                                           'messages_id_changed_at': self.current_date_time,
                                           'messages_id_changed_by': self.username
                                           }
                messageId_db_list.append(messageId_db_dictionary)
            else:
                django_query_instance.django_update_query(MessagesId,
                                                          {'messages_id': messageId_detail[
                                                              'message_id'], 'client': self.client},
                                                          {'messages_id': messageId_detail['message_id'],
                                                           'messages_type': messageId_detail['message_type'],
                                                           'messages_id_changed_at': self.current_date_time,
                                                           'messages_id_changed_by': self.username,
                                                           'del_ind': messageId_detail['del_ind'],
                                                           'client': self.client})
        bulk_create_entry_db(MessagesId, messageId_db_list)

    def save_messageIdDesc_data_into_db(self, messageIdDesc_data):
        """

        """

        self.save_message_id_desc(messageIdDesc_data['data'])
        message = get_message_detail_based_on_action(messageIdDesc_data['action'])

        upload_response = get_configuration_data(MessagesIdDesc, {'del_ind': False, 'client': self.client},
                                                 ['msg_id_desc_guid', 'messages_id', 'messages_id_desc', 'language_id'])
        return upload_response, message

    def save_message_id_desc(self, messageIdDesc_data):
        """

        """
        messageIdDesc_db_list = []
        for messageIdDesc_detail in messageIdDesc_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(MessagesIdDesc,
                                                                {'messages_id': messageIdDesc_detail[
                                                                    'messages_id'],
                                                                 'language_id': messageIdDesc_detail['language_id'],
                                                                 'client': self.client
                                                                 }):
                guid = guid_generator()
                messageIdDesc_db_dictionary = {'msg_id_desc_guid': guid,
                                               'messages_id': messageIdDesc_detail['messages_id'],
                                               'messages_id_desc': convert_to_camel_case(
                                                   messageIdDesc_detail['messages_id_desc']),
                                               'language_id': Languages.objects.get(
                                                   language_id=messageIdDesc_detail['language_id']),
                                               'del_ind': False,
                                               'client': self.client,
                                               'messages_id_desc_created_at': self.current_date_time,
                                               'messages_id_desc_created_by': self.username,
                                               'messages_id_desc_changed_at': self.current_date_time,
                                               'messages_id_desc_changed_by': self.username
                                               }
                messageIdDesc_db_list.append(messageIdDesc_db_dictionary)
            else:
                django_query_instance.django_update_query(MessagesIdDesc,
                                                          {'messages_id': messageIdDesc_detail[
                                                              'messages_id'],
                                                           'language_id': messageIdDesc_detail['language_id'],
                                                           'client': self.client
                                                           },
                                                          {'messages_id': messageIdDesc_detail['messages_id'],
                                                           'messages_id_desc': convert_to_camel_case(
                                                               messageIdDesc_detail['messages_id_desc']),
                                                           'language_id': Languages.objects.get(
                                                               language_id=messageIdDesc_detail['language_id']),
                                                           'messages_id_desc_changed_at': self.current_date_time,
                                                           'messages_id_desc_changed_by': self.username,
                                                           'del_ind': messageIdDesc_detail['del_ind'],
                                                           'client': self.client})
        bulk_create_entry_db(MessagesIdDesc, messageIdDesc_db_list)

    def save_orgnode_types_data_into_db(self, orgnode_data):

        self.save_org_node_type(orgnode_data['data'])

        message = get_message_detail_based_on_action(orgnode_data['action'])

        upload_response = get_configuration_data(OrgNodeTypes,
                                                 {'del_ind': False, 'client': self.client},
                                                 ['node_type_guid', 'node_type',
                                                  'description'])

        return upload_response, message

    def save_org_node_type(self, orgnode_data):
        """

        """
        orgnode_data_db_list = []
        used_flag_set = []
        used_flag_reset = []
        for orgnode_detail in orgnode_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgNodeTypes,
                                                                {'node_type': orgnode_detail['node_type'],
                                                                 'client': self.client}):
                guid = guid_generator()
                orgnode_db_dictionary = {'node_type_guid': guid,
                                         'node_type': (orgnode_detail['node_type']).upper(),
                                         'description': convert_to_camel_case(orgnode_detail['description']),
                                         'del_ind': False,
                                         'client': self.client,
                                         'org_node_types_changed_at': self.current_date_time,
                                         'org_node_types_changed_by': self.username,
                                         'org_node_types_created_at': self.current_date_time,
                                         'org_node_types_created_by': self.username,
                                         }

                orgnode_data_db_list.append(orgnode_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgNodeTypes,
                                                          {'node_type': orgnode_detail['node_type'],
                                                           'client': self.client},
                                                          {
                                                              'node_type': orgnode_detail['node_type'],
                                                              'description': convert_to_camel_case(
                                                                  orgnode_detail['description']),
                                                              'org_node_types_changed_at': self.current_date_time,
                                                              'org_node_types_changed_by': self.username,
                                                              'client': self.client,
                                                              'del_ind': orgnode_detail['del_ind']})
            if orgnode_detail['del_ind']:
                used_flag_reset.append(orgnode_detail['node_type'])
            else:
                used_flag_set.append(orgnode_detail['node_type'])

        bulk_create_entry_db(OrgNodeTypes, orgnode_data_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'org_node_types')

    def save_orgattributes_data_into_db(self, attr_data):

        self.save_attributes(attr_data['data'])

        message = get_message_detail_based_on_action(attr_data['action'])

        upload_response = get_configuration_data(OrgAttributes, {'del_ind': False},
                                                 ['attribute_id', 'attribute_name',
                                                  'range_indicator', 'multiple_value',
                                                  'allow_defaults', 'inherit_values',
                                                  'maximum_length'])

        return upload_response, message

    def save_attributes(self, attr_data):
        """

        """
        attr_data_db_list = []
        used_flag_set = []
        used_flag_reset = []
        for attr_detail in attr_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgAttributes,
                                                                {'attribute_id': attr_detail['attribute_id']}):

                attr_db_dictionary = {'attribute_id': (attr_detail['attribute_id']).upper(),
                                      'attribute_name': convert_to_camel_case(attr_detail['attribute_name']),
                                      'range_indicator': attr_detail['range_indicator'],
                                      'multiple_value': attr_detail['multiple_value'],
                                      'allow_defaults': attr_detail['allow_defaults'],
                                      'inherit_values': attr_detail['inherit_values'],
                                      'maximum_length': attr_detail['maximum_length'],
                                      'del_ind': False,
                                      'org_attributes_changed_at': self.current_date_time,
                                      'org_attributes_changed_by': self.username,
                                      'org_attributes_created_at': self.current_date_time,
                                      'org_attributes_created_by': self.username}

                attr_data_db_list.append(attr_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgAttributes,
                                                          {'attribute_id': attr_detail['attribute_id']},
                                                          {'attribute_id': attr_detail['attribute_id'],
                                                           'attribute_name': convert_to_camel_case(
                                                               attr_detail['attribute_name']),
                                                           'range_indicator': attr_detail['range_indicator'],
                                                           'multiple_value': attr_detail['multiple_value'],
                                                           'allow_defaults': attr_detail['allow_defaults'],
                                                           'inherit_values': attr_detail['inherit_values'],
                                                           'maximum_length': attr_detail['maximum_length'],
                                                           'org_attributes_changed_at': self.current_date_time,
                                                           'org_attributes_changed_by': self.username,
                                                           'del_ind': attr_detail['del_ind']})
            if attr_detail['del_ind']:
                used_flag_reset.append(attr_detail['attribute_id'])
            else:
                used_flag_set.append(attr_detail['attribute_id'])

        bulk_create_entry_db(OrgAttributes, attr_data_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'attribute_id')

    def save_authorobject_data_into_db(self, authobj_data):
        self.save_auth_obj(authobj_data['data'], self.username)

        message = get_message_detail_based_on_action(authobj_data['action'])

        upload_response = get_configuration_data(AuthorizationObject, {'del_ind': False},
                                                 ['auth_obj_id', 'auth_level_ID',
                                                  'auth_level'])

        return upload_response, message

    def save_auth_obj(self, authobj_data, username):
        authobj_data_db_list = []
        used_flag_set = []
        used_flag_reset = []
        used_flag_set1 = []
        used_flag_reset1 = []
        for authobj_detail in authobj_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AuthorizationObject,
                                                                {'auth_obj_id': authobj_detail['auth_obj_id']}):

                authobj_db_dictionary = {'auth_obj_id': (authobj_detail['auth_obj_id']).upper(),
                                         'auth_level_ID': (authobj_detail['auth_level_ID']).upper(),
                                         'auth_level': (authobj_detail['auth_level']).upper(),
                                         'del_ind': False,
                                         'authorization_object_changed_at': self.current_date_time,
                                         'authorization_object_changed_by': username,
                                         'authorization_object_created_at': self.current_date_time,
                                         'authorization_object_created_by': username,
                                         }

                authobj_data_db_list.append(authobj_db_dictionary)
            else:

                django_query_instance.django_update_query(AuthorizationObject,
                                                          {'auth_obj_id': authobj_detail['auth_obj_id']},
                                                          {'auth_obj_id': authobj_detail['auth_obj_id'],
                                                           'auth_level_ID': authobj_detail['auth_level_ID'],
                                                           'auth_level': (authobj_detail['auth_level']).upper(),
                                                           'authorization_object_changed_at': self.current_date_time,
                                                           'authorization_object_changed_by': username,
                                                           'del_ind': authobj_detail['del_ind']})
            if authobj_detail['del_ind']:
                used_flag_reset.append(authobj_detail['auth_obj_id'])
                used_flag_reset1.append(authobj_detail['auth_level'])
            else:
                used_flag_set.append(authobj_detail['auth_obj_id'])
                used_flag_set1.append(authobj_detail['auth_level'])

        bulk_create_entry_db(AuthorizationObject, authobj_data_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'auth_obj_id')
        set_reset_field(used_flag_reset1, used_flag_set1, 'auth_level')

    def save_auth_data_into_db(self, auth_data):

        self.save_auth(auth_data['data'])

        message = get_message_detail_based_on_action(auth_data['action'])

        upload_response = get_configuration_data(Authorization, {'del_ind': False, 'client': self.client},
                                                 ['role', 'auth_obj_grp', 'auth_guid'])

        upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDescription,
                                                                                 {'del_ind': False, 'used_flag': False,
                                                                                  'field_name': 'authorization',
                                                                                  'client': self.client},
                                                                                 ['field_type_id', 'field_type_desc'])
        return upload_response, message, upload_fieldtypedesc

    def save_auth(self, auth_data):
        """

        """
        auth_db_list = []
        roles_type_field = ''
        used_flag_set = []
        used_flag_reset = []
        for auth_detail in auth_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Authorization,
                                                                {'role': auth_detail['role'],
                                                                 'client': self.client
                                                                 }):

                guid = guid_generator()
                auth_db_dictionary = {'auth_guid': guid,
                                      'role': UserRoles.objects.get(role=auth_detail['role']),
                                      'auth_obj_grp': auth_detail['auth_obj_grp'],
                                      'del_ind': False,
                                      'client': self.client,
                                      'authorization_changed_at': self.current_date_time,
                                      'authorization_changed_by': self.username,
                                      'authorization_created_at': self.current_date_time,
                                      'authorization_created_by': self.username,
                                      }
                auth_db_list.append(auth_db_dictionary)
                fieldtypedesc_instance.update_usedFlag(roles_type_field)
            else:
                django_query_instance.django_update_query(Authorization,
                                                          {'role': auth_detail['role'],
                                                           'client': self.client
                                                           },
                                                          {'auth_obj_grp': auth_detail['auth_obj_grp'],
                                                           'role': UserRoles.objects.get(role=auth_detail['role']),
                                                           'authorization_changed_at': self.current_date_time,
                                                           'authorization_changed_by': self.username,
                                                           'client': self.client,
                                                           'del_ind': auth_detail['del_ind']})
            if auth_detail['del_ind']:
                used_flag_reset.append(auth_detail['role'])
            else:
                used_flag_set.append(auth_detail['role'])
        bulk_create_entry_db(Authorization, auth_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'authorization')

    def save_orgattributes_level_data(self, orgattlevel_data):
        orgattlevel_db_list = []
        for orgattlevel_detail in orgattlevel_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                                {'node_type': orgattlevel_detail['node_type'],
                                                                 'node_values': orgattlevel_detail['node_values'],
                                                                 'org_model_types': 'ORG_ATTRIBUTES',
                                                                 'client': self.client}):

                guid = guid_generator()
                prodcatdesc_db_dictionary = {'org_model_nodetype_config_guid': guid,
                                             'node_type': orgattlevel_detail['node_type'],
                                             'node_values': orgattlevel_detail['node_values'],
                                             'org_model_types': 'ORG_ATTRIBUTES',
                                             'org_model_nodetype_config_created_at': self.current_date_time,
                                             'org_model_nodetype_config_created_by': self.username,
                                             'org_model_nodetype_config_changed_at': self.current_date_time,
                                             'org_model_nodetype_config_changed_by': self.username,
                                             'client': self.client
                                             }

                orgattlevel_db_list.append(prodcatdesc_db_dictionary)
            else:
                django_query_instance.django_update_query(OrgModelNodetypeConfig,
                                                          {'node_type': orgattlevel_detail['node_type'],
                                                           'node_values': orgattlevel_detail['node_values'],
                                                           'org_model_types': 'ORG_ATTRIBUTES',
                                                           'client': self.client},
                                                          {'node_type': orgattlevel_detail['node_type'],
                                                           'org_model_types': 'ORG_ATTRIBUTES',
                                                           'node_values': orgattlevel_detail['node_values'],
                                                           'org_model_nodetype_config_changed_at': self.current_date_time,
                                                           'org_model_nodetype_config_changed_by': self.username,
                                                           'del_ind': orgattlevel_detail['del_ind'],
                                                           'client': OrgClients.objects.get(client=self.client)})
        bulk_create_entry_db(OrgModelNodetypeConfig, orgattlevel_db_list)

    def save_orgattributes_level_data_into_db(self, orgattlevel_data):
        self.save_orgattributes_level_data(orgattlevel_data)

        message = get_message_detail_based_on_action(orgattlevel_data['action'])

        upload_response = get_configuration_data(OrgModelNodetypeConfig, {'del_ind': False,
                                                                          'client': self.client},
                                                 ['org_model_nodetype_config_guid', 'node_type', 'node_values'])

        return upload_response, message

    def save_auth_group_data_into_db(self, auth_group_data):
        self.save_auth_grp(auth_group_data['data'])

        message = get_message_detail_based_on_action(auth_group_data['action'])

        upload_response = get_configuration_data(AuthorizationGroup, {'del_ind': False},
                                                 ['auth_grp_guid', 'auth_obj_grp', 'auth_grp_desc', 'auth_level',
                                                  'auth_obj_id'
                                                  ])

        return upload_response, message

    def save_auth_grp(self, auth_group_data):
        """

        """
        auth_group_db_list = []
        for auth_group_detail in auth_group_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AuthorizationGroup,
                                                                {'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                                 'auth_obj_id': auth_group_detail['auth_obj_id']}):
                guid = guid_generator()
                auth_group_db_dictionary = {'auth_grp_guid': guid,
                                            'auth_obj_grp': auth_group_detail['auth_obj_grp'].upper(),
                                            'auth_grp_desc': convert_to_camel_case(auth_group_detail['auth_grp_desc']),
                                            'auth_level': auth_group_detail['auth_level'].upper(),
                                            'auth_obj_id': AuthorizationObject.objects.get(
                                                auth_obj_id=auth_group_detail['auth_obj_id']),
                                            'del_ind': False,
                                            'authorization_group_changed_at': self.current_date_time,
                                            'authorization_group_changed_by': self.username,
                                            'authorization_group_created_at': self.current_date_time,
                                            'authorization_group_created_by': self.username,
                                            }
                auth_group_db_list.append(auth_group_db_dictionary)

            else:

                django_query_instance.django_update_query(AuthorizationGroup,
                                                          {'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                           'auth_obj_id': auth_group_detail['auth_obj_id'],
                                                           },
                                                          {
                                                              'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                              'auth_grp_desc': convert_to_camel_case(
                                                                  auth_group_detail['auth_grp_desc']),
                                                              'auth_level': auth_group_detail['auth_level'],
                                                              'auth_obj_id': AuthorizationObject.objects.get(
                                                                  auth_obj_id=auth_group_detail['auth_obj_id']),
                                                              'authorization_group_changed_at': self.current_date_time,
                                                              'authorization_group_changed_by': self.username,
                                                              'del_ind': auth_group_detail['del_ind']})
        bulk_create_entry_db(AuthorizationGroup, auth_group_db_list)

    def save_roles_data_into_db(self, roles_data):
        self.save_user_roles(roles_data['data'])

        message = get_message_detail_based_on_action(roles_data['action'])

        upload_response = get_configuration_data(UserRoles, {'del_ind': False}, ['role', 'role_desc'])
        upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDescription,
                                                                                 {'del_ind': False, 'used_flag': False,
                                                                                  'field_name': 'roles',
                                                                                  'client': self.client},
                                                                                 ['field_type_id', 'field_type_desc'])

        return upload_response, message, upload_fieldtypedesc

    def save_user_roles(self, roles_data):
        """

        """
        roles_db_list = []
        roles_type_field = ''
        used_flag_set = []
        used_flag_reset = []
        for roles_detail in roles_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UserRoles,
                                                                {'role': roles_detail['role']}):
                roles_db_dictionary = {'role': roles_detail['role'].upper(),
                                       'role_desc': convert_to_camel_case(roles_detail['role_desc']),
                                       'user_roles_created_at': self.current_date_time,
                                       'user_roles_created_by': self.username,
                                       'user_roles_changed_at': self.current_date_time,
                                       'user_roles_changed_by': self.username
                                       }
                roles_db_list.append(roles_db_dictionary)
                fieldtypedesc_instance.update_usedFlag(roles_type_field)
            else:
                django_query_instance.django_update_query(UserRoles,
                                                          {'role': roles_detail['role']},
                                                          {'role': roles_detail['role'],
                                                           'role_desc': roles_detail['role_desc'],
                                                           'user_roles_changed_at': self.current_date_time,
                                                           'user_roles_changed_by': self.username,
                                                           'del_ind': roles_detail['del_ind']})
            if roles_detail['del_ind']:
                used_flag_reset.append(roles_detail['role'])
            else:
                used_flag_set.append(roles_detail['role'])

        bulk_create_entry_db(UserRoles, roles_db_list)
        set_reset_field(used_flag_reset, used_flag_set, 'roles')

    def save_email_settings_into_db(self, email_data):
        """

        """
        variant_list = []
        self.save_email_settings(email_data['data'])
        message = get_message_detail_based_on_action(email_data['action'])

        upload_response = get_configuration_data(EmailContents,
                                                 {'del_ind': False,
                                                  'client': self.client},
                                                 ['email_contents_guid', 'object_type', 'subject', 'header', 'body',
                                                  'footer', 'language_id'])
        variant_values = get_configuration_data(EmailObjectTypes,
                                                {'del_ind': False,
                                                 'client': self.client},
                                                ['object_type'])
        for variant_names in variant_values:
            variant_list.append(variant_names['object_type'])

        return upload_response, message, variant_list

    def save_email_settings(self, email_data):
        """

        """
        emailSettings_db_list = []
        for emailSettings_detail in email_data:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(EmailContents,
                                                                {'object_type': emailSettings_detail['email_type'],
                                                                 'language_id': emailSettings_detail['language_id'],
                                                                 'client': self.client}):
                guid = guid_generator()
                emailSettings_db_dictionary = {'email_contents_guid': guid,
                                               'object_type': emailSettings_detail['email_type'],
                                               'subject': emailSettings_detail['email_subject'],
                                               'header': emailSettings_detail['email_header'],
                                               'body': emailSettings_detail['email_body'],
                                               'footer': emailSettings_detail['email_footer'],
                                               'language_id': Languages.objects.get(
                                                   language_id=emailSettings_detail['language_id']),
                                               'del_ind': False,
                                               'client': self.client,
                                               'email_contents_created_at': self.current_date_time,
                                               'email_contents_created_by': self.username,
                                               'email_contents_changed_at': self.current_date_time,
                                               'email_contents_changed_by': self.username
                                               }
                emailSettings_db_list.append(emailSettings_db_dictionary)
            else:
                django_query_instance.django_update_query(EmailContents,
                                                          {'object_type': emailSettings_detail['email_type'],
                                                           'language_id': emailSettings_detail['language_id'],
                                                           'client': self.client},
                                                          {'object_type': emailSettings_detail['email_type'],
                                                           'subject': emailSettings_detail['email_subject'],
                                                           'header': emailSettings_detail['email_header'],
                                                           'body': emailSettings_detail['email_body'],
                                                           'footer': emailSettings_detail['email_footer'],
                                                           'language_id': Languages.objects.get(
                                                               language_id=emailSettings_detail['language_id']),
                                                           'email_contents_changed_at': self.current_date_time,
                                                           'email_contents_changed_by': self.username,
                                                           'del_ind': emailSettings_detail['del_ind'],
                                                           'client': self.client})
        bulk_create_entry_db(EmailContents, emailSettings_db_list)


class SystemSettingConfig:
    def __init__(self, client):
        self.client = client

    def update_system_attributes(self, sys_attr_value, sys_attr_type):
        django_query_instance.django_filter_only_query(SystemSettingsConfig, {
            'client': self.client, 'del_ind': False, 'sys_attr_value': sys_attr_value, 'sys_attr_type': sys_attr_type
        }).update(sys_settings_default_flag=True)


def node_type_dropdown():
    data = {
        'upload_dropdown_db_values': get_field_unused_list_values('org_node_types')

    }
    return data


def node_type_data():
    upload_orgnodetypes = list(
        OrgNodeTypes.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('node_type_guid',
                                                                                                 'node_type',
                                                                                                 'description'))

    for node_type_fd in upload_orgnodetypes:
        if django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                        {'del_ind': False,
                                                         'node_type': node_type_fd['node_type']}):
            node_type_fd["del_ind_flag"] = False
        else:
            node_type_fd["del_ind_flag"] = True

    return upload_orgnodetypes


def org_attr_dropdown():
    upload_dropdown_db_values = get_field_unused_list_values('attribute_id')

    data = {
        'upload_dropdown_db_values': upload_dropdown_db_values,
    }
    return data


def org_attr_data():
    upload_orgattributes = list(
        OrgAttributes.objects.filter(del_ind=False).values('attribute_id', 'attribute_name', 'range_indicator',
                                                           'multiple_value', 'allow_defaults', 'inherit_values',
                                                           'maximum_length'))

    for attribute_id_fd in upload_orgattributes:
        if django_query_instance.django_existence_check(OrgModelNodetypeConfig,
                                                        {'del_ind': False,
                                                         'node_values': attribute_id_fd['attribute_id']}):
            attribute_id_fd["del_ind_flag"] = False
        else:
            attribute_id_fd["del_ind_flag"] = True

    return upload_orgattributes


def orgattr_level_dropdown():
    upload_attributesid_dropdown = django_query_instance.django_filter_query(
        OrgAttributes, {'del_ind': False}, None, ['attribute_id'])

    upload_orgnodetypes_dropdown = django_query_instance.django_filter_query(
        OrgNodeTypes, {'client': global_variables.GLOBAL_CLIENT, 'del_ind': False}, None, ['node_type'])
    data = {
        'upload_attributesid_dropdown': upload_attributesid_dropdown,
        'upload_orgnodetypes_dropdown': upload_orgnodetypes_dropdown
    }
    return data


def orgattr_level_data():
    upload_orgattributes_level = django_query_instance.django_filter_query(
        OrgModelNodetypeConfig, {'del_ind': False, 'org_model_types': 'ORG_ATTRIBUTES'}, None,
        ['org_model_nodetype_config_guid',
         'node_values', 'node_type'])

    return upload_orgattributes_level


def auth_object_dropdown():
    auth_obj_id_db_values = get_field_unused_list_values('auth_obj_id')

    auth_type_db_values = get_field_list_values('auth_level')
    data = {
        'auth_obj_id_db_values': auth_obj_id_db_values,
        'auth_type_db_values': auth_type_db_values
    }
    return data


def auth_object_data():
    upload_authobj = list(
        AuthorizationObject.objects.filter(del_ind=False).values('auth_obj_id', 'auth_level_ID',
                                                                 'auth_level'))
    for authobject_fd in upload_authobj:
        if django_query_instance.django_existence_check(AuthorizationGroup,
                                                        {'del_ind': False,
                                                         'auth_obj_id': authobject_fd['auth_obj_id']}):
            authobject_fd["del_ind_flag"] = False
        else:
            authobject_fd["del_ind_flag"] = True
    return upload_authobj


def auth_grp_dropdown():
    upload_data_AuthorizationGroup = list(
        AuthorizationObject.objects.filter(del_ind=False).values('auth_obj_id', 'auth_level_ID'))

    auth_group_db_values = get_field_list_values('auth_obj_grp')
    auth_type_db_values = get_field_list_values('auth_level')

    data = {
        'upload_data_AuthorizationGroup': upload_data_AuthorizationGroup,
        'auth_group_db_values': auth_group_db_values,
        'auth_type_db_values': auth_type_db_values
    }
    return data


def auth_grp_data():
    upload_authgrp = list(
        AuthorizationGroup.objects.filter(del_ind=False).values('auth_grp_guid', 'auth_obj_grp', 'auth_obj_id',
                                                                'auth_grp_desc', 'auth_level'))
    for authgrp_fd in upload_authgrp:
        if django_query_instance.django_existence_check(Authorization,
                                                        {'del_ind': False,
                                                         'auth_obj_grp': authgrp_fd['auth_obj_grp']}):
            authgrp_fd["del_ind_flag"] = False
        else:
            authgrp_fd["del_ind_flag"] = True
    return upload_authgrp


def user_roles_dropdown():
    dropdown_db_values = get_field_unused_list_values('roles')
    data = {
        'dropdown_db_values': dropdown_db_values
    }
    return data


def user_roles_data():
    upload_roles = list(UserRoles.objects.filter(del_ind=False).values('role', 'role_desc'))
    for roles_fd in upload_roles:
        if django_query_instance.django_existence_check(Authorization,
                                                        {'del_ind': False,
                                                         'role': roles_fd['role']}):
            roles_fd["del_ind_flag"] = False
        else:
            roles_fd["del_ind_flag"] = True
    return upload_roles


def authorization_dropdown():
    upload_dropdown_db_values = get_field_unused_list_values('authorization')
    data = {
        'dropdown_db_values': upload_dropdown_db_values
    }
    return data


def authorization_data():
    upload_auth = list(
        Authorization.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('auth_guid',
                                                                                                  'auth_obj_grp'
                                                                                                  'role'))
    for auth_fd in upload_auth:
        if django_query_instance.django_existence_check(UserRoles,
                                                        {'del_ind': False,
                                                         'role': auth_fd['role']}):
            auth_fd["del_ind_flag"] = False
        else:
            auth_fd["del_ind_flag"] = True
    return upload_auth


def document_dropdown():
    dropdown_db_values = get_field_unused_list_values('document_type')

    data = {
        'dropdown_db_values': dropdown_db_values,
    }
    return data


def document_data():
    upload_doc_type = django_query_instance.django_filter_query(DocumentType, {'del_ind': False}, None,
                                                                ['document_type', 'document_type_desc'])
    return upload_doc_type


def accasscat_dropdown():
    dropdown_acct_assmt_values = get_field_unused_list_values('acct_assignment_category')
    data = {
        'dropdown_acct_assmt_values': dropdown_acct_assmt_values,
    }
    return data


def accasscat_data():
    upload_account_assign_cat = django_query_instance.django_filter_query(AccountAssignmentCategory, {'del_ind': False},
                                                                          None, ['account_assign_cat', 'description'])
    for acccat_fd in upload_account_assign_cat:
        if not django_query_instance.django_existence_check(DetermineGLAccount,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'account_assign_cat': acccat_fd['account_assign_cat'],
                                                             'del_ind': False}):
            acccat_fd["del_ind_flag"] = False
        else:
            acccat_fd["del_ind_flag"] = True
    return accasscat_data


def po_split_type_dropdown():
    dropdown_acct_assmt_values = get_field_unused_list_values('split_type')
    data = {
        'dropdown_acct_assmt_values': dropdown_acct_assmt_values,

    }
    return data


def po_split_type_data():
    upload_account_assign_cat = django_query_instance.django_filter_query(PoSplitType, {'del_ind': False},
                                                                          None, ['po_split_type', 'po_split_type_desc'])
    for potyp_fd in upload_account_assign_cat:
        if not django_query_instance.django_existence_check(PoSplitCriteria,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'po_split_type': potyp_fd['po_split_type'],
                                                             'del_ind': False}):
            potyp_fd["del_ind_flag"] = False
        else:
            potyp_fd["del_ind_flag"] = True

    return upload_account_assign_cat


def posplit_criteria_dropdown():
    """

    """
    upload_account_assign_cat = get_configuration_data(PoSplitCriteria,
                                                       {'del_ind': False,
                                                        'client': global_variables.GLOBAL_CLIENT},
                                                       ['po_split_criteria_guid', 'company_code_id', 'activate',
                                                        'po_split_type'])
    po_split_types = django_query_instance.django_filter_query(PoSplitType, {'del_ind': False}, None, None)
    for po_criteria in upload_account_assign_cat:
        for po_split_type in po_split_types:
            if po_split_type['po_split_type'] == po_criteria['po_split_type']:
                po_criteria['po_split_type_desc'] = str(po_split_type['po_split_type']) + ' - ' + po_split_type[
                    'po_split_type_desc']

    po_split_typ = django_query_instance.django_filter_query(PoSplitType, {'del_ind': False}, None,
                                                             ['po_split_type', 'po_split_type_desc'])
    for po_dropdown in po_split_typ:
        po_dropdown['po_split_type_desc'] = str(po_dropdown['po_split_type']) + ' - ' + po_dropdown[
            'po_split_type_desc']

    dropdown_activate = get_field_list_values('activate')

    upload_data_company = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))

    data = {'po_split_typ': po_split_typ,
            'dropdown_activate': dropdown_activate,
            'upload_data_company': upload_data_company}
    return data


def posplit_criteria_data():
    """

    """
    upload_account_assign_cat = django_query_instance.django_filter_query(PoSplitCriteria,
                                                                          {'del_ind': False,
                                                                           'client': global_variables.GLOBAL_CLIENT},
                                                                          None,
                                                                          ['po_split_criteria_guid', 'company_code_id',
                                                                           'activate',
                                                                           'po_split_type'])
    data = get_po_split_creteria_dropdown(upload_account_assign_cat)
    data['upload_account_assign_cat'] = upload_account_assign_cat
    return data


def purchase_control_dropdown():
    dropdown_activate = get_field_list_values('purchase_ctrl_flag')

    upload_company_code = list(
        OrgCompanies.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('company_id'))
    data = {
        'dropdown_activate': dropdown_activate,
        'upload_company_code': upload_company_code
    }
    return data


def purchase_control_data():
    upload_purchase_control = django_query_instance.django_filter_query(PurchaseControl, {'del_ind': False}, None,
                                                                        ['purchase_control_guid', 'company_code_id',
                                                                         'call_off',
                                                                         'purchase_ctrl_flag'])
    return upload_purchase_control


def msgid_dropdown():
    dropdown_msg_type_values = get_field_list_values('messages_type')
    dropdown_msg_id_values = get_field_unused_list_values('messages_id')
    data = {
        'dropdown_msg_type_values': dropdown_msg_type_values,
        'dropdown_msg_id_values': dropdown_msg_id_values
    }
    return data


def msgid_data():
    message_id_data = django_query_instance.django_filter_query(MessagesId, {'del_ind': False,
                                                                             'client': global_variables.GLOBAL_CLIENT},
                                                                None,
                                                                ['msg_id_guid', 'messages_id', 'messages_type'])
    return message_id_data


def msgdesc_dropdown():
    messages_id_list = list(
        MessagesId.objects.filter(del_ind=False, client=global_variables.GLOBAL_CLIENT).values('messages_id'))
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    data = {
        'messages_id_list': messages_id_list,
        'language_list': language_list
    }
    return data


def msgdesc_data():
    message_id_desc_data = django_query_instance.django_filter_query(MessagesIdDesc, {'del_ind': False,
                                                                                      'client': global_variables.GLOBAL_CLIENT},
                                                                     None,
                                                                     ['msg_id_desc_guid', 'messages_id',
                                                                      'messages_id_desc',
                                                                      'language_id'])
    return message_id_desc_data


def calendar_dropdown():
    country_list = get_country_data()
    data = {'country_list': country_list}
    return data


def calendar_dropdown_data():
    calender_data = django_query_instance.django_filter_query(CalenderConfig,
                                                              {'del_ind': False},
                                                              None,
                                                              ['calender_config_guid', 'calender_id', 'description',
                                                               'year', 'working_days', 'country_code'])
    country_code = list(CalenderConfig.objects.filter(del_ind=False).values_list('country_code', flat=True))
    country_desc = django_query_instance.django_filter_query(Country,
                                                             {'country_code__in': country_code,
                                                              'del_ind': False},
                                                             None, None)

    var1 = []
    var2 = []
    for calender in calender_data:
        for country in country_desc:
            if calender['country_code'] == country['country_code']:
                if country['country_name']:
                    calender['country_desc'] = country['country_name']
                else:
                    calender['country_desc'] = country['country_code']
        # for i in range(len(calender['working_days'])):
        res_array = []

        for cw in calender['working_days']:
            if not cw == ',':
                res_array.append(weekday(cw))
                val_dict = {'value': res_array}
        var1.append(res_array)
        var2.append(val_dict)
        calender['wday_array'] = res_array
    return calender_data


def holiday_data():
    holidays_data = list(CalenderHolidays.objects.filter(del_ind=False).values('calender_holiday_guid', 'calender_id',
                                                                               'holiday_description', 'from_date',
                                                                               'to_date'))
    return holidays_data


def transaction_fc_dropdown():
    number_range_sequence = []
    upload_numberrange = list(
        NumberRanges.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_FC,
                                    del_ind=False).values('sequence'))
    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_FC,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_FC).values('document_type'))

    data = {
        'rendered_active_inactive': rendered_active_inactive,
        'document_type_render': document_type_render,
        'rendered_sequence': number_range_sequence
    }
    return data


def transaction_fc_data():
    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_FC,
                                        del_ind=False).values('guid',
                                                              'transaction_type',
                                                              'description',
                                                              'document_type',
                                                              'sequence',
                                                              'active_inactive'))
    return upload_transactiontype


def transaction_sc_dropdown():
    number_range_sequence = []
    upload_numberrange = list(
        NumberRanges.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_SC,
                                    del_ind=False).values('sequence'))
    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_SC,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_SC).values('document_type'))

    data = {
        'rendered_active_inactive': rendered_active_inactive,
        'document_type_render': document_type_render,
        'rendered_sequence': number_range_sequence
    }
    return data


def transaction_sc_data():
    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_SC,
                                        del_ind=False).values('guid',
                                                              'transaction_type',
                                                              'description',
                                                              'document_type',
                                                              'sequence',
                                                              'active_inactive'))
    return upload_transactiontype


def transaction_po_dropdown():
    number_range_sequence = []
    upload_numberrange = list(
        NumberRanges.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_PO,
                                    del_ind=False).values('sequence'))
    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_PO,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_PO).values('document_type'))

    data = {
        'rendered_active_inactive': rendered_active_inactive,
        'document_type_render': document_type_render,
        'rendered_sequence': number_range_sequence
    }
    return data


def transaction_po_data():
    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_PO,
                                        del_ind=False).values('guid',
                                                              'transaction_type',
                                                              'description',
                                                              'document_type',
                                                              'sequence',
                                                              'active_inactive'))
    return upload_transactiontype


def transaction_gv_dropdown():
    number_range_sequence = []
    upload_numberrange = list(
        NumberRanges.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_CONF,
                                    del_ind=False).values('sequence'))
    for number_range in upload_numberrange:
        if not django_query_instance.django_existence_check(TransactionTypes,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'sequence': number_range['sequence'],
                                                             'document_type': CONST_DOC_TYPE_CONF,
                                                             'del_ind': False}):
            number_range_sequence.append(number_range)
    rendered_active_inactive = list(
        FieldTypeDescription.objects.filter(field_name='active_inactive', del_ind=False,
                                            client=global_variables.GLOBAL_CLIENT).values('field_type_id',
                                                                                          'field_type_desc'))
    document_type_render = list(
        DocumentType.objects.filter(del_ind=False, document_type=CONST_DOC_TYPE_CONF).values('document_type'))

    data = {
        'rendered_active_inactive': rendered_active_inactive,
        'document_type_render': document_type_render,
        'rendered_sequence': number_range_sequence
    }
    return data


def transaction_gv_data():
    upload_transactiontype = list(
        TransactionTypes.objects.filter(client=global_variables.GLOBAL_CLIENT, document_type=CONST_DOC_TYPE_CONF,
                                        del_ind=False).values('guid',
                                                              'transaction_type',
                                                              'description',
                                                              'document_type',
                                                              'sequence',
                                                              'active_inactive'))
    return upload_transactiontype


def delete_holiday_data(calender_id):
    django_query_instance.django_filter_delete_query(CalenderHolidays, {'calender_id': calender_id})
    return True
