# Generated by Django 3.0.8 on 2020-07-19 10:41

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200718_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.image_path),
        ),
        migrations.CreateModel(
            name='FeedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=core.models.image_path)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Feed')),
            ],
        ),
        migrations.CreateModel(
            name='DiscussionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=core.models.image_path)),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CommunityDiscussion')),
            ],
        ),
    ]