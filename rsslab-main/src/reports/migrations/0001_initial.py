# Generated by Django 4.0.5 on 2022-06-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_num', models.CharField(blank=True, max_length=10, null=True)),
                ('history', models.TextField(blank=True, null=True)),
                ('record_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
