# Generated by Django 3.0.2 on 2020-02-04 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20200201_1841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='company',
            name='images',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Image'),
        ),
    ]
