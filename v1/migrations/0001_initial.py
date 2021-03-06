# Generated by Django 3.2.6 on 2021-11-08 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='익명', max_length=10, verbose_name="User's username")),
                ('password', models.CharField(max_length=100, verbose_name='Username')),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='fineDustInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='v1.user', verbose_name='User')),
                ('firstCityName', models.CharField(max_length=50, null=True)),
                ('lastCityName', models.CharField(max_length=50, null=True)),
                ('fullCityName', models.CharField(max_length=100, null=True)),
                ('fineDust', models.CharField(max_length=10, null=True, verbose_name='good-bad-worst')),
                ('fineDustValue', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='weatherInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='v1.user', verbose_name='user')),
                ('cityName', models.TextField(default='')),
                ('weather', models.TextField()),
                ('temperature', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='userRoomPlug',
            fields=[
                ('primaryKey', models.BigAutoField(db_column='pk', primary_key=True, serialize=False, verbose_name='pk')),
                ('roomID', models.IntegerField()),
                ('roomName', models.CharField(default='room', max_length=15, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userRoomLight',
            fields=[
                ('primaryKey', models.BigAutoField(db_column='pk', primary_key=True, serialize=False, verbose_name='pk')),
                ('roomID', models.IntegerField()),
                ('roomName', models.CharField(default='room', max_length=15, null=True)),
                ('light1', models.BooleanField(default=False)),
                ('lightName1', models.CharField(default='light1', max_length=15, null=True)),
                ('light2', models.BooleanField(default=False)),
                ('lightName2', models.CharField(default='light2', max_length=15, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
