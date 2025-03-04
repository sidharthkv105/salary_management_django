# Generated by Django 5.1.2 on 2025-03-04 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_date', models.DateField()),
                ('pay', models.FloatField()),
                ('da', models.FloatField()),
                ('hra', models.FloatField()),
                ('allowance', models.FloatField()),
                ('co_date', models.DateField()),
                ('gpf', models.FloatField()),
                ('sli', models.FloatField()),
                ('gis', models.FloatField()),
                ('lic', models.FloatField()),
                ('medisep', models.FloatField()),
                ('gpais', models.FloatField()),
                ('pro_tax', models.FloatField()),
                ('i_tax', models.FloatField()),
                ('gross', models.FloatField()),
                ('deduction', models.FloatField()),
                ('net', models.FloatField()),
            ],
        ),
    ]
