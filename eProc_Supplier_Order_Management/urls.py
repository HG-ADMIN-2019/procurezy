from django.urls import path
from eProc_Supplier_Order_Management.views.supplier_order_management_views import *

app_name = 'eProc_Supplier_Order_Management'
# Defining the mapping between URLs and views
urlpatterns = [
    path('po_extract', po_extract, name='po_extract'),
]