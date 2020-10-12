from django.db import models

# Create your models here.

class State(models.Model):
    geocodeid = models.IntegerField("Geographic Code Identifier",primary_key=True)
    name = models.CharField("State Name", null=False, max_length=100, unique=True)
    abbreviation = models.CharField("State Abbreviation", null=False, max_length=2)
    
    def __str__(self):
        return self.name

class CensusData(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, primary_key=True, unique=True, db_column="geocodeid")
    population = models.IntegerField("Population", null=False)
    density = models.FloatField("Population Density", null=True)

    def __str__(self):
        return f"{self.name}:{str(self.geocodeid)}"

class CoronaVirusTesting(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, primary_key=True, unique=True, db_column="geocodeid")
    percentageoftestingtarget = models.IntegerField("Percentage Of Testing Target", null=True)
    positivitytestrage = models.IntegerField("Positivity Test Rage", null=True)
    dailytestsper100k = models.IntegerField("Daily Tests Per 100,000", null=True)
    hospitalizedper100k = models.IntegerField("Hospitalized Per 100,000", null=True)

    def __str__(self):
        return f"{self.name}:{str(self.state.geocodeid)}"


class DailyData(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, db_column="geocodeid")
    date = models.DateField("Date Pulled From Feed")
    positive = models.IntegerField("Positive Test Rate Percentage", null=True)
    negative = models.IntegerField("Negative Test Rate Percentage", null=True)
    hospitalizedcurrently = models.IntegerField("Number of People Currently Hospitalized", null=True)
    hospitalizedcumulative = models.IntegerField("Number of People Hospitalized Cumulative", null=True)
    inicucurrently = models.IntegerField("Number of People Currently in ICU", null=True)
    inicucumulative = models.IntegerField("Number of People in ICU Cumulative", null=True)
    onventilatorcurrently = models.IntegerField("Number of People on Ventilator Currently", null=True)
    onventilatorcumulative = models.IntegerField("Number of People on Ventilator Cumulative", null=True)
    recovered = models.IntegerField("Number of People Who Recovered", null=True)
    death = models.IntegerField("Number of People Who have Died", null=True)
    deathconfirmed = models.IntegerField("Number of People Who have Confirmed to have Died from COVID-19", null=True)
    deathprobable = models.IntegerField("Number of People Who have Probably Died from COVID-19", null=True)
    positiveincrease = models.IntegerField("Number of Positive Test Increases", null=True)
    negativeincrease = models.IntegerField("Number of Negative Test Increases", null=True)
    totaltests = models.IntegerField("Number of Total Tests", null=True)
    newtests = models.IntegerField("Number of New Tests", null=True)
    newdeaths = models.IntegerField("Number of New Deaths", null=True)
    newhospitalizations = models.IntegerField("Number of New Hospitalizations", null=True)

    def __str__(self):
        return f"{self.name}:{str(self.state.geocodeid)}" 

    class Meta:
        unique_together=(("state", "date"),)

class EconomyState(models.Model):  
    id = models.IntegerField("ID", primary_key=True)
    state = models.CharField("State", max_length=25, null=False) 

    def __str__(self):
        return self.state   

class Event(models.Model):  
    id = models.IntegerField("ID", primary_key=True)
    eventname = models.CharField("Name of Event", max_length=50, null=False) 

    def __str__(self):
        return self.eventname   

class EventDate(models.Model):  
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column="eventid")
    eventdate = models.DateField("Date of Event")

    def __str__(self):
        return f"{self.event.eventname}:{self.eventdate.strftime('%Y-%m-%d')}"  

    class Meta:
        unique_together=(("event", "eventdate"),)        

class GredeEffDt(models.Model):
    state = models.ForeignKey(State, to_field='name', db_column='state', primary_key=True, on_delete=models.CASCADE)
    grade = models.CharField("State Grade", max_length=3, null=False)
    stayathomedeclaredate = models.DateField("Date Stay At Home was Declared", null=True)
    stayathomestartdata = models.DateField("Date Stay At Home Started", null=True)
    
    def __str__(self):
       return f"{self.name}:{self.state.name}"

class StateReopening(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, primary_key=True, unique=True, db_column="geocodeid")
    economystate = models.ForeignKey(EconomyState, on_delete=models.CASCADE, null=False, db_column="economystateid")
    stayathomeexpiredate = models.DateField("Date Stay At Home Order Expired", null=True)
    openbusinesses = models.CharField("Open Businesses Description", null=True, max_length=3000)
    closedbusinesses = models.CharField("Closed Businesses Description", null=True, max_length=3000)
    hasstayathomeorder = models.BooleanField("Has Stay At Home Order", null=True)
