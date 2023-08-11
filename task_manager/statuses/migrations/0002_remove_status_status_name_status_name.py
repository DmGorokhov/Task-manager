# Generated by Django 4.2.3 on 2023-08-10 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='status_name',
        ),
        migrations.AddField(
            model_name='status',
            name='name',
            field=models.CharField(default='fg', max_length=150, unique=True, verbose_name='Name'),
            preserve_default=False,
        ),
    ]