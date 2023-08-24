# Generated by Django 3.1.7 on 2023-08-24 13:07

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import eProc_Registration.models.registration_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('eProc_Configuration', '0002_auto_20230824_1307'),
        ('eProc_Org_Model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDataHistory',
            fields=[
                ('email_key', models.AutoField(db_column='EMAIL_KEY', primary_key=True, serialize=False)),
                ('email', models.EmailField(db_column='EMAIL', max_length=100)),
                ('username', models.CharField(db_column='USERNAME', max_length=16)),
                ('person_no', models.CharField(blank=True, db_column='PERSON_NO', max_length=2, null=True, verbose_name='Personal Number')),
                ('form_of_address', models.CharField(db_column='FORM_OF_ADDRESS', max_length=40)),
                ('first_name', models.CharField(db_column='FIRST_NAME', max_length=30)),
                ('last_name', models.CharField(db_column='LAST_NAME', max_length=30)),
                ('gender', models.CharField(blank=True, db_column='GENDER', max_length=12, null=True)),
                ('phone_num', models.CharField(db_column='PHONE_NUM', max_length=30, null=True)),
                ('password', models.CharField(db_column='PASSWORD', max_length=256)),
                ('date_joined', models.DateTimeField(db_column='DATE_JOINED', null=True)),
                ('first_login', models.DateTimeField(db_column='FIRST_LOGIN', null=True)),
                ('last_login', models.DateTimeField(db_column='LAST_LOGIN', null=True)),
                ('is_active', models.BooleanField(db_column='IS_ACTIVE', default=True)),
                ('is_superuser', models.BooleanField(db_column='IS_SUPERUSER', default=False)),
                ('is_staff', models.BooleanField(db_column='IS_STAFF', default=True)),
                ('date_format', models.CharField(db_column='DATE_FORMAT', max_length=30, null=True)),
                ('employee_id', models.CharField(db_column='EMPLOYEE_ID', max_length=15, null=True)),
                ('decimal_notation', models.CharField(db_column='DECIMAL_NOTATION', max_length=15, null=True)),
                ('user_type', models.CharField(db_column='USER_TYPE', default=False, max_length=25)),
                ('login_attempts', models.PositiveIntegerField(db_column='LOGIN_ATTEMPTS', default=False)),
                ('user_locked', models.BooleanField(db_column='USER_LOCKED', default=False)),
                ('pwd_locked', models.BooleanField(db_column='PWD_LOCKED', default=False)),
                ('sso_user', models.BooleanField(db_column='SSO_USER', default=False, null=True)),
                ('user_data_created_at', models.DateTimeField(blank=True, db_column='USER_DATA_CREATED_AT', null=True)),
                ('user_data_created_by', models.CharField(db_column='USER_DATA_CREATED_BY', max_length=30, null=True)),
                ('user_data_changed_at', models.DateTimeField(blank=True, db_column='USER_DATA_CHANGED_AT', null=True)),
                ('user_data_changed_by', models.CharField(db_column='USER_DATA_CHANGED_BY', max_length=30, null=True)),
                ('valid_from', models.DateTimeField(blank=True, db_column='VALID_FROM', null=True)),
                ('valid_to', models.DateTimeField(blank=True, db_column='VALID_TO', null=True)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.CharField(db_column='CLIENT', max_length=8, null=True)),
                ('currency_id', models.CharField(db_column='CURRENCY_ID', max_length=3, null=True)),
                ('language_id', models.CharField(db_column='LANGUAGE_ID', max_length=2, null=True)),
                ('object_id', models.PositiveBigIntegerField(db_column='OBJECT_ID', null=True)),
                ('time_zone', models.CharField(db_column='TIME_ZONE', max_length=6, null=True)),
            ],
            options={
                'db_table': 'MTD_USER_INFO_HISTORY',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('email', models.EmailField(db_column='EMAIL', error_messages={'unique': 'Email-Id already exists.'}, max_length=100, primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='USERNAME', max_length=16)),
                ('person_no', models.CharField(blank=True, db_column='PERSON_NO', max_length=2, null=True, verbose_name='Personal Number')),
                ('form_of_address', models.CharField(db_column='FORM_OF_ADDRESS', max_length=40)),
                ('first_name', models.CharField(db_column='FIRST_NAME', max_length=30)),
                ('last_name', models.CharField(db_column='LAST_NAME', max_length=30)),
                ('gender', models.CharField(blank=True, db_column='GENDER', max_length=12, null=True)),
                ('phone_num', models.CharField(db_column='PHONE_NUM', max_length=30, null=True)),
                ('password', models.CharField(db_column='PASSWORD', max_length=256)),
                ('date_joined', models.DateTimeField(db_column='DATE_JOINED', null=True)),
                ('first_login', models.DateTimeField(db_column='FIRST_LOGIN', null=True)),
                ('last_login', models.DateTimeField(db_column='LAST_LOGIN', null=True)),
                ('is_active', models.BooleanField(db_column='IS_ACTIVE', default=True)),
                ('is_superuser', models.BooleanField(db_column='IS_SUPERUSER', default=False)),
                ('is_staff', models.BooleanField(db_column='IS_STAFF', default=True)),
                ('date_format', models.CharField(db_column='DATE_FORMAT', max_length=30, null=True)),
                ('employee_id', models.CharField(db_column='EMPLOYEE_ID', max_length=15, null=True)),
                ('decimal_notation', models.CharField(db_column='DECIMAL_NOTATION', max_length=15, null=True)),
                ('user_type', models.CharField(db_column='USER_TYPE', default=False, max_length=25)),
                ('login_attempts', models.PositiveIntegerField(db_column='LOGIN_ATTEMPTS', default=False)),
                ('user_locked', models.BooleanField(db_column='USER_LOCKED', default=False)),
                ('pwd_locked', models.BooleanField(db_column='PWD_LOCKED', default=False)),
                ('sso_user', models.BooleanField(db_column='SSO_USER', default=False, null=True)),
                ('user_data_created_at', models.DateTimeField(blank=True, db_column='USER_DATA_CREATED_AT', null=True)),
                ('user_data_created_by', models.CharField(db_column='USER_DATA_CREATED_BY', max_length=30, null=True)),
                ('user_data_changed_at', models.DateTimeField(blank=True, db_column='USER_DATA_CHANGED_AT', null=True)),
                ('user_data_changed_by', models.CharField(db_column='USER_DATA_CHANGED_BY', max_length=30, null=True)),
                ('valid_from', models.DateTimeField(blank=True, db_column='VALID_FROM', null=True)),
                ('valid_to', models.DateTimeField(blank=True, db_column='VALID_TO', null=True)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
                ('currency_id', models.ForeignKey(db_column='CURRENCY', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Configuration.currency')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('language_id', models.ForeignKey(db_column='LANGUAGE_ID', max_length=5, null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.languages')),
                ('object_id', models.ForeignKey(db_column='OBJECT_ID', null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Org_Model.orgmodel')),
                ('time_zone', models.ForeignKey(db_column='TIME_ZONE', null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.timezone')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'MMD_USER_INFO',
                'managed': True,
                'unique_together': {('client', 'username')},
            },
            bases=(models.Model, eProc_Registration.models.registration_model.DBQueriesUser),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
