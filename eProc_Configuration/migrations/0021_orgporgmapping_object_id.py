# Generated by Django 3.1.7 on 2023-06-15 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Org_Model', '0001_initial'),
        ('eProc_Configuration', '0020_orgporgmapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgporgmapping',
            name='object_id',
            field=models.ForeignKey(db_column='OBJECT_ID', default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Org_Model.orgmodel'),
        ),
    ]