# Generated by Django 5.0.4 on 2024-05-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0003_assessment_prediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='ground_truth',
            field=models.IntegerField(blank=True, choices=[(0, 'Yes'), (1, 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='prediction',
            field=models.IntegerField(blank=True, choices=[(0, 'Yes'), (1, 'No')], null=True),
        ),
    ]