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
        po_pdf_reader()


        # data = {'pdf_data': pdfData}
    context = {'inc_nav': True,
               'inc_footer': True,
               'is_slide_menu': True,
               'text': text,
               'header_detail': header_detail,
               'supplier_address': supplier_address
               }
    return render(request, 'Supplier_Order_Management/som_po_data.html', context)
