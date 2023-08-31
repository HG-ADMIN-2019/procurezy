import os
import csv

from Majjaka_eProcure import *
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic_Settings.Utilities.basic_settings_specific import *
from eProc_Configuration.Utilities.application_settings_specific import *
from eProc_Configuration.models import *
from eProc_Master_Settings.Utilities.master_settings_specific import *
from eProc_Org_Model.Utilities.apiHandler import ApiHandler

django_query_instance = DjangoQueries()


class InitialSetupClient(BasicSettingsSave, ApplicationSettingsSave, MasterSettingsSave):
    def __init__(self, client):
        super().__init__()
        self.client = django_query_instance.django_get_query(OrgClients,
                                                             {'client': client})
        self.username = CONST_SYSTEM_USER

    def initial_save_basic_data(self):
        """

        """
        directory = os.path.join(str(settings.BASE_DIR), 'MajjakaScript', 'basic_data')
        for root, dirs, files in os.walk(directory):
            for file in files:
                # check for csv file
                if file.endswith(".csv") or file.endswith(".CSV"):
                    file_path = os.path.join(directory, file)  # create path
                    csv_file = open(file_path, 'r')  # open .csv file
                    csvreader = csv.reader(csv_file)  # read file
                    header = next(csvreader)  # skip header
                    csv_to_db_data = []

                    if file == CONST_COUNTRIES_CSV:
                        for csv_data in csvreader:
                            csv_to_db_data.append({'country_code': csv_data[0],
                                                   'country_name': csv_data[1],
                                                   'del_ind': csv_data[2]})
                        self.save_country(csv_to_db_data)
                    if file == CONST_CURRENCY_CSV:
                        for csv_data in csvreader:
                            csv_to_db_data.append({'currency_id': csv_data[0],
                                                   'description': csv_data[1],
                                                   'del_ind': csv_data[2]})
                        self.save_currency(csv_to_db_data)
                    if file == CONST_TIMEZONE_CSV:
                        for csv_data in csvreader:
                            csv_to_db_data.append({'time_zone': csv_data[0],
                                                   'description': csv_data[1],
                                                   'utc_difference': csv_data[2],
                                                   'daylight_save_rule': csv_data[3],
                                                   'del_ind': csv_data[4],
                                                   })
                        self.save_time_zone(csv_to_db_data)
                    if file == CONST_LANGUAGES_CSV:
                        for csv_data in csvreader:
                            csv_to_db_data.append({'language_id': csv_data[0],
                                                   'description': csv_data[1],
                                                   'del_ind': csv_data[2],
                                                   })
                        self.save_languages(csv_to_db_data)
                    if file == CONST_UOM_CSV:
                        for csv_data in csvreader:
                            csv_to_db_data.append({'uom_id': csv_data[0],
                                                   'uom_description': csv_data[1],
                                                   'iso_code_id': csv_data[2],
                                                   'del_ind': csv_data[3],
                                                   })
                        self.save_uom(csv_to_db_data)
                    if file == CONST_PRODUCT_CATEGORY_CSV:
                        for csv_data in csvreader:
                            csv_to_db_data.append({'prod_cat_id': csv_data[0],
                                                   'prod_cat_desc': csv_data[1],
                                                   'del_ind': csv_data[2],
                                                   })
                        self.save_unspsc(csv_to_db_data)
                    csv_file.close()

    def initial_save_application_data(self):
        """

        """
        directory = os.path.join(str(settings.BASE_DIR), 'MajjakaScript', 'application_data')
        # Save  OrgNodeTypes data
        self.org_node_type_script(directory)
        # # save OrgAttributes
        self.org_attribute_script(directory)
        # # save Roles
        self.user_roles_script(directory)
        # #  save   auth obj
        self.auth_obj_script(directory)
        # #     save auth
        self.auth_script(directory)
        # #     save auth
        self.auth_grp_script(directory)
        # #     save field type
        self.field_desc_script(directory)
        # #     save field type
        self.field_type_script(directory)
        # #     save message id
        self.message_id_script(directory)
        # # save messages desc
        self.message_id_desc_script(directory)
        # # save system settings
        self.system_settings_script(directory)
        # # save node level attributes
        self.node_level_attribute_script(directory)
        # # save email
        self.email_contents_script(directory)
        # save UNSPC
        self.Unspc_code_script(directory)
        # save DOCUMENTS
        self.document_type_script(directory)
        # save ACC ASS CAT CUST
        self.acc_ass_cat_cust_type_script(directory)
        # save CALENDER
        self.calendar_script(directory)
        # save HOLIDAY CALENDER
        self.holiday_calendar_script(directory)
        # save PURCHASE SPLIT TYPE
        self.purchase_order_split_criteria_script(directory)
        # save PURCHASE ORDER SPLIT TYPE
        self.purchase_order_split_criteria_script(directory)
        # save PURCHASE CONTROL
        self.purchase_control_script(directory)
        # save FAVOURITE CART
        self.favourite_cart_script(directory)
        # save SHOPPING CART
        self.shopping_cart_script(directory)
        # save PURCHASE ORDER
        self.purchase_order_script(directory)
        # save FAVOURITE CART
        self.favourite_transaction_script(directory)
        # save SHOPPING CART
        self.shopping_transaction_script(directory)
        # save PURCHASE ORDER
        self.purchase_transaction_script(directory)

    def org_node_type_script(self, directory):
        file_path = os.path.join(directory, CONST_ORG_NODE_TYPES_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'node_type': csv_data[0],
                                       'description': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_org_node_type(csv_to_db_data)

    def org_attribute_script(self, directory):
        file_path = os.path.join(directory, CONST_ORG_ATTRIBUTES_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'attribute_id': csv_data[0], 'attribute_name': csv_data[1],
                                       'range_indicator': csv_data[2], 'multiple_value': csv_data[3],
                                       'allow_defaults': csv_data[4], 'inherit_values': csv_data[5],
                                       'maximum_length': csv_data[5], 'del_ind': csv_data[7]})
            self.save_attributes(csv_to_db_data)

    def user_roles_script(self, directory):
        file_path = os.path.join(directory, CONST_USER_ROLES_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'role': csv_data[0],
                                       'role_desc': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_user_roles(csv_to_db_data)

    def auth_obj_script(self, directory):
        file_path = os.path.join(directory, CONST_AUTHORIZATION_OBJECT)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'auth_obj_id': csv_data[0],
                                       'auth_level': csv_data[1],
                                       'auth_level_ID': csv_data[2],
                                       'auth_level_desc': csv_data[3],
                                       'del_ind': csv_data[4]})
            self.save_auth_obj(csv_to_db_data)

    def auth_script(self, directory):
        file_path = os.path.join(directory, CONST_AUTHORIZATION)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'auth_obj_grp': csv_data[0],
                                       'auth_type': csv_data[1],
                                       'role': csv_data[2],
                                       'del_ind': csv_data[3]})
            self.save_auth(csv_to_db_data)

    def auth_grp_script(self, directory):
        """

        """
        file_path = os.path.join(directory, CONST_AUTHORIZATION_GROUP)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'auth_obj_grp': csv_data[0],
                                       'auth_grp_desc': csv_data[1],
                                       'auth_level': csv_data[2],
                                       'auth_obj_id': csv_data[3],
                                       'del_ind': csv_data[4]})
            self.save_auth_grp(csv_to_db_data)

    def field_desc_script(self, directory):
        file_path = os.path.join(directory, CONST_FIELD_DESC)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'field_name': csv_data[0],
                                       'field_desc': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_field_desc(csv_to_db_data)

    def field_type_script(self, directory):
        file_path = os.path.join(directory, CONST_FIELD_TYPE_DESC)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'field_type_id': csv_data[0],
                                       'field_type_desc': csv_data[1],
                                       'used_flag': csv_data[2],
                                       'del_ind': csv_data[3],
                                       'field_name': csv_data[4]})
            self.save_field_type_desc(csv_to_db_data)

    def message_id_script(self, directory):
        file_path = os.path.join(directory, CONST_MESSAGE_ID_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'message_id': csv_data[0],
                                       'message_type': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_message_id(csv_to_db_data)

    def message_id_desc_script(self, directory):
        file_path = os.path.join(directory, CONST_MESSAGE_ID_DESC_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'messages_id': csv_data[0],
                                       'messages_id_desc': csv_data[1],
                                       'messages_category': csv_data[2],
                                       'language_id': csv_data[3],
                                       'del_ind': csv_data[4]})
            self.save_message_id_desc(csv_to_db_data)

    def system_settings_script(self, directory):
        file_path = os.path.join(directory, CONST_SYSTEM_SETTINGS_CONFIG_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'sys_attr_type': csv_data[0],
                                       'sys_attr_value': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_system_settings(csv_to_db_data)

    def node_level_attribute_script(self, directory):
        file_path = os.path.join(directory, CONST_ORG_NODE_LEVEL_ATTRIBUTES_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'node_type': csv_data[0],
                                       'node_values': csv_data[1],
                                       'org_model_types': csv_data[2],
                                       'del_ind': csv_data[3]})
            self.save_orgattributes_level_data(csv_to_db_data)

    def email_contents_script(self, directory):
        file_path = os.path.join(directory, CONST_EMAIL_CONTENTS_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'object_type': csv_data[0],
                                       'subject': csv_data[1],
                                       'header': csv_data[2],
                                       'body': csv_data[3],
                                       'footer': csv_data[4],
                                       'language_id': csv_data[5],
                                       'del_ind': csv_data[6]})
            self.save_email_settings(csv_to_db_data)

    def Unspc_code_script(self, directory):
        file_path = os.path.join(directory, CONST_UNSPSC_CODE_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'prod_cat_id': csv_data[0],
                                       'prod_cat_desc': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_unspsc(csv_to_db_data)

    def document_type_script(self, directory):
        file_path = os.path.join(directory, CONST_DOCUMENT_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'document_type': csv_data[0],
                                       'document_type_desc': csv_data[1],
                                       'del_ind': csv_data[2]})
            documenttype_data = {'data': csv_to_db_data}  # Wrap the data in a dictionary
            self.save_document_type_data(documenttype_data)  # Pass the wrapped data to the function

    def acc_ass_cat_cust_type_script(self, directory):
        file_path = os.path.join(directory, CONST_ACCOUNT_ASSIGNMENT_CATEGORY_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'ACCOUNT_ASSIGN_CAT': csv_data[0],
                                       'DESCRIPTION': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_acc_asg_data(csv_to_db_data)

    def calendar_script(self, directory):
        file_path = os.path.join(directory, CONST_CALENDAR_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'calender_id': csv_data[0],  # Use 'calender_id' here
                                       'country_code': csv_data[1],  # Use 'country_code' here
                                       'description': csv_data[2],  # Use 'description' here
                                       'year': csv_data[3],  # Use 'year' here
                                       'working_days': csv_data[4],  # Use 'working_days' here
                                       'del_ind': csv_data[5]})  # Use 'del_ind' here
            calendar_data = {'data': csv_to_db_data}
            self.save_calendar_data(calendar_data)

    def holiday_calendar_script(self, directory):
        file_path = os.path.join(directory, CONST_CALENDAR_HOLIDAY_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'CALENDER_ID': csv_data[0],
                                       'COUNTRY_CODE': csv_data[1],
                                       'DESCRIPTION': csv_data[2],
                                       'YEAR': csv_data[3],
                                       'del_ind': csv_data[4]})
            self.save_calendar_holiday(csv_to_db_data)

    def purchase_order_split_type_script(self, directory):
        file_path = os.path.join(directory, CONST_PO_SPLIT_TYPE_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'PO_SPLIT_TYPE': csv_data[0],
                                       'PO_SPLIT_TYPE_DESC': csv_data[1],
                                       'del_ind': csv_data[2]})
            self.save_po_split_type(csv_to_db_data)

    def purchase_order_split_criteria_script(self, directory):
        file_path = os.path.join(directory, CONST_PO_SPLIT_CRITERIA_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'po_split_type': csv_data[0],
                                       'company_code_id': csv_data[1],
                                       'activate': csv_data[2],
                                       'del_ind': csv_data[3]})
            self.save_po_split_creteria(csv_to_db_data)

    def purchase_control_script(self, directory):
        file_path = os.path.join(directory, CONST_PURCHASE_CONTROL_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'company_code_id': csv_data[0],
                                       'call_off': csv_data[1],
                                       'purchase_ctrl_flag': csv_data[2],
                                       'del_ind': csv_data[3]})
            self.save_purchase_control(csv_to_db_data)

    def favourite_cart_script(self, directory):
        file_path = os.path.join(directory, CONST_FAVOURITE_CART_NUMBER_RANGE_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'sequence': int(csv_data[0]),
                                       'starting': int(csv_data[1]),
                                       'ending': int(csv_data[2]),
                                       'current': int(csv_data[3]),
                                       'document_type': csv_data[4],
                                       'del_ind':int(csv_data[5])})
            number_range_data = {'data': csv_to_db_data}

            self.save_number_range_data(number_range_data)

    def shopping_cart_script(self, directory):
        file_path = os.path.join(directory, CONST_SHOPPING_CART_NUMBER_RANGE_CSV)
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')
            csvreader = csv.reader(csv_file)
            header = next(csvreader)
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'sequence': csv_data[0],
                                       'starting': csv_data[1],
                                       'ending': csv_data[2],
                                       'current': csv_data[3],
                                       'document_type': csv_data[4],
                                       'del_ind': csv_data[5]})

            # Wrap the csv_to_db_data list in a dictionary with 'data' key
            number_range_data = {'data': csv_to_db_data}

            self.save_number_range_data(number_range_data)

    def purchase_order_script(self, directory):
        file_path = os.path.join(directory, CONST_PURCHASE_ORDER_NUMBER_RANGE_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'sequence': csv_data[0],
                                       'starting': csv_data[1],
                                       'ending': csv_data[2],
                                       'current': csv_data[3],
                                       'document_type': csv_data[4],
                                       'del_ind': csv_data[5]})
            number_range_data = {'data': csv_to_db_data}

            self.save_number_range_data(number_range_data)

    def favourite_transaction_script(self, directory):
        file_path = os.path.join(directory, CONST_FAVOURITE_TRANSACTION_TYPE_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'transaction_type': csv_data[0],
                                       'description': csv_data[1],
                                       'sequence': csv_data[2],
                                       'active_inactive': csv_data[3],
                                       'document_type': csv_data[4],
                                       'del_ind': csv_data[5]})
            transaction_data = {'data': csv_to_db_data}

            self.save_transaction_data(transaction_data)

    def shopping_transaction_script(self, directory):
        file_path = os.path.join(directory, CONST_SHOPPING_CART_TRANSACTION_TYPE_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'transaction_type': csv_data[0],
                                       'description': csv_data[1],
                                       'sequence': csv_data[2],
                                       'active_inactive': csv_data[3],
                                       'document_type': csv_data[4],
                                       'del_ind': csv_data[5]})
            transaction_data = {'data': csv_to_db_data}

            self.save_transaction_data(transaction_data)

    def purchase_transaction_script(self, directory):
        file_path = os.path.join(directory, CONST_PURCHASE_ORDER_TRANSACTION_TYPE_CSV)  # create path
        if os.path.exists(file_path):
            csv_file = open(file_path, 'r')  # open .csv file
            csvreader = csv.reader(csv_file)  # read file
            header = next(csvreader)  # skip header
            csv_to_db_data = []
            for csv_data in csvreader:
                csv_to_db_data.append({'transaction_type': csv_data[0],
                                       'description': csv_data[1],
                                       'sequence': csv_data[2],
                                       'active_inactive': csv_data[3],
                                       'document_type': csv_data[4],
                                       'del_ind': csv_data[5]})
            transaction_data = {'data': csv_to_db_data}

            self.save_transaction_data(transaction_data)


def create_organization_structure(client_id):
    """

    """
    org_model_detail = None
    if django_query_instance.django_existence_check(OrgClients,
                                                    {'client': client_id}):
        client_detail = django_query_instance.django_get_query(OrgClients,
                                                               {'client': client_id})
        org_name = 'RNODE_' + str(client_detail.client)
        if not django_query_instance.django_existence_check(OrgNames,
                                                            {'name': org_name,
                                                             'client': client_id}):
            ApiHandler.create_organization(client_id, org_name)
            org_model_detail = django_query_instance.django_get_query(OrgModel,
                                                                      {'name': org_name,
                                                                       'client': client_id})
        if org_model_detail:
            node_name = 'NODE_' + str(client_detail.client)
            ApiHandler.save_node(client_id, node_name, 'NODE',
                                 org_model_detail.node_guid, org_model_detail.root_node_object_id)


def check_data_setup(client_id):
    """

    """
    data_setup_flag = True
    # check for basic data table
    if not django_query_instance.django_existence_check(Country, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(Currency, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(Languages, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(UnspscCategories, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(TimeZone, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(UnitOfMeasures, {'del_ind': False}):
        data_setup_flag = False
    # check for application data table
    if not django_query_instance.django_existence_check(OrgNodeTypes, {'del_ind': False, 'client': client_id}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(OrgAttributes, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(UserRoles, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(AuthorizationGroup, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(AuthorizationObject, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(Authorization, {'del_ind': False, 'client': client_id}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(FieldDesc, {'del_ind': False}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(FieldTypeDescription, {'del_ind': False, 'client': client_id}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(MessagesId, {'del_ind': False, 'client': client_id}):
        data_setup_flag = False
    if not django_query_instance.django_existence_check(MessagesIdDesc, {'del_ind': False, 'client': client_id}):
        data_setup_flag = False

    return data_setup_flag


def check_org_setup(client_id):
    """

    """
    org_set_up_flag = True

    if django_query_instance.django_existence_check(OrgClients,
                                                    {'client': client_id}):
        client_detail = django_query_instance.django_get_query(OrgClients,
                                                               {'client': client_id})
        org_name = 'RNODE_' + str(client_detail.client)
        node_name = 'NODE_' + str(client_detail.client)
        if not django_query_instance.django_existence_check(OrgNames,
                                                            {'name': org_name,
                                                             'client': client_id}):
            org_set_up_flag = False
        if not django_query_instance.django_existence_check(OrgModel,
                                                            {'name__in': [org_name, node_name],
                                                             'client': client_id}):
            org_set_up_flag = False
    else:
        org_set_up_flag = False
    return org_set_up_flag


def check_user(client_id):
    """

    """
    user_flag = True
    if not django_query_instance.django_existence_check(UserData,
                                                        {'client': client_id}):
        user_flag = False
    return user_flag


def check_status(client_detail):
    """

    """
    status = ''
    if client_detail['data_setup_flag'] == True and client_detail['org_setup_flag'] == True and client_detail[
        'user_flag']:
        status = 'COMPLETED'
    elif client_detail['data_setup_flag'] == False and client_detail['org_setup_flag'] == False and client_detail[
        'user_flag'] == False:
        status = 'READY'
    else:
        status = 'PROGRESS'
    return status


def get_client_data():
    """"
    """
    client_details = django_query_instance.django_filter_query(OrgClients,
                                                               {'del_ind': False},
                                                               None,
                                                               ['client', 'description'])
    for client_detail in client_details:
        client_detail['data_setup_flag'] = check_data_setup(client_detail['client'])
        client_detail['org_setup_flag'] = check_org_setup(client_detail['client'])
        client_detail['user_flag'] = check_user(client_detail['client'])
        client_detail['status'] = check_status(client_detail)
        if client_detail['status'] == 'READY':
            client_detail['edit_update_flag'] = True
        else:
            client_detail['edit_update_flag'] = False
    return client_details


def delete_client_from_db(client_id):
    """

    """
    try:
        django_query_instance.django_filter_delete_query(OrgClients,
                                                         {'client': client_id})
        return True
    except ProtectedError:
        return False


def delete_application_setup_client(client_id):
    """

    """
    django_query_instance.django_filter_delete_query(OrgNodeTypes, {'client': client_id})
    django_query_instance.django_filter_delete_query(Authorization, {'client': client_id})
    django_query_instance.django_filter_delete_query(FieldTypeDescription, {'client': client_id})
    django_query_instance.django_filter_delete_query(MessagesIdDesc, {'client': client_id})
