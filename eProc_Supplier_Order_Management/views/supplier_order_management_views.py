import datetime
import os

from django.shortcuts import render
from pypdf._reader import PdfReader
import tabula
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.functions.distinct_list import distinct_list
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Supplier_Order_Management.Utilities.supplier_order_management_specific import *


def po_extract(request):
    """

    """
    update_user_info(request)
    text = []
    header_detail = []
    supplier_address = []
    if request.POST:
        pdfData = ''
        reader = ''

        po_item_data = []
        directory = os.path.join(str(settings.BASE_DIR), 'media', 'pdf_read')
        for root, dirs, files in os.walk(directory):
            for file in files:
                additional_info = []
                cost_obj_data = []
                item_row_num = []
                file_path = os.path.join(directory, file)  # create path
                pdfData = tabula.read_pdf(file_path, pages="all", output_format="json")
                reader = PdfReader(file_path)
                # print(len(reader.pages))
                page = reader.pages[0]
                extract_text = page.extract_text()
                text = extract_text.splitlines()
                print(text)
                header_detail = {}
                header_detail, supplier_address = get_po_data(text, header_detail)
                get_po_table_data(pdfData[0], header_detail)
                data = pdfData[1]
                po_total_table = pdfData[2]['data']
                total_detail = po_total_table[0][1]['text'].split(' ')
                header_detail['total_value'] = total_detail[0]
                header_detail['currency'] = total_detail[1]
                item_num = 0
                po_item_data  = []
                for count, item_data in enumerate(data['data']):
                    if count != 0:
                        for text_data in item_data:
                            item_dictionary = {}
                            text_value = text_data['text']
                            if text_value:
                                if text_value.find("Additional comments on the line item") != -1:
                                    value = text_value.split('\r')
                                    print("additional info:", value)
                                    po_item_data.append({item_num: text_value})
                                    additional_info.append({'item_num': count + 1, 'data': value})
                                elif text_value.find("Cost Object") != -1:
                                    po_item_data.append({item_num: text_value})
                                    print("Cost Object:", text_value)
                                    cost_obj_data.append({'item_num': count + 1, 'data': text_value})
                                elif text_value.find("External Product ID") != -1:
                                    print("External Product ID:", text_value)
                                    po_item_data.append({item_num: text_value})
                                else:
                                    text_value = text_value.replace('\r', '')
                                    item_row_num.append(count)
                                    item_num = count
                                    po_item_data.append({count: text_value})
                                    print("item data:", text_value)
                item_row_num = distinct_list(item_row_num)
                po_item_details = []
                print("po_item_data:",po_item_data)
                for count, row_num in enumerate(item_row_num):
                    item_list = []
                    for item_data in po_item_data:
                        for key, value in item_data.items():
                            if key == row_num:
                                item_list.append(value)
                    po_item_details.append(item_list)
                save_po_data(header_detail, po_item_details, supplier_address)

        # data = {'pdf_data': pdfData}
    context = {'inc_nav': True,
               'inc_footer': True,
               'is_slide_menu': True,
               'text': text,
               'header_detail': header_detail,
               'supplier_address': supplier_address
               }
    return render(request, 'Supplier_Order_Management/som_po_data.html', context)
