# Generated by Django 2.1.8 on 2019-09-10 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0003_goodstype_type_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodstype',
            name='type_picture',
            field=models.ImageField(upload_to='images'),
        ),
    ]
