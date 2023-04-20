import os

from django.shortcuts import render
from pypdf._reader import PdfReader
import tabula
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.functions.string_related_functions import remove_space


def po_extract(request):
    """

    """
    if request.POST:
        pdfData = ''
        reader = ''

        directory = os.path.join(str(settings.BASE_DIR), 'media', 'pdf_read')
        for root, dirs, files in os.walk(directory):
            for file in files:
                additional_info = []
                cost_obj_data = []
                file_path = os.path.join(directory, file)  # create path
                pdfData = tabula.read_pdf(file_path, pages="all", output_format="json")
                reader = PdfReader(file_path)
                # print(len(reader.pages))
                page = reader.pages[0]
                extract_text = page.extract_text()
                text = extract_text.splitlines()
                print(text)
                header_detail = {}
                header_detail,supplier_address = get_po_data(text, header_detail)
                get_po_table_data(pdfData[0], header_detail)
                # pdf_file = open(file_path, 'rb')  # open .csv file
                # reader = PyPDF2.PdfFileReader(pdf_file)
                # page1 = reader.getPage(0)
                # print(reader.numPages)
                # pdfData = page1.extractText()
                # print(pdfData[1])
                data = pdfData[1]
                for count, item_data in enumerate(data['data']):
                    if count != 0:
                        for text_data in item_data:
                            item_dictionary = {}
                            text_value = text_data['text']
                            if text_value:
                                if text_value.find("Additional comments on the line item") != -1:
                                    value = text_value.split('\r')
                                    print("additional info:", value)
                                    additional_info.append({'item_num':count+1,'data':value})
                                elif text_value.find("Cost Object") != -1:
                                    print("Cost Object:", text_value)
                                    cost_obj_data.append({'item_num':count+1,'data':text_value})
                                elif text_value.find("External Product ID") != -1:
                                    print("External Product ID:", text_value)
                                    item_data.append({'ext':text_value})
                                else:
                                    text_value = text_value.replace('\r', '')
                                    item_data.append({count:text_value})
                                    print("item data:", item_data)

        # data = {'pdf_data': pdfData}
    context = {'inc_nav': True,
               'inc_footer': True,
               'is_slide_menu': True}
    return render(request, 'Supplier_Order_Management/po_extract.html', context)


def get_po_data(text, header_detail):
    """

    """
    supplier_address = {'address_details': '', 'invoice_address': '', 'delivery_address': ''}
    header_detail['invoicing_detail'] = ''
    index = 0
    flag = False
    buyer_flag = False
    invoice_address = False
    pdf_invoice_address_flag = False
    delivery_address_flag = False
    incoterm_flag = False
    payment_term_flag = False
    invoicing_detail_flag = False
    goods_recep_flag = False
    supplier_note_text_flag = False
    for count, po_data in enumerate(text):
        if po_data.find("PURCHASE ORDER NO") != -1:
            header_detail['doc_num'] = remove_space(po_data.split(':')[1])
        if flag:
            if not po_data.find("Buyer") != -1:
                supplier_address['address_details'] = supplier_address['address_details'] + ' ' + po_data
            else:
                if po_data.find("Buyer") != -1:
                    data = po_data.split('Buyer')
                    supplier_address['address_details'] = supplier_address['address_details'] + ' ' + data[0]
                    buyer_flag = True
                    flag = False
        if po_data == "Vendor":
            flag = True
        if incoterm_flag:
            header_detail['incoterm'] = po_data.split('Terms of Payment')[0]
            payment_term_flag = True
            incoterm_flag = False
        if po_data == 'Terms of Delivery (In accordance with INCOTERMS 2010)':
            incoterm_flag = True
            delivery_address_flag = False
        if delivery_address_flag:
            supplier_address['delivery_address'] = supplier_address['delivery_address'] + ' ' + po_data
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
                header_detail['invoicing_detail'] = header_detail['invoicing_detail'] + ' ' + po_data.split('Goods Marking')[0]
                invoicing_detail_flag = False
        if po_data == 'Invoicing':
            invoicing_detail_flag = True
            payment_term_flag = False
        if payment_term_flag:
            header_detail['payment_term'] = po_data

        if pdf_invoice_address_flag:
            header_detail['pdf_invoice_address'] = po_data.split('Delivery Address')[0]
            delivery_address_flag = True
            pdf_invoice_address_flag = False
        if po_data == 'PDF Invoice Address':
            invoice_address = False
            pdf_invoice_address_flag = True
            delivery_address_flag = False
        if po_data == 'Invoice Address':
            invoice_address = True
        if invoice_address:
            supplier_address['invoice_address'] = supplier_address['invoice_address'] + ' ' + po_data

    return header_detail,supplier_address


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
