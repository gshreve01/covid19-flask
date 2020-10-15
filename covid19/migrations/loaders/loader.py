from django.db import migrations, models
import pandas as pd
import os
import datetime
import math


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fixture_dir = os.path.abspath(os.path.join(BASE_DIR, 'loaders/fixture.data'))
format_str = '%m/%d/%Y' # The desired format for django date
format_str2 = '%Y-%m-%d' # The desired format for django date

def load_fixture(apps, schema_editor):
    print("Start loading data...")
    stateQS = loadStateData(apps, schema_editor)
    economyStateQS = loadEconomyState(apps, schema_editor)
    loadStateReopening(apps, schema_editor, stateQS, economyStateQS)
    loadGredeEffDt(apps, schema_editor, stateQS)
    loadCensusData(apps, schema_editor, stateQS)
    loadCoronaVirusTesting(apps, schema_editor, stateQS)
    eventsQS = loadEvents(apps, schema_editor)
    loadEventDates(apps, schema_editor, eventsQS)
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
            positivitytestrate = row.PositivityTestRate,
            dailytestsper100k = row.DailyTestPer100K,
            hospitalizedper100k = row.HospitalizedPer100K)
        )
    MyModel.objects.using(db_alias).bulk_create(data)        

def loadDailyData(apps, schema_editor, stateQS):
    print("Loading Daily Data .....")
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
            # break

    if data:
        totalRecCount += recCount
        MyModel.objects.using(db_alias).bulk_create(data) 
        print(f"....Loading {totalRecCount} records")

def loadEconomyState(apps, schema_editor):
    print("Loading EconomyState.....")
    csv_filename = os.path.join(fixture_dir, 'EconomyState.csv')
    MyModel = apps.get_model("covid19", "EconomyState")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        data.append(MyModel(
            id = row.id,
            state = row.state)
        )
    MyModel.objects.using(db_alias).bulk_create(data)
        
    objs = MyModel.objects.values()
    return objs

def loadEvents(apps, schema_editor):
    print("Loading Events.....")
    csv_filename = os.path.join(fixture_dir, 'Events.csv')
    MyModel = apps.get_model("covid19", "Event")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        data.append(MyModel(
            id = row.id,
            eventname = row.eventname)
        )
    MyModel.objects.using(db_alias).bulk_create(data)    
    objs = MyModel.objects.values()
    return objs

def loadEventDates(apps, schema_editor, eventsQS):
    print("Loading Event Dates.....")
    csv_filename = os.path.join(fixture_dir, 'EventDates.csv')
    MyModel = apps.get_model("covid19", "EventDate")
    EventModel = apps.get_model("covid19", "Event")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        record = eventsQS.filter(id = row.eventid)[0]
        eventData = EventModel(**record)        
        data.append(MyModel(
            event = eventData,
            eventdate = datetime.datetime.strptime(row.eventdate, format_str))
        )
    MyModel.objects.using(db_alias).bulk_create(data)    


def loadGredeEffDt(apps, schema_editor, stateQS):
    print("Loading Grade Effective Date.....")
    csv_filename = os.path.join(fixture_dir, 'StayatHomeGrades.csv')
    MyModel = apps.get_model("covid19", "GredeEffDt")
    StateModel = apps.get_model("covid19", "State")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        record = stateQS.filter(name = row.State)[0]
        stateData = StateModel(**record)
        data.append(MyModel(
            state = stateData,
            grade = row.Grade,
            stayathomedeclaredate = dateValueOrNone(row["Date Announced"], format_str2),
            stayathomestartdate = dateValueOrNone(row["Effective Date"], format_str2))          
        )
    MyModel.objects.using(db_alias).bulk_create(data) 

def dateValueOrNone(value, format_str):
    if value and not str(value) == 'nan':
        return datetime.datetime.strptime(value, format_str)
    else:
        return None

def loadStateReopening(apps, schema_editor, stateQS, economyStateQS):
    print("Loading State Reopening.....")
    csv_filename = os.path.join(fixture_dir, 'CovidOpeningData.csv')
    MyModel = apps.get_model("covid19", "StateReopening")
    StateModel = apps.get_model("covid19", "State")
    EconomyStateModel = apps.get_model("covid19", "EconomyState")
    db_alias = schema_editor.connection.alias

    df = pd.read_csv(csv_filename, delimiter=',')
    data = []

    for index, row in df.iterrows():
        economyStateKey = row.economy_state.replace("EconomyState.", "")
        record = stateQS.filter(name = row.state)[0]
        stateData = StateModel(**record)
        record = economyStateQS.filter(state = economyStateKey)[0]
        economyStateData = EconomyStateModel(**record)
        data.append(MyModel(
            state = stateData,
            economystate = economyStateData,
            stayathomeexpiredate = dateValueOrNone(row.expired_on, format_str),
            openbusinesses = row.open,
            closedbusinesses = row.close,
            hasstayathomeorder = row.had_stay_at_home_order == 'True')          
        )
    MyModel.objects.using(db_alias).bulk_create(data) 

def unload_fixture(apps, schema_editor):

    # Dropping Views
    print("Dropping Views....")
    migrations.RunSQL("drop view covid19_vcensusdata;")
    migrations.RunSQL("drop view covid19_vcompletecoviddata;")
    migrations.RunSQL("drop view covid19_veventrelatedcoviddata;")
    migrations.RunSQL("drop view covid19_vlatestdatecoviddata;")
    migrations.RunSQL("drop view covid19_vstatereopening;")

    # Dropping Tables
    print("Dropping Tables....")
    migrations.RunSQL("drop table covid19_coronavirustesting;")
    migrations.RunSQL("drop table covid19_eventdate")
    migrations.RunSQL("drop table covid19_gredeeffdt")
    migrations.RunSQL("drop table covid19_statereopening")
    migrations.RunSQL("drop table covid19_event")
    migrations.RunSQL("drop table covid19_dailydata")
    migrations.RunSQL("drop table covid19_economystate")
    migrations.RunSQL("drop table covid19_censusdata")
    migrations.RunSQL("drop table covid19_state")  

# delete from django_migrations where app = 'covid19';

# drop table covid19_coronavirustesting;
# drop table covid19_eventdate;
# drop table covid19_gredeeffdt;
# drop table covid19_statereopening;
# drop table covid19_event;
# drop table covid19_dailydata;
# drop table covid19_economystate;
# drop table covid19_censusdata;
# drop table covid19_state;
    
    # "Brutally deleting all entries for this model..."

    # MyModel = apps.get_model("covid19", "censusdata")
    # MyModel.objects.all().delete()

# from .loaders.loader import load_fixture, unload_fixture
# migrations.RunPython(load_fixture, reverse_code=unload_fixture),