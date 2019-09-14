# Generated by Django 2.2.5 on 2019-09-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='article_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.CharField(choices=[('Diary', 'Diary'), ('Vegetables', 'Vegetables'), ('Fruits', 'Fruits'), ('Backing & GRains', 'Backing & GRains'), ('Added Sweeteners', 'Added Sweeteners'), ('Spices', 'Spices'), ('Meats', 'Meats'), ('Seafood', 'Seafood'), ('Condiments', 'Condiments'), ('Oils', 'Oils'), ('Seasoning', 'Seasoning'), ('Sauces', 'Sauces'), ('Legumes', 'Legumes'), ('Alcohol', 'Alcohol'), ('Soup', 'Soup'), ('Nuts', 'Nuts'), ('Dessert & Snack', 'Dessert & Snack'), ('Beverages', 'Beverages')], default='Fruits', max_length=255),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit_name',
            field=models.CharField(choices=[('g', 'g'), ('kg', 'kg'), ('cl', 'cl'), ('l', 'l')], default='kg', max_length=255),
        ),
    ]
