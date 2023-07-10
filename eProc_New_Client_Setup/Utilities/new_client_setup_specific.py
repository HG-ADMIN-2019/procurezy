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
        # save OrgAttributes
        self.org_attribute_script(directory)
        # save Roles
        self.user_roles_script(directory)
        #  save   auth obj
        self.auth_obj_script(directory)
        #     save auth
        self.auth_script(directory)
        #     save auth
        self.auth_grp_script(directory)
        #     save field type
        self.field_desc_script(directory)
        #     save field type
        self.field_type_script(directory)
        #     save message id
        self.message_id_script(directory)
        # save messages desc
        self.message_id_desc_script(directory)
        # save system settings
        self.system_settings_script(directory)

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
                csv_to_db_data.append({'SYS_ATTR_TYPE': csv_data[1],
                                       'SYS_ATTR_VALUE': csv_data[2],
                                       'del_ind': csv_data[3]})
            self.system_settings_new(csv_to_db_data)


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
