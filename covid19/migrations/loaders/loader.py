from django.db import migrations, models
import pandas as pd
import os
import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fixture_dir = os.path.abspath(os.path.join(BASE_DIR, 'loaders/fixture.data'))
format_str = '%m/%d/%Y' # The desired format for django date

def load_fixture(apps, schema_editor):
    stateQS = loadStateData(apps, schema_editor)
    loadCensusData(apps, schema_editor, stateQS)
    loadCoronaVirusTesting(apps, schema_editor, stateQS)
    loadDailyData(apps, schema_editor, stateQS)

def loadStateData(apps, schema_editor):
    print("Loading State Data.....")
    csv_filename = os.path.join(fixture_dir, 'State.csv')
    MyModel = apps.get_model("covid19", "State")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        data.append(MyModel(
            geocodeid = row.GeoCodeID,
            name = row.state,
            abbreviation = row.state_abbr)
        )
    MyModel.objects.using(db_alias).bulk_create(data)
    objs = MyModel.objects.values()
    return objs

def loadCensusData(apps, schema_editor, stateQS):
    print("Loading Census Data.....")
    csv_filename = os.path.join(fixture_dir, 'CensusData.csv')
    MyModel = apps.get_model("covid19", "CensusData")
    StateModel = apps.get_model("covid19", "State")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        record = stateQS.filter(geocodeid = row.GeoCodeID)[0]
        stateData = StateModel(**record)
        StateModel = apps.get_model("covid19", "State")       
        data.append(MyModel(
            state = stateData,
            population = row.Population,
            density = row.Density)
        )
    MyModel.objects.using(db_alias).bulk_create(data)


def loadCoronaVirusTesting(apps, schema_editor, stateQS):
    print("Loading Corona Virus Testing.....")
    csv_filename = os.path.join(fixture_dir, 'CoronaVirusTesting.csv')
    MyModel = apps.get_model("covid19", "CoronaVirusTesting")
    StateModel = apps.get_model("covid19", "State")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        record = stateQS.filter(geocodeid = row.GeoCodeID)[0]
        stateData = StateModel(**record)
        data.append(MyModel(
            state = stateData,
            percentageoftestingtarget = row.PercentageOfTestingTarget,
            positivitytestrage = row.PositivityTestRate,
            dailytestsper100k = row.DailyTestPer100K,
            hospitalizedper100k = row.HospitalizedPer100K)
        )
    MyModel.objects.using(db_alias).bulk_create(data)        

def loadDailyData(apps, schema_editor, stateQS):
    print("Loading Daily Data Testing.....")
    csv_filename = os.path.join(fixture_dir, 'DailyData.csv')
    MyModel = apps.get_model("covid19", "DailyData")
    StateModel = apps.get_model("covid19", "State")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []
    recCount = 0
    totalRecCount = 0

    for index, row in df.iterrows():
        record = stateQS.filter(geocodeid = row.GeoCodeID)[0]
        stateData = StateModel(**record)
        data.append(MyModel(
            state = stateData,
            date = datetime.datetime.strptime(row.Date, format_str),
            positive = row.Positive,
            negative = row.Negative,
            hospitalizedcurrently = row.HospitalizedCurrently,
            hospitalizedcumulative = row.hospitalizedcumulative,
            inicucurrently = row.InICUCurrently,
            inicucumulative = row.inicucumulative,
            onventilatorcurrently = row.onventilatorcurrently,
            onventilatorcumulative = row.onventilatorcumulative,
            recovered = row.Recovered,
            death = row.Death,
            deathconfirmed = row.DeathConfirmed,
            deathprobable = row.DeathProbable,
            positiveincrease = row.PositiveIncrease,
            negativeincrease = row.NegativeIncrease,
            totaltests = row.TotalTests,
            newtests = row.NewTests,
            newdeaths = row.NewDeaths,
            newhospitalizations = row.NewHospitalizations
            )
        )
        recCount+=1
        if recCount > 99:
            MyModel.objects.using(db_alias).bulk_create(data) 
            data = []
            totalRecCount += recCount
            recCount = 0
            print(f"....Loading {totalRecCount} records")

    if data:
        totalRecCount += recCount
        MyModel.objects.using(db_alias).bulk_create(data) 
        print(f"....Loading {totalRecCount} records")

def unload_fixture(apps, schema_editor):

# delete from django_migrations where app = 'covid19';

# drop table covid19_coronavirustesting;
# drop table covid19_eventdate;
# drop table covid19_gredeeffdt;
# drop table covid19_statereopening;
# drop table covid19_state;
# drop table covid19_event;
# drop table covid19_dailydata;
# drop table covid19_economystate;
# drop table covid19_censusdata;
    
    "Brutally deleting all entries for this model..."

    MyModel = apps.get_model("covid19", "censusdata")
    MyModel.objects.all().delete()

# from .loaders.loader import load_fixture, unload_fixture
# migrations.RunPython(load_fixture, reverse_code=unload_fixture),