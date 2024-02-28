# Generated by Django 5.0 on 2024-01-23 01:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_cartitem_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Oder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('p', 'Pending'), ('c', 'Complete'), ('f', 'Failed')], default='P', max_length=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('oder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oder_items', to='store.oder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.product')),
            ],
        ),
    ]
