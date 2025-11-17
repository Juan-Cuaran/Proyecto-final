from django.db import migrations


def create_default_user(apps, schema_editor):
    UsersModel = apps.get_model('core', 'UsersModel')
    UsersModel.objects.update_or_create(
        UsersID='1081277507',
        defaults={
            'Name': 'Juanes',
            'Password': 'Juanes123',
            'Role': 'admin',
        }
    )


def remove_default_user(apps, schema_editor):
    UsersModel = apps.get_model('core', 'UsersModel')
    UsersModel.objects.filter(UsersID='1081277507').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_user, reverse_code=remove_default_user),
    ]
