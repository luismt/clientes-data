# Generated by Django 4.1.6 on 2023-03-06 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_fullsolution_managers_instalaciones_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrataciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contrato', models.CharField(max_length=100)),
                ('servicio', models.CharField(max_length=100)),
                ('periodo', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.reporte')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]