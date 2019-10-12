# Generated by Django 2.2.5 on 2019-09-16 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_c_rbac', '0002_auto_20190916_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, verbose_name='部门名称')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='校区名称')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('userinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_c_rbac.UserInfo')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_crm.Department', verbose_name='部门')),
            ],
            bases=('app_c_rbac.userinfo',),
        ),
    ]
