# Generated by Django 3.1.7 on 2023-06-23 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Shopping_Cart', '0007_auto_20221114_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='scitem',
            name='grouping_ind',
            field=models.BooleanField(db_column='grouping_ind', default=False, null=True, verbose_name='grouping_ind '),
        ),
    ]
