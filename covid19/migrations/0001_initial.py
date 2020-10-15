# Generated by Django 3.0.8 on 2020-10-12 20:04

from django.db import migrations, models
import django.db.models.deletion
from .loaders.loader import load_fixture, unload_fixture
from .loaders.db_views import *

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EconomyState',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=25, verbose_name='State')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('eventname', models.CharField(max_length=50, verbose_name='Name of Event')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('geocodeid', models.IntegerField(primary_key=True, serialize=False, verbose_name='Geographic Code Identifier')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='State Name')),
                ('abbreviation', models.CharField(max_length=2, verbose_name='State Abbreviation')),
            ],
        ),
        migrations.CreateModel(
            name='CensusData',
            fields=[
                ('state', models.ForeignKey(db_column='geocodeid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='covid19.State', unique=True)),
                ('population', models.IntegerField(verbose_name='Population')),
                ('density', models.FloatField(null=True, verbose_name='Population Density')),
            ],
        ),
        migrations.CreateModel(
            name='CoronaVirusTesting',
            fields=[
                ('state', models.ForeignKey(db_column='geocodeid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='covid19.State', unique=True)),
                ('percentageoftestingtarget', models.IntegerField(null=True, verbose_name='Percentage Of Testing Target')),
                ('positivitytestrate', models.IntegerField(null=True, verbose_name='Positivity Test Rage')),
                ('dailytestsper100k', models.IntegerField(null=True, verbose_name='Daily Tests Per 100,000')),
                ('hospitalizedper100k', models.IntegerField(null=True, verbose_name='Hospitalized Per 100,000')),
            ],
        ),
        migrations.CreateModel(
            name='GredeEffDt',
            fields=[
                ('state', models.ForeignKey(db_column='state', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='covid19.State', to_field='name')),
                ('grade', models.CharField(max_length=3, verbose_name='State Grade')),
                ('stayathomedeclaredate', models.DateField(null=True, verbose_name='Date Stay At Home was Declared')),
                ('stayathomestartdate', models.DateField(null=True, verbose_name='Date Stay At Home Started')),
            ],
        ),
        migrations.CreateModel(
            name='StateReopening',
            fields=[
                ('state', models.ForeignKey(db_column='geocodeid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='covid19.State', unique=True)),
                ('stayathomeexpiredate', models.DateField(null=True, verbose_name='Date Stay At Home Order Expired')),
                ('openbusinesses', models.CharField(max_length=3000, null=True, verbose_name='Open Businesses Description')),
                ('closedbusinesses', models.CharField(max_length=3000, null=True, verbose_name='Closed Businesses Description')),
                ('hasstayathomeorder', models.BooleanField(null=True, verbose_name='Has Stay At Home Order')),
                ('economystate', models.ForeignKey(db_column='economystateid', on_delete=django.db.models.deletion.CASCADE, to='covid19.EconomyState')),
            ],
        ),
        migrations.CreateModel(
            name='EventDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventdate', models.DateField(verbose_name='Date of Event')),
                ('event', models.ForeignKey(db_column='eventid', on_delete=django.db.models.deletion.CASCADE, to='covid19.Event')),
            ],
            options={
                'unique_together': {('event', 'eventdate')},
            },
        ),
        migrations.CreateModel(
            name='DailyData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date Pulled From Feed')),
                ('positive', models.IntegerField(null=True, verbose_name='Positive Test Rate Percentage')),
                ('negative', models.IntegerField(null=True, verbose_name='Negative Test Rate Percentage')),
                ('hospitalizedcurrently', models.IntegerField(null=True, verbose_name='Number of People Currently Hospitalized')),
                ('hospitalizedcumulative', models.IntegerField(null=True, verbose_name='Number of People Hospitalized Cumulative')),
                ('inicucurrently', models.IntegerField(null=True, verbose_name='Number of People Currently in ICU')),
                ('inicucumulative', models.IntegerField(null=True, verbose_name='Number of People in ICU Cumulative')),
                ('onventilatorcurrently', models.IntegerField(null=True, verbose_name='Number of People on Ventilator Currently')),
                ('onventilatorcumulative', models.IntegerField(null=True, verbose_name='Number of People on Ventilator Cumulative')),
                ('recovered', models.IntegerField(null=True, verbose_name='Number of People Who Recovered')),
                ('death', models.IntegerField(null=True, verbose_name='Number of People Who have Died')),
                ('deathconfirmed', models.IntegerField(null=True, verbose_name='Number of People Who have Confirmed to have Died from COVID-19')),
                ('deathprobable', models.IntegerField(null=True, verbose_name='Number of People Who have Probably Died from COVID-19')),
                ('positiveincrease', models.IntegerField(null=True, verbose_name='Number of Positive Test Increases')),
                ('negativeincrease', models.IntegerField(null=True, verbose_name='Number of Negative Test Increases')),
                ('totaltests', models.IntegerField(null=True, verbose_name='Number of Total Tests')),
                ('newtests', models.IntegerField(null=True, verbose_name='Number of New Tests')),
                ('newdeaths', models.IntegerField(null=True, verbose_name='Number of New Deaths')),
                ('newhospitalizations', models.IntegerField(null=True, verbose_name='Number of New Hospitalizations')),
                ('state', models.ForeignKey(db_column='geocodeid', on_delete=django.db.models.deletion.CASCADE, to='covid19.State')),
            ],
            options={
                'unique_together': {('state', 'date')},
            },
        ),
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
        migrations.RunSQL(vcensusdata, "drop view covid19_vcensusdata"),
        migrations.RunSQL(vcompletecoviddata, "drop view covid19_vcompletecoviddata"),
        migrations.RunSQL(veventrelatedcoviddata, "drop view covid19_veventrelatedcoviddata"),
        migrations.RunSQL(vlatestdatecoviddata, "drop view covid19_vlatestdatecoviddata"),
        migrations.RunSQL(vstatereopening, "drop view covid19_vstatereopening"),
    ]
