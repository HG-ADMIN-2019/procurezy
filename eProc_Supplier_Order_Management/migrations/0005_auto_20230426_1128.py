# Generated by Django 3.1.7 on 2023-04-26 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Supplier_Order_Management', '0004_someformfielddata_eform_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sompoaddresses',
            name='address_details',
            field=models.CharField(db_column='ADDRESS_DETAILS', max_length=400, null=True),
        ),
    ]