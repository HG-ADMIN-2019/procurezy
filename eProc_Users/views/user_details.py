"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        user_details.py
    Usage:
        Story SP12-10
        Function to get the user details
        Taking the user email id and getting details and rendering back to the user details page

     Author:
        Varsha Prasad
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.constants.constants import CONST_DECIMAL_NOTATION, CONST_DATE_FORMAT, CONST_USER_REG
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.functions.randam_generator import random_alpha_numeric
from eProc_Basic.Utilities.messages.messages import MSG183
from eProc_Configuration.models import *
from eProc_Emails.Utilities.email_notif_generic import email_notify
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import convert_to_boolean
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()


@login_required()
@transaction.atomic
def update_user_basic_details(request):
    message = ''
    update_user_info(request)
    if request.method == 'POST':
        message, msg_type = save_user_data(request)
        # update_user_basic_data = django_query_instance.django_filter_only_query(UserData,
        #                                                                         {'email': request.POST.get('email'),
        #                                                                          'del_ind': False})
        #
        # update_user_basic_data.update(
        #     first_name=request.POST.get('first_name'),
        #     last_name=request.POST.get('last_name'),
        #     phone_num=request.POST.get('phone_num'),
        #     language_id=request.POST.get('language_id'),
        #     time_zone=request.POST.get('time_zone'),
        #     date_format=request.POST.get('date_format'),
        #     employee_id=request.POST.get('employee_id'),
        #     decimal_notation=request.POST.get('decimal_notation'),
        #     currency_id=request.POST.get('currency_id'),
        #     user_type=request.POST.get('user_type'),
        #     user_locked=convert_to_boolean(request.POST.get('user_locked')),
        #     pwd_locked=convert_to_boolean(request.POST.get('pwd_locked')),
        #     is_superuser=convert_to_boolean(request.POST.get('super_user')),
        # )
        # msgid = 'MSG183'
        # error_msg = get_message_desc(msgid)[1]

        return JsonResponse({'message': message, 'msg_type': msg_type})


def save_user_data(request):
    """

    """
    message = {}
    update_supplier_guid = ''
    user_details = {}
    status = request.POST.get('status')
    user_details['username'] = request.POST.get('username')
    user_details['first_name'] = request.POST.get('first_name')
    user_details['last_name'] = request.POST.get('last_name')
    user_details['employee_id'] = request.POST.get('employee_id')
    user_details['user_type'] = request.POST.get('user_type')
    user_details['language_id'] = request.POST.get('language_id')
    user_details['currency_id'] = request.POST.get('currency_id')
    user_details['time_zone'] = request.POST.get('time_zone')
    user_details['email'] = request.POST.get('email')
    user_details['phone_num'] = request.POST.get('phone_num')
    user_details['date_format'] = request.POST.get('date_format')
    user_details['decimal_notation'] = request.POST.get('decimal_notation')
    user_details['login_attempts'] = request.POST.get('login_attempts')
    user_details['is_superuser'] = request.POST.get('super_user')
    user_details['user_locked'] = request.POST.get('user_locked')
    user_details['pwd_locked'] = request.POST.get('pwd_locked')
    user_details['is_active'] = request.POST.get('is_active')

    if user_details['login_attempts'] == '':
        user_details['login_attempts'] = 0

    # encrypted_supp = encrypt(supplier_details['supplier_id'])
    if status in ['UPDATE', 'update']:
        if django_query_instance.django_existence_check(UserData,
                                                        {'email': user_details['email'],
                                                         'del_ind': False,
                                                         'client': global_variables.GLOBAL_CLIENT}):
            django_query_instance.django_update_query(UserData,
                                                      {'email': user_details['email'],
                                                       'del_ind': False,
                                                       'client': global_variables.GLOBAL_CLIENT}, user_details)
            msgid = 'MSG177'
            error_msg = get_message_desc(msgid)[1]

            message['type'] = 'success'
            return error_msg, message
    else:
        if django_query_instance.django_existence_check(UserData,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'username': user_details['username'],
                                                         'del_ind': False}):
            msgid = 'MSG084'
            error_msg = get_message_desc(msgid)[1]

            message['type'] = 'error'
            return error_msg, message
        elif django_query_instance.django_existence_check(UserData,
                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                           'employee_id': user_details[
                                                               'employee_id'],
                                                           'del_ind': False}):
            # msgid = 'MSG300'
            # error_msg = get_message_desc(msgid)[1]
            error_msg = "Username exists"
            message['type'] = 'error'
            return error_msg, message
        elif django_query_instance.django_existence_check(UserData,
                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                           'email': user_details[
                                                               'email'],
                                                           'del_ind': False}):
            msgid = 'MSG0121'
            error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            error_msg = ' Email Already Exists'
            message['type'] = 'error'
            return error_msg, message
        else:
            user_details['client'] = global_variables.GLOBAL_CLIENT
            user_details['time_zone'] = django_query_instance.django_get_query(TimeZone, {
                'time_zone': user_details['time_zone']})
            user_details['currency_id'] = django_query_instance.django_get_query(Currency, {
                'currency_id': user_details['currency_id']})
            user_details['language_id'] = django_query_instance.django_get_query(Languages, {
                'language_id': user_details['language_id']})
            password = random_alpha_numeric(8)
            user_details['password'] = make_password(password)
            django_query_instance.django_create_query(UserData,
                                                      user_details)
            variant_name = CONST_USER_REG
            username = user_details['username']
            email = user_details['email']
            first_name = user_details['first_name']
            email_data = {
                'username': username,
                'email': email,
                'first_name': first_name,
                'email_user_monitoring_guid': '',
                'password': password
            }
            email_notify(email_data, variant_name, global_variables.GLOBAL_CLIENT)
            msgid = 'MSG183'
            error_msg = get_message_desc(msgid)[1]
            message['type'] = 'success'

    return error_msg, message
