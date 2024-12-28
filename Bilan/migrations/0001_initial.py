# Generated by Django 5.0.10 on 2024-12-28 00:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Consultation', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BilanBiologique',
            fields=[
                ('IdBilanBiologique', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parametre', models.CharField(max_length=25)),
                ('valeur', models.FloatField()),
                ('Consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BilanBiologique_Consultation', to='Consultation.consultation')),
                ('medecin', models.ForeignKey(limit_choices_to={'role': 'laborantin'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BilanBiologique_Medecin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BilanRadiologique',
            fields=[
                ('IdBilanRadiologique', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('examen', models.CharField(max_length=25)),
                ('image', models.URLField()),
                ('compterendu', models.IntegerField(null=True)),
                ('Consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BilanRadiologique_Consultation', to='Consultation.consultation')),
                ('Medecin', models.ForeignKey(limit_choices_to={'role': 'radiologue'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BilanRadiologique_Medecin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DemandeBilan',
            fields=[
                ('IdDemandeBilan', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('typebilan', models.CharField(choices=[('B', 'Biologique'), ('R', 'Radiologique')], max_length=1)),
                ('TypeTest', models.CharField(max_length=150)),
                ('etat', models.CharField(choices=[('enattente', 'En attente'), ('traitee', 'Traitée')], default='enattente', max_length=10)),
                ('patient', models.ForeignKey(limit_choices_to={'role': 'patient'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DemandeBilan_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
