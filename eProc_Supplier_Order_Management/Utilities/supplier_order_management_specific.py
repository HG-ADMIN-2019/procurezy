import datetime

from unicodedata import decimal

from eProc_Basic.Utilities.constants.constants import CONST_CC
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
from eProc_Basic.Utilities.functions.guid_generator import guid_generator, random_int
from eProc_Basic.Utilities.functions.string_related_functions import remove_space
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Supplier_Order_Management.models.supplier_order_management_models import SOMPoHeader, SOMPoItem, \
    SOMEformFieldData, SOMPoAccounting

django_query_instance = DjangoQueries()


def get_po_data(text, header_detail):
    """

    """
    supplier_address = {'supplier_address_detail': '', 'invoice_address': '', 'delivery_address': ''}
    header_detail['invoicing_detail'] = ''
    index = 0
    flag = False
    buyer_flag = False
    invoice_address = False
    pdf_invoice_address_flag = False
    delivery_address_flag = False
    incoterm_flag = False
    company_name_flag = False
    payment_term_flag = False
    invoicing_detail_flag = False
    goods_recep_flag = False
    supplier_note_text_flag = False
    supplier_id_flag = False
    for count, po_data in enumerate(text):
        if po_data.find("PURCHASE ORDER NO") != -1:
            header_detail['doc_number'] = remove_space(po_data.split(':')[1])
        if flag:
            if not po_data.find("Buyer") != -1:
                if supplier_id_flag:
                    header_detail['supplier_id'] = po_data
                    supplier_id_flag = False
                supplier_address['supplier_address_detail'] = supplier_address[
                                                                  'supplier_address_detail'] + ' ' + po_data
            else:
                if po_data.find("Buyer") != -1:
                    data = po_data.split('Buyer')
                    supplier_address['supplier_address_detail'] = supplier_address['supplier_address_detail'] + ' ' + \
                                                                  data[0]
                    buyer_flag = True
                    flag = False
        if po_data == "Vendor":
            flag = True
            supplier_id_flag = True
        if incoterm_flag:
            header_detail['incoterm'] = po_data.split('Terms of Payment')[0]
            payment_term_flag = True
            incoterm_flag = False
        if po_data == 'Terms of Delivery (In accordance with INCOTERMS 2010)':
            incoterm_flag = True
            delivery_address_flag = False
        if delivery_address_flag:
            supplier_address['delivery_address'] = supplier_address['delivery_address'] + ' ' + po_data
            if company_name_flag:
                header_detail['requester_company_name'] = po_data
                company_name_flag = False
        if goods_recep_flag:
            header_detail['goods_recep'] = po_data
            goods_recep_flag = False
        if po_data == 'Goods Receiver':
            goods_recep_flag = True
        if supplier_note_text_flag:
            if not po_data == 'Order line no. Product no. Product Order quantity UOM Unit price excl.':
                header_detail['supplier_note_text'] = po_data
            supplier_note_text_flag = False
        if po_data == 'Note(s) to Supplier':
            supplier_note_text_flag = True
        if invoicing_detail_flag:
            if not po_data.find('Goods Marking'):
                header_detail['invoicing_detail'] = header_detail['invoicing_detail'] + ' ' + po_data
            else:
                header_detail['invoicing_detail'] = header_detail['invoicing_detail'] + ' ' + \
                                                    po_data.split('Goods Marking')[0]
                invoicing_detail_flag = False
        if po_data == 'Invoicing':
            invoicing_detail_flag = True
            payment_term_flag = False
        if payment_term_flag:
            header_detail['payment_term'] = po_data

        if pdf_invoice_address_flag:
            header_detail['pdf_invoice_address'] = po_data.split('Delivery Address')[0]
            delivery_address_flag = True
            company_name_flag = True
            pdf_invoice_address_flag = False
        if po_data == 'PDF Invoice Address':
            invoice_address = False
            pdf_invoice_address_flag = True
            delivery_address_flag = False
        if po_data == 'Invoice Address':
            invoice_address = True
        if invoice_address:
            supplier_address['invoice_address'] = supplier_address['invoice_address'] + ' ' + po_data

    return header_detail, supplier_address


def get_po_table_data(po_table_details, header_detail):
    """

    """

    for row_count, po_table_detail in enumerate(po_table_details['data']):
        for cell_count, text_data in enumerate(po_table_detail):
            if row_count == 0:
                if cell_count == 0:
                    buyer_detail = text_data['text'].split('\r')
                    header_detail['requester'] = buyer_detail[1]
                    header_detail['requester_email'] = buyer_detail[2]
                if cell_count == 1:
                    supplier_contact = text_data['text'].split('\r')
                    header_detail['supplier_contact'] = supplier_contact[1]
                if cell_count == 2:
                    ordered_at = text_data['text'].split('\r')
                    header_detail['ordered_at'] = ordered_at[1]
            if row_count == 1:
                if cell_count == 0:
                    requester_mobile_num = text_data['text'].split('\r')
                    header_detail['requester_mobile_num'] = requester_mobile_num[1]
                if cell_count == 2:
                    supplier_mobile_num = text_data['text'].split('\r')
                    header_detail['supplier_mobile_num'] = supplier_mobile_num[1]
                if cell_count == 3:
                    supplier_email = text_data['text'].split('\r')
                    header_detail['supplier_email'] = supplier_email[1]

    print("header details: ", header_detail)
    return header_detail


def save_po_data(header_detail, po_item_details, address):
    """

    """
    print("po header", header_detail)
    print("po item", po_item_details)
    print("po addr", address)
    save_som_po_instance = SaveSOMPO()
    save_som_po_instance.save_som_po_header(header_detail)
    save_som_po_instance.save_som_po_items(po_item_details)
    save_som_po_instance.save_som_po_address(address)

    return header_detail


class SaveSOMPO:
    def __init__(self):
        self.som_po_header_guid = guid_generator()
        self.som_po_header_instance = ''
        self.requester = ''
        self.som_po_item_instance = ''

    def save_som_po_header(self, header_detail):
        """

        """
        self.requester = header_detail['goods_recep']
        header_detail['som_po_header_guid'] = self.som_po_header_guid
        header_detail['ordered_at'] = datetime.datetime.strptime(header_detail['ordered_at'], '%m-%d-%Y')
        header_detail['posting_date'] = header_detail['ordered_at']
        header_detail['status'] = 'ORDERED'
        header_detail['time_zone'] = ''
        if not checkKey(header_detail, 'supplier_note_text'):
            header_detail['supplier_note_text'] = ''
        header_detail['som_po_header_created_at'] = datetime.datetime.now()
        header_detail['som_po_header_created_by'] = global_variables.GLOBAL_LOGIN_USERNAME
        header_detail['som_po_header_changed_at'] = datetime.datetime.now()
        header_detail['som_po_header_changed_by'] = global_variables.GLOBAL_LOGIN_USERNAME
        header_detail['client'] = global_variables.GLOBAL_CLIENT
        django_query_instance.django_create_query(SOMPoHeader,
                                                  header_detail)

    def save_som_po_items(self, po_item_details):
        """

        """
        som_po_item_list = []
        self.som_po_header_instance = django_query_instance.django_get_query(SOMPoHeader,
                                                                             {
                                                                                 'som_po_header_guid': self.som_po_header_guid})
        for po_item_detail in po_item_details:
            som_po_item_guid = guid_generator()
            som_po_item = {'som_po_item_guid': som_po_item_guid,
                           'som_po_header_guid': self.som_po_header_instance,
                           'som_po_item_num': po_item_detail[0], 'int_product_id': po_item_detail[1],
                           'description': po_item_detail[2], 'quantity': int(round(float(po_item_detail[3])))}
            unit = po_item_detail[4].split('(')[1]
            som_po_item['unit'] = unit.split(')')[0]
            som_po_item['price'] = round(float(po_item_detail[5]), 2)
            som_po_item['item_del_date'] = datetime.datetime.strptime(po_item_detail[6], '%m-%d-%Y')
            som_po_item['value'] = float(po_item_detail[7].split(' ')[0])
            som_po_item['price_unit'] = '1'
            som_po_item['currency'] = po_item_detail[7].split(' ')[1]
            som_po_item['goods_recep'] = self.requester
            som_po_item['client'] = global_variables.GLOBAL_CLIENT
            som_po_item['som_po_item_created_at'] = datetime.datetime.now()
            som_po_item['som_po_item_created_by'] = global_variables.GLOBAL_LOGIN_USERNAME
            som_po_item['som_po_item_changed_at'] = datetime.datetime.now()
            som_po_item['som_po_item_changed_by'] = global_variables.GLOBAL_LOGIN_USERNAME
            django_query_instance.django_create_query(SOMPoItem,
                                                      som_po_item)
            self.som_po_item_instance = django_query_instance.django_get_query(SOMPoItem,
                                                                               {'som_po_item_guid': som_po_item_guid,
                                                                                'del_ind': False,
                                                                                'client': global_variables.GLOBAL_CLIENT})
            if len(po_item_detail) > 7:
                for po_additional_data in po_item_detail:
                    if po_additional_data.find("Additional comments on the line item") != -1:
                        additional_data = po_additional_data.split('ShortDescription:')
                        eform_data = additional_data[0]
                        eform_description = additional_data[1]
                        eform_list = eform_data.split('\r')
                        for count, eform in enumerate(eform_list):
                            if eform.find("Additional comments on the line item") != -1:
                                del eform_list[count]

                        eform_id = self.save_eform_data(eform_list, eform_description)
                        django_query_instance.django_update_query(SOMPoItem,
                                                                  {'som_po_item_guid': som_po_item_guid,
                                                                   'del_ind': False,
                                                                   'client': global_variables.GLOBAL_CLIENT},
                                                                  {'eform_id': eform_id})
                    if po_additional_data.find("Cost Object") != -1:
                        acc_data = po_additional_data.split('\r')[1]
                        self.save_acc_detail(acc_data, po_item_detail[0])

    def save_acc_detail(self, acc_data, item_num):
        """

        """
        acc_details = acc_data.split(': ')
        acc_dictionary = {'som_po_accounting_guid': guid_generator(),
                          'som_po_accounting_created_at': datetime.datetime.now(),
                          'som_po_accounting_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                          'som_po_accounting_changed_at': datetime.datetime.now(),
                          'som_po_accounting_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                          'som_po_item_guid': self.som_po_item_instance,
                          'client': global_variables.GLOBAL_CLIENT,
                          'acc_item_num': item_num
                          }
        for count, acc_detail in enumerate(acc_details):
            if acc_detail.find("Generic Account") != -1:
                acc_dictionary['generic_acc_str'] = acc_details[count + 1].split(' ')[0]
            if acc_detail.find("Cost Center") != -1:
                acc_dictionary['acc_cat'] = CONST_CC
                acc_dictionary['cost_center'] = acc_details[count + 1].split(' ')[0]
            if acc_detail.find("GL Account") != -1:
                acc_dictionary['gl_acc_num'] = acc_details[count + 1].split(' ')[0]
        django_query_instance.django_create_query(SOMPoAccounting,
                                                  acc_dictionary)
        return acc_dictionary

    def save_eform_data(self, eform_data, eform_description):
        """

        """
        eform_id = random_int(8)
        eform_list = []
        for count, eform in enumerate(eform_data):
            if eform:
                eform_detail = eform.split(': ')
                eform_dictionary = {'som_eform_field_data_guid': guid_generator(),
                                    'eform_id': eform_id,
                                    'eform_field_name': eform_detail[0],
                                    'eform_field_data': eform_detail[1],
                                    'eform_field_count': count + 1,
                                    'eform_description': eform_description,
                                    'eform_field_data_created_at': datetime.datetime.now(),
                                    'som_eform_field_data_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                    'som_eform_field_data_changed_at': datetime.datetime.now(),
                                    'som_eform_field_data_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                    'client': global_variables.GLOBAL_CLIENT,
                                    'som_po_item_guid': self.som_po_item_instance}
                eform_list.append(eform_dictionary)
        bulk_create_entry_db(SOMEformFieldData, eform_list)
        return eform_id

    def save_som_po_address(self,address):
        """

        """
        for key, value in address.items():
            if key == 'supplier_address_detail':
                som_po_address_dic = {'som_po_addresses_guid':guid_generator(),
                                      'address_type':'S',
                                      }
