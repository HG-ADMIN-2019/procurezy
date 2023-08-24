# Generated by Django 3.1.7 on 2023-08-24 13:07

from django.db import migrations, models
import django.db.models.deletion
import eProc_Org_Support.models.org_support_models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eProc_Configuration', '0001_initial'),
        ('eProc_Org_Model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgSupport',
            fields=[
                ('org_support_guid', models.CharField(db_column='ORG_SUPPORT_GUID', max_length=32, primary_key=True, serialize=False)),
                ('org_support_types', models.CharField(db_column='ORG_SUPPORT_TYPES', max_length=50)),
                ('org_support_email', models.CharField(db_column='ORG_SUPPORT_EMAIL', max_length=50)),
                ('org_support_number', models.CharField(db_column='ORG_SUPPORT_NUMBER', max_length=20)),
                ('username', models.CharField(db_column='USERNAME', max_length=16, null=True)),
                ('org_support_created_at', models.DateTimeField(db_column='ORG_SUPPORT_CREATED_AT', null=True)),
                ('org_support_created_by', models.CharField(db_column='ORG_SUPPORT_CREATED_BY', max_length=16, null=True)),
                ('org_support_changed_at', models.DateTimeField(blank=True, db_column='ORG_SUPPORT_CHANGED_AT', null=True)),
                ('org_support_changed_by', models.CharField(db_column='ORG_SUPPORT_CHANGED_BY', max_length=16, null=True)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
                ('object_id', models.ForeignKey(db_column='OBJECT_ID', null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Org_Model.orgmodel')),
            ],
            options={
                'db_table': 'MTD_ORG_SUPPORT',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrgAnnouncements',
            fields=[
                ('unique_announcement_id', models.CharField(db_column='UNIQUE_ANNOUNCEMENT_ID', default=None, max_length=32, primary_key=True, serialize=False)),
                ('announcement_id', models.CharField(db_column='ANNOUNCEMENT_ID', max_length=10, null=True)),
                ('announcement_subject', models.CharField(db_column='ANNOUNCEMENT_SUBJECT', max_length=225)),
                ('announcement_description', models.CharField(db_column='ANNOUNCEMENT_DESCRIPTION', max_length=1000)),
                ('announcement_type', models.CharField(db_column='ANNOUNCEMENT_TYPE', max_length=50, null=True)),
                ('status', models.CharField(db_column='STATUS', max_length=30)),
                ('priority', models.CharField(db_column='PRIORITY', max_length=30)),
                ('announcement_from_date', models.DateTimeField(blank=True, db_column='ANNOUNCEMENT_FROM_DATE', null=True)),
                ('announcement_to_date', models.DateTimeField(blank=True, db_column='ANNOUNCEMENT_TO_DATE', null=True)),
                ('announcements_created_at', models.DateTimeField(blank=True, db_column='ANNOUNCEMENTS_CREATED_AT', null=True)),
                ('announcements_created_by', models.CharField(db_column='ANNOUNCEMENTS_CREATED_BY', max_length=16, null=True)),
                ('announcements_changed_at', models.DateTimeField(blank=True, db_column='ANNOUNCEMENTS_CHANGED_AT', null=True)),
                ('announcements_changed_by', models.CharField(db_column='ANNOUNCEMENTS_CHANGED_BY', max_length=16, null=True)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
                ('object_id', models.ForeignKey(db_column='OBJECT_ID', null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Org_Model.orgmodel')),
            ],
            options={
                'db_table': 'MTD_ORG_ANNOUNCEMENTS',
                'managed': True,
            },
            bases=(models.Model, eProc_Org_Support.models.org_support_models.DBQueriesOrgannsmt),
        ),
    ]
