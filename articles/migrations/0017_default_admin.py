from django.db import migrations
from django.contrib.auth import get_user_model

def create_default_admin(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@climategoal.com',
            password='password'
        )

def remove_default_admin(apps, schema_editor):
    User = get_user_model()
    User.objects.filter(username='admin').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_contactmessage'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_default_admin, remove_default_admin),
    ]
