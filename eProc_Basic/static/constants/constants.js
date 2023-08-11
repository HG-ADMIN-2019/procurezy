const uiConstants = {

    //App Names
    CONST_APPNAME01: 'eProc_Configuration',
    CONST_APPNAME02: 'eProc_Role_authorization',
    CONST_APPNAME03: 'eProc_Registration',

    //Table Names
    CONST_TABLENAME_COUNTRY: 'Country',
    CONST_TABLENAME_SUPPLIERMASTER: 'SupplierMaster',
    CONST_TABLENAME_CURRENCY: 'Currency',
    CONST_TABLENAME_LANGUAGE: 'Languages',
    CONST_TABLENAME_UNSPSC: 'UnspscCategories',
    CONST_TABLENAME_TIMEZONE: 'TimeZone',
    CONST_TABLENAME_UOM: 'UnitOfMeasures',
    CONST_TABLENAME_CLIENT: 'OrgClients',
    CONST_TABLENAME_DOCTYPE: 'DocumentType',
    CONST_TABLENAME_AAC: 'AccountAssignmentCategory',
    CONST_TABLENAME_AAV: 'AccountingData',
    CONST_TABLENAME_NUMBER_RANGE: 'NumberRanges',
    CONST_TABLENAME_AAD: 'AccountingDataDesc',
    CONST_TABLENAME_TRANSACTION_TYPES: 'TransactionTypes',
    CONST_TABLENAME_APPROVAL_TYPE: 'ApproverType',
    CONST_TABLENAME_ALV: 'ApproverLimitValue',
    CONST_TABLENAME_APPROVAL_LIMIT: 'ApproverLimit',
    CONST_TABLENAME_ROLES: 'UserRoles',
    CONST_TABLENAME_AUTH_OBJ: 'AuthorizationObject',
    CONST_TABLENAME_AUTH_GROUP: 'AuthorizationGroup',
    CONST_TABLENAME_AUTH: 'Authorization',
    CONST_TABLENAME_ORG_NODE_TYPE: 'OrgNodeTypes',
    CONST_TABLENAME_ORG_ATTR: 'OrgAttributes',
    CONST_TABLENAME_DETGL: 'DetermineGLAccount',
    CONST_TABLENAME_PRODUCTS_DETAIL: 'ProductsDetail',
    CONST_TABLENAME_CUSTPRODCATDESC:'UnspscCategoriesCustDesc',
    CONST_TABLENAME_CUSTPRODCAT:'UnspscCategoriesCust',
    CONST_TABLENAME_SPEND_LIMIT_ID: 'SpendLimitId',
    CONST_TABLENAME_WORKFLOWSCHEMA:'WorkflowSchema',
    CONST_TABLENAME_WFACCOUNTING:'WorkflowACC',
    CONST_TABLENAME_SPEND_LIMIT_ID:'SpendLimitId',
    CONST_TABLENAME_SPEND_LIMIT_VALUE:'SpendLimitValue',
    CONST_TABLENAME_ADDRESS_TYPE:'addresstype',
    CONST_TABLENAME_ADDRESS:'OrgAddress',
    CONST_TABLENAME_ORGCOMPANIES:'OrgCompanies',
    CONST_TABLENAME_WFSCHEMA: 'WorkflowSchema',
    CONST_TABLENAME_ADDRESSTYPE:'OrgAddressMap',
    CONST_TABLENAME_PURGRP:'OrgPGroup',
    CONST_TABLENAME_PURORG:'OrgPorg',
    CONST_TABLENAME_EMPLOYEE:'UserData',
    CONST_TABLENAME_INCOTERMS: 'Incoterms',
    CONST_TABLENAME_PAYMENT_TERM_DESC: 'Payterms_desc',
    CONST_TABLENAME_PURCHASE_CONTROL: 'PurchaseControl',


    //Header Data
    CONST_HEADER_DATA_COUNTRY: ["COUNTRY_CODE", "COUNTRY_NAME", "del_ind"],
    CONST_HEADER_DATA_CURRENCY: ["CURRENCY_ID", "DESCRIPTION", "del_ind"],
    CONST_HEADER_DATA_LANGUAGE: ["LANGUAGE_ID", "DESCRIPTION", "del_ind"],
    CONST_HEADER_DATA_TIMEZONE: ["TIME_ZONE", "DESCRIPTION", "UTC_DIFFERENCE", "DAYLIGHT_SAVE_RULE", "del_ind"],
    CONST_HEADER_DATA_UOM: ["UOM_ID", "UOM_DESCRIPTION", "del_ind"],
    CONST_HEADER_DATA_CLIENT: ["CLIENT", "DESCRIPTION", "del_ind"],
    CONST_HEADER_DATA_DOCTYPE: ["DOCUMENT_TYPE", "DOCUMENT_TYPE_DESC", "del_ind"],
    CONST_HEADER_DATA_ACC: ["ACCOUNT_ASSIGN_CAT", "DESCRIPTION", "del_ind"],
    CONST_HEADER_DATA_ALV: ["APP_CODE_ID", "UPPER_LIMIT_VALUE", "APP_TYPES", "CURRENCY_ID", "COMPANY_ID", "del_ind"],
    CONST_HEADER_DATA_AAV: ["ACCOUNT_ASSIGN_VALUE", "VALID_FROM", "VALID_TO", "COMPANY_ID", "ACCOUNT_ASSIGN_CAT", "del_ind"],
    CONST_HEADER_DATA_NUMBER_RANGE: ["SEQUENCE", "STARTING", "ENDING", "CURRENT", "DOCUMENT_TYPE", "del_ind"],
    CONST_DOCTYPE_SC: "DOC01",
    CONST_DOCTYPE_PO: "DOC05",
    CONST_DOCTYPE_GV: "DOC06",

    CONST_HEADER_DATA_AAD: ['ACCOUNT_ASSIGN_VALUE', 'DESCRIPTION', 'ACCOUNT_ASSIGN_CAT', 'COMPANY_ID','LANGUAGE_ID', 'del_ind'],
    CONST_HEADER_DATA_TRANSACTION_TYPES: ['DOCUMENT_TYPE', 'TRANSACTION_TYPE', 'DESCRIPTION', 'SEQUENCE','ACTIVE_INACTIVE', 'del_ind'],
    CONST_HEADER_DATA_APPROVAL_TYPE: ["APP_TYPES", "APPROVAL_TYPE_DESC", "del_ind"],
    CONST_HEADER_DATA_APPROVAL_LIMIT: ['APPROVER_USERNAME', 'APP_CODE_ID', 'COMPANY_ID', 'del_ind'],
    CONST_HEADER_DATA_ROLES: ['ROLES', 'ROLE_DESC', 'del_ind'],
    CONST_HEADER_DATA_AUTH_OBJ: ['AUTH_OBJ_ID', 'AUTH_LEVEL', 'AUTH_LEVEL_ID', 'AUTH_LEVEL_DESC', 'del_ind'],
    CONST_HEADER_DATA_AUTH_GROUP: ['AUTH_OBJ_GRP', 'AUTH_OBJ_ID', 'AUTH_GRP_DESC', 'AUTH_LEVEL', 'del_ind'],
    CONST_HEADER_DATA_AUTH: ['AUTH_OBJ_GRP', 'AUTH_TYPE', 'ROLE', 'del_ind'],
    CONST_HEADER_DATA_ORG_NODE_TYPE: ['NODE_TYPE', 'DESCRIPTION', 'del_ind'],
    CONST_HEADER_DATA_ORG_ATTR: ['ATTRIBUTE_ID', 'ATTRIBUTE_NAME','RANGE_INDICATOR','MULTIPLE_VALUE','ALLOW_DEFAULTS','INHERIT_VALUES','MAXIMUM_LENGTH', 'del_ind'],
    CONST_HEADER_DATA_DETGL: ['PROD_CAT_ID','GL_ACCOUNT','GL_ACC_DEFAULT','ACCOUNT_ASSIGN_CAT','COMPANY_ID','FROM_VALUE','TO_VALUE','CURRENCY_ID',"del_ind"],
    CONST_HEADER_DATA_SUPPLIERMASTER: ['SUPPLIER_ID','SUPP_TYPE','NAME1','NAME2','CITY','POSTAL_CODE','STREET','LANDLINE','MOBILE_NUM','FAX','EMAIL','EMAIL1','EMAIL2','EMAIL3','EMAIL4','EMAIL5','OUTPUT_MEDIUM','SEARCH_TERM1','SEARCH_TERM2','DUNS_NUMBER','BLOCK DATE','BLOCK','WORKING DAYS','IS_ACTIVE','REGISTRATION_NUMBER','del_ind','COUNTRY_CODE','CURRENCY_ID','LANGUAGE_ID'],
    CONST_HEADER_DATA_CUSTPRODCATDESC:['CATEGORY_DESC','del_ind','LANGUAGE_ID','PROD_CAT_ID'],
    CONST_HEADER_DATA_CUSTPRODCAT:['del_ind','PRODUCT CATEGORY'],
    CONST_HEADER_DATA_SPEND_LIMIT_ID:['SPEND_CODE_ID', 'SPENDER_USERNAME', 'COMPANY_ID', 'del_ind'],
    CONST_HEADER_DATA_PRODUCTS_DETAIL: ['CATALOG_ITEM','PRODUCT_NAME','PRODUCT_DESCRIPTION','supp_product_id ','SUPPLIER_ID','SEARCH_TERM1','SEARCH_TERM2','MANUFACTURER','BRAND','OFFER_KEY','PRICE_ON_REQUEST','MANU_PROD','PRODUCT_TYPE','CATALOG_ID','LEAD_TIME','QUANTITY_AVAIL','PRICE','PRICE_UNIT','PROD_CAT_ID','QUANTITY_MIN','CTR_NUM','CTR_ITEM_NUM','PRODUCT_STATUS','PRICE_1','QUANTITY_1','PRICE_2','QUANTITY_2','PRICE_3', 'QUANTITY_3','EXTERNAL_LINK','SUPPLIER_PRODUCT_ID','EFORM_ID','PRODUCT_INFO_ID','PRODUCTS_DETAIL_SOURCE_SYSTEM', 'CLIENT','COUNTRY_OF_ORIGIN','CURRENCY','LANGUAGE','UNIT_OF_MEASURE','UNSPSC', 'PRODUCT_ID','del_ind'],
    CONST_HEADER_DATA_WORKFLOWSCHEMA:['WORKFLOW SCEHMA','APPROVAR TYPES','COMPANY CODE','del_ind'],
    CONST_HEADER_DATA_SPEND_LIMIT_VALUE:['SPEND_CODE_ID', 'UPPER_LIMIT_VALUE', 'COMPANY_ID','CURRENCY_ID','del_ind'],
    CONST_HEADER_DATA_ADDRESS_TYPE:['ADDRESS_TYPE','ADDRESS NUMBER','COMPANY_ID','VALID_FROM','VALID_TO','del_ind'],
    CONST_HEADER_DATA_ADDRESS:['ADDRESS_NUMBER', 'ADDRESS_PARTNER_TYPE','TITLE', 'NAME1', 'NAME2', 'STREET', 'AREA', 'LANDMARK', 'CITY','postal_code', 'REGION', 'MOBILE_NUMBER', 'TELEPHONE_NUMBER', 'FAX_NUMBER', 'EMAIL','COUNTRY_CODE','LANGUAGE_ID', 'TIME_ZONE', 'del_ind'],
    CONST_HEADER_DATA_ORGCOMPANIES:['COMPANY_ID','NAME1', 'NAME2','del_ind'],
    CONST_HEADER_DATA_WFACCOUNTING:['ACC_VALUE', 'COMPANY_ID', 'APP_USERNAME','SUP_COMPANY_ID', 'SUP_ACC_VALUE', 'del_ind','ACCOUNT_ASSIGN_CAT', 'CURRENCY_ID', 'SUP_ACCOUNT_ASSIGN_CAT'],
    CONST_HEADER_DATA_PURGRP:[ 'PGROUP_ID', 'DESCRIPTION','PORG_ID','OBJECT_ID','del_ind'],
    CONST_HEADER_DATA_PURORG:[ 'PORG_ID', 'DESCRIPTION','COMPANY_ID','OBJECT_ID','del_ind'],
    CONST_HEADER_DATA_EMP_DETAIL: ['EMAIL','USERNAME','PERSON_NO','FORM_OF_ADDRESS','FIRST_NAME','LAST_NAME','GENDER','PHONE_NUM','PASSWORD','DATE_JOINED','FIRST_LOGIN','LAST_LOGIN','IS_ACTIVE','IS_SUPERUSER','IS_STAFF','DATE_FORMAT','EMPLOYEE_ID','DECIMAL_NOTATION','USER_TYPE','LOGIN_ATTEMPTS','USER_LOCKED','PWD_LOCKED','SSO_USER','VALID_FROM','VALID_TO','CURRENCY','LANGUAGE_ID','OBJECT_ID', 'TIME_ZONE','del_ind'],
    CONST_HEADER_DATA_INCOTERMS: ["INCOTERM_KEY", "DESCRIPTION", "del_ind"],
    CONST_HEADER_DATA_PAYMENT_TERMS_DESC: ['PAYMENT_TERM_KEY','DESCRIPTION','DAY_LIMIT','del_ind', 'LANGUAGE_ID'],
    CONST_HEADER_DATA_PUR_CONTROL: ["company_code_id", "purchase_ctrl_flag", "call_off", "del_ind"],
}


