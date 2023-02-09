# Generated by Django 3.1.7 on 2022-12-12 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Configuration', '0015_auto_20221201_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDetails',
            fields=[
                ('project_detail_guid', models.CharField(db_column='PROJECT_DETAIL_GUID', max_length=32, primary_key=True, serialize=False)),
                ('project_id', models.CharField(db_column='PROJECT_ID', max_length=20)),
                ('project_name', models.CharField(db_column='PROJECT_NAME', max_length=30)),
                ('project_desc', models.CharField(db_column='PROJECT_DESC', max_length=255)),
                ('start_date', models.DateField(db_column='START_DATE')),
                ('end_date', models.DateField(db_column='END_DATE')),
                ('del_ind', models.BooleanField(db_column='DEL_IND', default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
            ],
            options={
                'db_table': 'MAD_PROJECT_DETAILS',
                'managed': True,
                'unique_together': {('client', 'project_id')},
            },
        ),
        migrations.CreateModel(
            name='ProjectCategories',
            fields=[
                ('project_categories_guid', models.CharField(db_column='PROJECT_CATEGORIES_GUID', max_length=32, primary_key=True, serialize=False)),
                ('project_id', models.CharField(db_column='PROJECT_ID', max_length=20)),
                ('project_category', models.CharField(db_column='PROJECT_CATEGORY', max_length=255)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
            ],
            options={
                'db_table': 'MAD_PROJECT_CATEGORIES',
                'managed': True,
                'unique_together': {('client', 'project_id', 'project_category')},
            },
        ),
    ]