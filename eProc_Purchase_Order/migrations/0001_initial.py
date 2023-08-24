# Generated by Django 3.1.7 on 2023-08-24 13:07

from django.db import migrations, models
import django.db.models.deletion
import eProc_Shopping_Cart.models.shopping_cart


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eProc_Configuration', '0002_auto_20230824_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoAccounting',
            fields=[
                ('po_accounting_guid', models.CharField(db_column='PO_ACCOUNTING_GUID', max_length=32, primary_key=True, serialize=False)),
                ('acc_item_num', models.DecimalField(db_column='ACC_ITEM_NUM', decimal_places=0, max_digits=4, null=True, verbose_name='Number')),
                ('acc_cat', models.CharField(db_column='ACC_CAT', max_length=5, null=True, verbose_name='Account Assignment Category')),
                ('dist_perc', models.CharField(blank=True, db_column='DIST_PERC', max_length=5, null=True, verbose_name='Distribution Percentage')),
                ('gl_acc_num', models.CharField(blank=True, db_column='GL_ACC_NUM', max_length=10, null=True, verbose_name='General Ledger Account')),
                ('cost_center', models.CharField(blank=True, db_column='COST_CENTER', max_length=10, null=True, verbose_name='Cost Center')),
                ('internal_order', models.CharField(blank=True, db_column='INTERNAL_ORDER', max_length=12, null=True, verbose_name='Internal Order')),
                ('generic_acc_str', models.CharField(blank=True, db_column='GENERIC_ACC_STR', max_length=64, null=True, verbose_name='Generic Acc Ass')),
                ('wbs_ele', models.CharField(blank=True, db_column='WBS_ELE', max_length=24, null=True, verbose_name='WBS Element')),
                ('project', models.CharField(blank=True, db_column='PROJECT', max_length=24, null=True, verbose_name='Project')),
                ('task_id', models.CharField(blank=True, db_column='TASK_ID', max_length=25, null=True, verbose_name='Task Id')),
                ('network', models.CharField(blank=True, db_column='NETWORK', max_length=12, null=True, verbose_name='Network')),
                ('ref_date', models.DateField(db_column='REF_DATE', null=True, verbose_name='Ref Date')),
                ('dist_qty', models.PositiveIntegerField(db_column='DIST_QTY', null=True)),
                ('dist_val', models.PositiveIntegerField(db_column='DIST_VAL', null=True)),
                ('dist_ind', models.BooleanField(db_column='DIST_IND', default=False)),
                ('custom1', models.CharField(db_column='CUSTOM1', max_length=12, null=True)),
                ('custom2', models.CharField(db_column='CUSTOM2', max_length=12, null=True)),
                ('custom3', models.CharField(db_column='CUSTOM3', max_length=12, null=True)),
                ('custom4', models.CharField(db_column='CUSTOM4', max_length=12, null=True)),
                ('asset_number', models.CharField(db_column='ASSET_NUMBER', max_length=24, null=True)),
                ('gl_acc_origin', models.CharField(blank=True, db_column='GL_ACC_ORIGIN', max_length=1, null=True, verbose_name='Original Account (determination/manual entry)')),
                ('asset_sub_no', models.CharField(blank=True, db_column='ASSET_SUB_NO', max_length=4, null=True, verbose_name='Asset Subnumber')),
                ('order_no', models.CharField(blank=True, db_column='ORDER_NO', max_length=12, null=True, verbose_name='Controlling Area')),
                ('prof_segm', models.CharField(blank=True, db_column='PROF_SEGM', max_length=10, null=True, verbose_name='Profit Center')),
                ('part_acct', models.CharField(blank=True, db_column='PART_ACCT', max_length=10, null=True, verbose_name='Partner account number')),
                ('fund', models.CharField(blank=True, db_column='FUND', max_length=10, null=True, verbose_name='Functional Area')),
                ('budget_period', models.CharField(blank=True, db_column='BUDGET_PERIOD', max_length=10, null=True, verbose_name='Budget Period')),
                ('po_accounting_created_at', models.DateTimeField(db_column='PO_ACCOUNTING_CREATED_AT', null=True)),
                ('po_accounting_created_by', models.CharField(db_column='PO_ACCOUNTING_CREATED_BY', max_length=12, null=True)),
                ('po_accounting_changed_at', models.DateTimeField(blank=True, db_column='PO_ACCOUNTING_CHANGED_AT', null=True)),
                ('po_accounting_changed_by', models.CharField(db_column='PO_ACCOUNTING_CHANGED_BY', max_length=12, null=True)),
                ('po_accounting_source_system', models.CharField(db_column='PO_ACCOUNTING_SOURCE_SYSTEM', max_length=20)),
                ('po_accounting_destination_system', models.CharField(db_column='PO_ACCOUNTING_DESTINATION_SYSTEM', max_length=20, null=True)),
                ('del_ind', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'MTD_PO_ACCOUNTING',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PoAddresses',
            fields=[
                ('po_addresses_guid', models.CharField(db_column='PO_ADDRESSES_GUID', max_length=32, primary_key=True, serialize=False)),
                ('item_num', models.PositiveIntegerField(db_column='ITEM_NUM', default=0, verbose_name='Item Number')),
                ('address_number', models.PositiveIntegerField(db_column='ADDRESS_NUMBER', null=True)),
                ('address_type', models.CharField(blank=True, db_column='ADDRESS_TYPE', max_length=1, null=True)),
                ('title', models.CharField(db_column='TITLE', max_length=40, null=True)),
                ('name1', models.CharField(db_column='NAME1', max_length=40, null=True, verbose_name='First Name')),
                ('name2', models.CharField(db_column='NAME2', max_length=40, null=True, verbose_name='Last Name')),
                ('street', models.CharField(db_column='STREET', max_length=100, verbose_name='Street')),
                ('area', models.CharField(db_column='AREA', max_length=100, verbose_name='Area')),
                ('landmark', models.CharField(db_column='LANDMARK', max_length=50, verbose_name='Landmark')),
                ('city', models.CharField(db_column='CITY', max_length=20, verbose_name='City')),
                ('postal_code', models.CharField(db_column='POSTAL_CODE', max_length=10, verbose_name='Postal Code')),
                ('region', models.CharField(db_column='REGION', max_length=30, verbose_name='Region')),
                ('country_code', models.CharField(db_column='COUNTRY_CODE', max_length=2, null=True, verbose_name='Country')),
                ('language_id', models.CharField(db_column='LANGUAGE_ID', max_length=2, null=True, verbose_name='Language')),
                ('mobile_number', models.CharField(blank=True, db_column='MOBILE_NUMBER', max_length=20, null=True, verbose_name='Mobile')),
                ('telephone_number', models.CharField(blank=True, db_column='TELEPHONE_NUMBER', max_length=20, null=True, verbose_name='Telephone')),
                ('fax_number', models.CharField(db_column='FAX_NUMBER', max_length=30, null=True, verbose_name='Fax')),
                ('email', models.EmailField(db_column='EMAIL', max_length=100, null=True)),
                ('time_zone', models.CharField(db_column='TIME_ZONE', max_length=6, null=True)),
                ('po_addr_created_at', models.DateTimeField(db_column='PO_ADDR_CREATED_AT', null=True)),
                ('po_addr_created_by', models.CharField(db_column='PO_ADDR_CREATED_BY', max_length=12, null=True)),
                ('po_addr_changed_at', models.DateTimeField(blank=True, db_column='PO_ADDR_CHANGED_AT', null=True)),
                ('po_addr_changed_by', models.CharField(db_column='PO_ADDR_CHANGED_BY', max_length=12, null=True)),
                ('po_addresses_source_system', models.CharField(db_column='PO_ADDRESSES_SOURCE_SYSTEM', max_length=20)),
                ('po_addresses_destination_system', models.CharField(db_column='PO_ADDRESSES_DESTINATION_SYSTEM', max_length=20)),
                ('del_ind', models.BooleanField(default=False, null=True)),
            ],
            options={
                'db_table': 'MTD_PO_ADDRESSES',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PoApproval',
            fields=[
                ('po_approval_guid', models.CharField(db_column='PO_APPROVAL_GUID', max_length=32, primary_key=True, serialize=False)),
                ('step_num', models.CharField(blank=True, db_column='STEP_NUM', max_length=3, null=True, verbose_name='Sequence')),
                ('app_desc', models.CharField(blank=True, db_column='APP_DESC', max_length=60, null=True, verbose_name='Agent Determination')),
                ('proc_lvl_sts', models.CharField(blank=True, db_column='PROC_LVL_STS', max_length=10, null=True, verbose_name='Level Status')),
                ('app_sts', models.CharField(blank=True, db_column='APP_STS', max_length=20, null=True, verbose_name='Status')),
                ('app_id', models.CharField(blank=True, db_column='APP_ID', max_length=70, null=True, verbose_name='Processor')),
                ('received_time', models.DateTimeField(blank=True, db_column='RECEIVED_TIME', null=True, verbose_name='Received On')),
                ('proc_time', models.DateTimeField(blank=True, db_column='PROC_TIME', null=True, verbose_name='Processed On')),
                ('time_zone', models.CharField(blank=True, db_column='TIME_ZONE', max_length=6, null=True, verbose_name='Time Zone')),
                ('app_types', models.CharField(db_column='APP_TYPES', max_length=30, null=True)),
                ('multiple_approver_flag', models.BooleanField(db_column='MULTIPLE_APPROVER_FLAG', default=False, null=True, verbose_name='Multiple Approver flag')),
                ('po_approval_created_at', models.DateTimeField(db_column='PO_APPROVAL_CREATED_AT', null=True)),
                ('po_approval_created_by', models.CharField(db_column='PO_APPROVAL_CREATED_BY', max_length=12, null=True)),
                ('po_approval_changed_at', models.DateTimeField(blank=True, db_column='PO_APPROVAL_CHANGED_AT', null=True)),
                ('po_approval_changed_by', models.CharField(db_column='PO_APPROVAL_CHANGED_BY', max_length=12, null=True)),
                ('del_ind', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'MTD_PO_APPROVAL',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PoHeader',
            fields=[
                ('po_header_guid', models.CharField(db_column='PO_HEADER_GUID', max_length=32, primary_key=True, serialize=False)),
                ('doc_number', models.CharField(db_column='DOC_NUMBER', max_length=10, verbose_name='PO Number')),
                ('transaction_type', models.CharField(db_column='TRANSACTION_TYPE', max_length=10)),
                ('posting_date', models.DateTimeField(blank=True, db_column='POSTING_DATE', null=True)),
                ('version_type', models.CharField(blank=True, db_column='VERSION_TYPE', max_length=1, null=True, verbose_name='Version type')),
                ('version_num', models.CharField(blank=True, db_column='VERSION_NUM', max_length=8, verbose_name='Version number')),
                ('description', models.CharField(blank=True, db_column='DESCRIPTION', max_length=255, verbose_name='PO NAME')),
                ('language_id', models.CharField(blank=True, db_column='LANGUAGE_ID', max_length=2, null=True)),
                ('gross_amount', models.CharField(blank=True, db_column='GROSS_AMOUNT', max_length=15, null=True, verbose_name='Gross Amount')),
                ('total_tax', models.CharField(blank=True, db_column='TOTAL_TAX', max_length=15, null=True, verbose_name='Total Tax')),
                ('total_value', models.CharField(db_column='TOTAL_VALUE', max_length=15, verbose_name='Total Value')),
                ('total_value_appr', models.CharField(blank=True, db_column='TOTAL_VALUE_APPR', max_length=15, null=True, verbose_name='Total Value Appr')),
                ('usr_budget_value', models.CharField(blank=True, db_column='USR_BUDGET_VALUE', max_length=15, null=True, verbose_name='User Budget Value')),
                ('currency', models.CharField(db_column='CURRENCY', max_length=3, verbose_name='Currency')),
                ('payment_term', models.CharField(blank=True, db_column='PAYMENT_TERM', max_length=4, null=True)),
                ('incoterm', models.CharField(blank=True, db_column='INCOTERM', max_length=3, null=True)),
                ('incoterm_loc', models.CharField(blank=True, db_column='INCOTERM_LOC', max_length=28, null=True, verbose_name='Incoterm location')),
                ('val_po_e', models.CharField(blank=True, db_column='VAL_PO_E', max_length=15, null=True, verbose_name='Value of POs/Confirmations/Invoices Created for Contract')),
                ('val_po_e_agg', models.CharField(blank=True, db_column='VAL_PO_E_AGG', max_length=15, null=True, verbose_name='Value of POs/Confirmations/Invoices Created for Contract')),
                ('requester', models.CharField(db_column='REQUESTER', max_length=12, verbose_name='Requester')),
                ('status', models.CharField(db_column='STATUS', max_length=20, verbose_name='Status')),
                ('gr_gi_slip_no', models.CharField(db_column='GR_GI_SLIP_NO', max_length=10, verbose_name='Status')),
                ('bill_of_lading', models.CharField(db_column='BILL_OF_LADING', max_length=16, verbose_name='Status')),
                ('posting_date_FI', models.DateTimeField(blank=True, db_column='POSTING_DATE_FI', null=True, verbose_name='Transaction Posting Date in Accounting\tPOSTING_DATE_FI')),
                ('ref_doc_no', models.CharField(blank=True, db_column='REF_DOC_NO', max_length=16, null=True, verbose_name='Ref Doc Number')),
                ('po_header_created_at', models.DateTimeField(db_column='PO_HEADER_CREATED_AT', verbose_name='Created At')),
                ('po_header_created_by', models.CharField(db_column='PO_HEADER_CREATED_BY', max_length=12, verbose_name='Creator')),
                ('po_header_changed_at', models.DateTimeField(blank=True, db_column='PO_HEADER_CHANGED_AT', verbose_name='Changed At')),
                ('po_header_changed_by', models.CharField(db_column='PO_HEADER_CHANGED_BY', max_length=12, verbose_name='Changed By')),
                ('document_type', models.CharField(db_column='DOCUMENT_TYPE', max_length=5, null=True)),
                ('silent_po', models.BooleanField(db_column='SILENT_PO', default=False)),
                ('ordered_at', models.DateTimeField(blank=True, db_column='ORDERED_AT', null=True, verbose_name='Ordered At')),
                ('time_zone', models.CharField(blank=True, db_column='TIME_ZONE', max_length=6, verbose_name='Time Zone')),
                ('company_code_id', models.CharField(db_column='COMPANY_CODE_ID', max_length=20)),
                ('inv_addr_num', models.PositiveIntegerField(blank=True, db_column='INV_ADDR_NUM', null=True, verbose_name='Invoice address number')),
                ('ship_addr_num', models.PositiveIntegerField(blank=True, db_column='SHIP_ADDR_NUM', null=True, verbose_name='Ship to Address Number')),
                ('supplier_id', models.CharField(blank=True, db_column='SUPPLIER_ID', max_length=12, null=True, verbose_name='Supplier ID')),
                ('supplier_username', models.CharField(blank=True, db_column='SUPPLIER_USERNAME', max_length=40, null=True)),
                ('supplier_mobile_num', models.CharField(blank=True, db_column='SUPPLIER_MOBILE_NUM', max_length=40, null=True)),
                ('supplier_fax_no', models.CharField(blank=True, db_column='SUPPLIER_FAX_NO', max_length=30, null=True)),
                ('supplier_email', models.CharField(blank=True, db_column='SUPPLIER_EMAIL', max_length=100, null=True)),
                ('pref_supplier', models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True, verbose_name='preferred supplier ')),
                ('supp_type', models.CharField(blank=True, db_column='SUPP_TYPE', max_length=35, null=True, verbose_name='Supplier Type')),
                ('delivery_days', models.CharField(blank=True, db_column='DELIVERY_DAYS', max_length=20, null=True)),
                ('blocked_supplier', models.BooleanField(db_column='BLOCKED_SUPPLIER', default=False)),
                ('po_pdf_creation_flag', models.BooleanField(db_column='PO_PDF_CREATION_FLAG', default=False)),
                ('po_pdf_email_flag', models.BooleanField(db_column='PO_PDF_EMAIL_FLAG', default=False)),
                ('tax_code', models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')),
                ('sgst', models.PositiveIntegerField(blank=True, db_column='SGST', null=True, verbose_name='State GST')),
                ('cgst', models.PositiveIntegerField(blank=True, db_column='CGST', null=True, verbose_name='Central GST')),
                ('vat', models.PositiveIntegerField(blank=True, db_column='VAT', null=True, verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')),
                ('po_header_source_system', models.CharField(db_column='PO_HEADER_SOURCE_SYSTEM', max_length=20)),
                ('pd_header_destination_system', models.CharField(db_column='PO_HEADER_DESTINATION_SYSTEM', max_length=20)),
                ('del_ind', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'MTD_PO_HEADER',
                'managed': True,
            },
            bases=(models.Model, eProc_Shopping_Cart.models.shopping_cart.DBQueries),
        ),
        migrations.CreateModel(
            name='PoPotentialApproval',
            fields=[
                ('po_potential_approval_guid', models.CharField(db_column='po_potential_approval_guid', max_length=32, primary_key=True, serialize=False)),
                ('app_id', models.CharField(blank=True, db_column='APP_ID', max_length=70, null=True, verbose_name='Approver ID')),
                ('step_num', models.CharField(blank=True, db_column='STEP_NUM', max_length=3, null=True, verbose_name='Sequence')),
                ('app_sts', models.CharField(blank=True, db_column='APP_STS', max_length=20, null=True, verbose_name='Status')),
                ('proc_lvl_sts', models.CharField(blank=True, db_column='PROC_LVL_STS', max_length=10, null=True, verbose_name='Level Status')),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
                ('po_approval_guid', models.ForeignKey(blank=True, db_column='PO_APPROVAL_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poapproval')),
                ('po_header_guid', models.ForeignKey(db_column='PO_HEADER_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poheader')),
            ],
            options={
                'db_table': 'MTD_PO_POTENTIAL_APPROVAL',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PoItem',
            fields=[
                ('po_item_guid', models.CharField(db_column='PO_ITEM_GUID', max_length=32, primary_key=True, serialize=False)),
                ('po_item_num', models.CharField(blank=True, db_column='PO_ITEM_NUM', max_length=10, null=True, verbose_name='Line Number')),
                ('sc_doc_num', models.CharField(blank=True, db_column='SC_DOC_NUM', max_length=10, null=True, verbose_name='SC Number')),
                ('rfq_doc_num', models.CharField(blank=True, db_column='RFQ_DOC_NUM', max_length=10, null=True, verbose_name='SC Number')),
                ('sc_item_num', models.PositiveIntegerField(db_column='SC_ITEM_NUM', verbose_name='Line Number')),
                ('rfq_item_num', models.PositiveIntegerField(blank=True, db_column='RFQ_ITEM_NUM', null=True, verbose_name='Line Number')),
                ('document_type', models.CharField(blank=True, db_column='DOCUMENT_TYPE', max_length=10, null=True)),
                ('int_product_id', models.CharField(db_column='INT_PRODUCT_ID', max_length=20, null=True)),
                ('supp_product_id', models.PositiveIntegerField(blank=True, db_column='SUPP_PRODUCT_ID', null=True)),
                ('description', models.CharField(blank=True, db_column='DESCRIPTION', max_length=255, null=True)),
                ('long_desc', models.CharField(blank=True, db_column='LONG_DESC', max_length=3000, null=True, verbose_name='Product Long desc')),
                ('stock_keeping_unit', models.CharField(blank=True, db_column='STOCK_KEEPING_UNIT', max_length=32, null=True)),
                ('univeral_product_code', models.CharField(blank=True, db_column='UNIVERAL_PRODUCT_CODE', max_length=32, null=True)),
                ('barcode', models.CharField(blank=True, db_column='BARCODE', max_length=20, null=True)),
                ('itm_language_id', models.CharField(blank=True, db_column='ITM_LANGUAGE_ID', max_length=2, null=True, verbose_name=' Short Text Language for an Item ')),
                ('order_date', models.DateTimeField(blank=True, db_column='ORDER_DATE', null=True)),
                ('grp_ind', models.BooleanField(db_column='GRP_IND', default=False, null=True, verbose_name='Grouping logic for different product categories in purchaser cockpit')),
                ('company_code_id', models.CharField(db_column='COMPANY_CODE_ID', max_length=20)),
                ('del_datcat', models.CharField(blank=True, db_column='DEL_DATCAT', max_length=2, null=True, verbose_name='Date type (day, week, month, interval)')),
                ('item_del_date', models.DateTimeField(db_column='ITEM_DEL_DATE', null=True, verbose_name='Delivery Date')),
                ('prod_cat_id', models.CharField(db_column='PROD_CAT_ID', max_length=20, verbose_name='UnspscCategories')),
                ('prod_cat_desc', models.CharField(blank=True, db_column='PROD_CAT_DESC', max_length=255, null=True, verbose_name='Description')),
                ('cust_prod_cat_id', models.CharField(db_column='CUST_PROD_CAT_ID', max_length=20, null=True, verbose_name='UnspscCategoriesCust')),
                ('lead_time', models.PositiveIntegerField(blank=True, db_column='LEAD_TIME', null=True, verbose_name='Lead time')),
                ('final_inv', models.BooleanField(blank=True, db_column='FINAL_INV', default=False, null=True)),
                ('final_entry_ind', models.BooleanField(blank=True, db_column='FINAL_ENTRY_IND', default=False, null=True)),
                ('overall_limit', models.DecimalField(blank=True, db_column='OVERALL_LIMIT', decimal_places=2, max_digits=15, null=True, verbose_name='overall limit')),
                ('expected_value', models.DecimalField(blank=True, db_column='EXPECTED_VALUE', decimal_places=2, max_digits=15, null=True, verbose_name='expected value')),
                ('start_date', models.DateTimeField(db_column='START_DATE', null=True, verbose_name='Start Date')),
                ('end_date', models.DateTimeField(db_column='END_DATE', null=True, verbose_name='End date')),
                ('required_on', models.DateField(blank=True, db_column='REQUIRED_ON', null=True)),
                ('undef_limit', models.BooleanField(blank=True, db_column='UNDEF_LIMIT', default=False, null=True)),
                ('ir_gr_ind_limi', models.BooleanField(db_column='IR_GR_IND_LIMI', default=False, null=True, verbose_name='Gr ind for LO')),
                ('gr_ind_limi', models.BooleanField(db_column='GR_IND_LIMI', default=False, null=True, verbose_name='Gr ind for LO')),
                ('val_cf_e', models.DecimalField(blank=True, db_column='VAL_CF_E', decimal_places=2, max_digits=15, null=True, verbose_name='Value of Entered Confirmations')),
                ('val_cf', models.DecimalField(blank=True, db_column='VAL_CF', decimal_places=2, max_digits=15, null=True, verbose_name=' Value of Confirmations Released')),
                ('val_iv_e', models.DecimalField(blank=True, db_column='VAL_IV_E', decimal_places=2, max_digits=15, null=True)),
                ('val_iv', models.DecimalField(blank=True, db_column='VAL_IV', decimal_places=2, max_digits=15, null=True)),
                ('val_po_e', models.DecimalField(blank=True, db_column='VAL_PO_E', decimal_places=2, max_digits=15, null=True)),
                ('val_po_e_agg', models.DecimalField(blank=True, db_column='VAL_PO_E_AGG', decimal_places=2, max_digits=15, null=True)),
                ('quan_cf_e', models.PositiveIntegerField(blank=True, db_column='QUAN_CF_E', null=True, verbose_name='Quantity of Entered Confirmation')),
                ('quan_cf', models.PositiveIntegerField(blank=True, db_column='QUAN_CF', null=True, verbose_name='Quantity of Released Confirmations')),
                ('quan_po_e', models.PositiveIntegerField(blank=True, db_column='QUAN_PO_E', null=True)),
                ('num_cf', models.PositiveIntegerField(blank=True, db_column='NUM_CF', null=True, verbose_name='Number of Entered Confirmations for a Purchase Order')),
                ('source_relevant_ind', models.BooleanField(db_column='SOURCE_RELEVANT_IND', default=False, null=True, verbose_name='Indicator - If the Document is Sourcing-Relevant ')),
                ('ext_demid', models.CharField(blank=True, db_column='EXT_DEMID', max_length=2, null=True, verbose_name='External Requirement Number')),
                ('ext_dem_posid', models.CharField(blank=True, db_column='EXT_DEM_POSID', max_length=2, null=True, verbose_name='External Requirement Tracking Number')),
                ('offcatalog', models.BooleanField(blank=True, db_column='OFFCATALOG', default=False, null=True, verbose_name='Off Catalog Flag(false=Not from catalog)')),
                ('process_flow', models.CharField(blank=True, db_column='PROCESS_FLOW', max_length=20, null=True, verbose_name='Item Category')),
                ('quantity_min', models.PositiveIntegerField(db_column='QUANTITY_MIN', null=True, verbose_name='Quantity Min')),
                ('quantity_max', models.PositiveIntegerField(db_column='QUANTITY_MAX', null=True, verbose_name='Quantity Max')),
                ('tiered_flag', models.BooleanField(blank=True, db_column='TIERED_FLAG', default=False, null=True)),
                ('bundle_flag', models.BooleanField(blank=True, db_column='BUNDLE_FLAG', default=False, null=True)),
                ('material_no', models.CharField(blank=True, db_column='MATERIAL_NO', max_length=18, null=True)),
                ('sgst', models.DecimalField(blank=True, db_column='SGST', decimal_places=2, max_digits=15, null=True, verbose_name='State GST')),
                ('cgst', models.DecimalField(blank=True, db_column='CGST', decimal_places=2, max_digits=15, null=True, verbose_name='Central GST')),
                ('vat', models.DecimalField(blank=True, db_column='VAT', decimal_places=2, max_digits=15, null=True, verbose_name='Value Added Tax - VAT code (%age as decimal) returned from catalogue ')),
                ('prod_type', models.CharField(blank=True, db_column='PROD_TYPE', max_length=2, verbose_name='Product Type')),
                ('catalog_id', models.CharField(blank=True, db_column='CATALOG_ID', max_length=20, null=True, verbose_name='Catalog ID')),
                ('catalog_name', models.CharField(blank=True, db_column='CATALOG_NAME', max_length=40, null=True)),
                ('fin_entry_ind', models.CharField(blank=True, db_column='FIN_ENTRY_IND', max_length=1, null=True, verbose_name='Fin entry ind')),
                ('price_origin', models.CharField(blank=True, db_column='PRICE_ORIGIN', max_length=1, null=True)),
                ('quantity', models.PositiveIntegerField(db_column='QUANTITY', verbose_name='Quantity')),
                ('base_price', models.DecimalField(blank=True, db_column='BASE_PRICE', decimal_places=2, max_digits=15, null=True, verbose_name='base price of the item')),
                ('additional_price', models.DecimalField(blank=True, db_column='ADDITIONAL_PRICE', decimal_places=2, max_digits=15, null=True, verbose_name='additionalprice of the item')),
                ('actual_price', models.DecimalField(blank=True, db_column='ACTUAL_PRICE', decimal_places=2, max_digits=15, null=True, verbose_name='Price without discount')),
                ('discount_percentage', models.DecimalField(blank=True, db_column='DISCOUNT_PERCENTAGE', decimal_places=2, max_digits=15, null=True, verbose_name='Discount percentage')),
                ('discount_value', models.DecimalField(blank=True, db_column='DISCOUNT_VALUE', decimal_places=2, max_digits=15, null=True, verbose_name='Discount value')),
                ('price', models.DecimalField(blank=True, db_column='PRICE', decimal_places=2, max_digits=15, null=True, verbose_name='Price')),
                ('tax_value', models.DecimalField(blank=True, db_column='TAX_VALUE', decimal_places=2, max_digits=15, null=True, verbose_name='tax Value')),
                ('price_unit', models.CharField(blank=True, db_column='PRICE_UNIT', max_length=5, null=True, verbose_name='Price Unit')),
                ('unit', models.CharField(db_column='UNIT', max_length=3, verbose_name='Unit')),
                ('gross_price', models.DecimalField(db_column='GROSS_PRICE', decimal_places=2, max_digits=15, verbose_name='Gross Price')),
                ('value', models.DecimalField(blank=True, db_column='VALUE', decimal_places=2, max_digits=15, null=True, verbose_name='Value')),
                ('value_min', models.DecimalField(blank=True, db_column='VALUE_MIN', decimal_places=2, max_digits=15, null=True, verbose_name='Value')),
                ('currency', models.CharField(db_column='CURRENCY', max_length=3, verbose_name='Currency')),
                ('tax_code', models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')),
                ('gr_ind', models.CharField(blank=True, db_column='GR_IND', max_length=1, null=True, verbose_name='Gr ind')),
                ('ir_gr_ind', models.BooleanField(db_column='IR_GR_IND', default=False, null=True)),
                ('ir_ind', models.BooleanField(db_column='IR_IND', default=False, null=True)),
                ('po_resp', models.BooleanField(db_column='PO_RESP', default=False, null=True, verbose_name='PO Response')),
                ('asn_ind', models.BooleanField(db_column='ASN_IND', default=False, null=True, verbose_name='Advance shipment Notice')),
                ('eform_id', models.CharField(db_column='EFORM_ID', max_length=40, null=True)),
                ('discount_id', models.CharField(db_column='DISCOUNT_ID', max_length=40, null=True)),
                ('variant_id', models.CharField(db_column='VARIANT_ID', max_length=40, null=True)),
                ('product_info_id', models.CharField(blank=True, db_column='PRODUCT_INFO_ID', max_length=40, null=True)),
                ('dis_rej_ind', models.BooleanField(blank=True, db_column='DIS_REJ_IND', default=False, null=True)),
                ('goods_marking', models.CharField(blank=True, db_column='GOODS_MARKING', max_length=60, null=True)),
                ('confirmed_qty', models.PositiveIntegerField(blank=True, db_column='CONFIRMED_QTY', null=True, verbose_name='Qunatity to be updated upon creation of confirmation')),
                ('ctr_name', models.CharField(blank=True, db_column='CTR_NAME', max_length=50, null=True, verbose_name='Contract Name')),
                ('ctr_num', models.CharField(blank=True, db_column='CTR_NUM', max_length=50, null=True, verbose_name='ctr num')),
                ('ctr_item_num', models.CharField(blank=True, db_column='CTR_ITEM_NUM', max_length=50, null=True, verbose_name='ctr num')),
                ('pref_supplier', models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True, verbose_name='preferred supplier ')),
                ('approved_by', models.CharField(blank=True, db_column='APPROVED_BY', max_length=16, null=True)),
                ('call_off', models.CharField(db_column='CALL_OFF', max_length=20, null=True)),
                ('manu_part_num', models.CharField(blank=True, db_column='MANU_PART_NUM', max_length=40, null=True, verbose_name='manu part num')),
                ('manu_code_num', models.CharField(blank=True, db_column='MANU_CODE_NUM', max_length=10, null=True, verbose_name='manu code num')),
                ('ship_from_addr_num', models.CharField(blank=True, db_column='SHIP_from_ADDR_NUM', max_length=10, null=True, verbose_name='ship from addr num')),
                ('status', models.CharField(blank=True, db_column='STATUS', max_length=20, null=True, verbose_name='Status')),
                ('bill_to_addr_num', models.CharField(blank=True, db_column='BILL_TO_ADDR_NUM', max_length=10, null=True, verbose_name='bill to addr num')),
                ('ship_to_addr_num', models.CharField(blank=True, db_column='SHIP_TO_ADDR_NUM', max_length=10, null=True, verbose_name='ship to addr num')),
                ('cash_disc1', models.PositiveIntegerField(blank=True, db_column='CASH_DISC1', null=True, verbose_name='Discount % value to be filled (from eform table - qty based discount)')),
                ('cash_disc2', models.PositiveIntegerField(blank=True, db_column='CASH_DISC2', null=True, verbose_name='Discount % value to be filled (from eform table - qty based discount)')),
                ('goods_recep', models.CharField(blank=True, db_column='GOODS_RECEP', max_length=12, null=True, verbose_name='Goods Recipient')),
                ('manufacturer', models.CharField(blank=True, db_column='MANUFACTURER', max_length=50, null=True, verbose_name='Manufacturer')),
                ('delivery_days', models.CharField(blank=True, db_column='DELIVERY_DAYS', max_length=20, null=True)),
                ('supplier_note_existence_flag', models.BooleanField(blank=True, db_column='SUPPLIER_NOTE_EXISTENCE_FLAG', default=False, null=True, verbose_name='Supplier note existence flag')),
                ('internal_note_existence_flag', models.BooleanField(blank=True, db_column='INTERNAL_NOTE_EXISTENCE_FLAG', default=False, null=True, verbose_name='Internal note existence flag')),
                ('attachment_existence_flag', models.BooleanField(blank=True, db_column='ATTACHMENT_EXISTENCE_FLAG', default=False, null=True, verbose_name='Attachment existence flag')),
                ('accounting_change_flag', models.BooleanField(blank=True, db_column='ACCOUNTING_CHANGE_FLAG', default=False, null=True, verbose_name='Accounting change flag')),
                ('address_change_flag', models.BooleanField(blank=True, db_column='ADDRESS_CHANGE_FLAG', default=False, null=True, verbose_name='Address change flag')),
                ('po_item_created_at', models.DateTimeField(db_column='CREATED_AT', verbose_name='Created At')),
                ('po_item_created_by', models.CharField(db_column='PO_ITEM_CREATED_BY', max_length=12, verbose_name='Creator')),
                ('po_item_changed_at', models.DateTimeField(blank=True, db_column='PO_ITEM_CHANGED_AT', verbose_name='Changed At')),
                ('po_item_changed_by', models.CharField(db_column='PO_ITEM_CHANGED_BY', max_length=12, verbose_name='Changed By')),
                ('po_item_source_system', models.CharField(db_column='PO_ITEM_SOURCE_SYSTEM', max_length=20)),
                ('po_item_destination_system', models.CharField(db_column='PO_ITEM_DESTINATION_SYSTEM', max_length=20)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
                ('po_header_guid', models.ForeignKey(db_column='PO_HEADER_GUID', on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poheader')),
            ],
            options={
                'db_table': 'MTD_PO_ITEM',
                'managed': True,
            },
        ),
    ]
