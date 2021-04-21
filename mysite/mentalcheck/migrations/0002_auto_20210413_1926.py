# Generated by Django 3.1.6 on 2021-04-13 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mentalcheck', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionsShared', models.BooleanField(default=False)),
                ('followed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('age', models.IntegerField()),
                ('medicalHistory', models.TextField(blank=True, default='')),
                ('emergencyContact', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='QuestionMC',
        ),
        migrations.DeleteModel(
            name='Support',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='questiontext',
            name='userAnswered',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]