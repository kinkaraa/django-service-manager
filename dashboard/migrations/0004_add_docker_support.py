# Migration for Docker support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_service_log_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.CharField(
                choices=[('standard', 'Standard Process'), ('docker', 'Docker Container')],
                default='standard',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='docker_container_name',
            field=models.CharField(
                blank=True,
                help_text='Nama container untuk tracking (opsional)',
                max_length=100,
                null=True
            ),
        ),
    ]
