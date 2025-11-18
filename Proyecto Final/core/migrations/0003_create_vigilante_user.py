from django.db import migrations


def create_vigilante_user(apps, schema_editor):
    UsersModel = apps.get_model('core', 'UsersModel')
    UsersModel.objects.update_or_create(
        UsersID='1081277506',
        defaults={
            'Name': 'Juan',
            'Password': 'Juanca01',
            'Role': 'vigilante',
        }
    )


def remove_vigilante_user(apps, schema_editor):
    UsersModel = apps.get_model('core', 'UsersModel')
    UsersModel.objects.filter(UsersID='1081277506').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_create_default_user'),
    ]

    operations = [
        migrations.RunPython(create_vigilante_user, reverse_code=remove_vigilante_user),
    ]
