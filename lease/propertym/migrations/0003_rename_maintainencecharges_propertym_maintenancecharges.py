# Generated by Django 4.1.7 on 2023-02-18 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("propertym", "0002_remove_propertym_modifieddate"),
    ]

    operations = [
        migrations.RenameField(
            model_name="propertym",
            old_name="maintainenceCharges",
            new_name="maintenanceCharges",
        ),
    ]
