# from django.core.serializers.json import DjangoJSONEncoder  
try:
    import simplejson as json
except ImportError:
    import json
import datetime  
import pandas as pd

def loadMostChangedState(engine):
    # This should be put in separate file
    statement = """\
select s.Name, t1.*, ro.stayathomestartdate, ro.stayathomeexpiredate, ro.state as economystate
from dailydata t1
join (
select max(positiveincrease) as PositiveIncrease, max(date) as MaxDate
from dailydata
where date = (
	select max(date)
	from dailydata
)
) t2 on t1.positiveincrease = t2.positiveincrease
join state s on s.geocodeid = t1.geocodeid
join vstatereopening ro on ro.name = s.name"""
    print(statement)

    with engine.connect() as conn:
        rs = conn.execute(statement)
        table = {}
        for row in rs:
            table = row

    print(table)
    return table

def convertRowProxyToDictionaryList(result, includeColumns):
    rows = []
    for v in result:
        rowEntry = {}
        for column, value in v.items():
            if column in includeColumns:
                rowEntry[column] = value
        rows.append(rowEntry)
    return rows

def loadLatestData(engine, dataPointName):
    includeColumns = ['state', 'date', dataPointName]
    # This should be put in separate file
    statement = """\
select *
from vlatestdatecoviddata;"""
    print(statement)

    rows = []
    with engine.connect() as conn:
        result = conn.execute(statement)
        rows = convertRowProxyToDictionaryList(result, includeColumns)
    print(rows)
    df = pd.DataFrame(rows)
    print(df.describe())
    # # response = jsonify({'result': [dict(row) for row in rs]})
    # print(jsonify({'result': [dict(row) for row in result]}))
    # response = jsonify({'result': [dict(row) for row in rows]})
    # response = jsonify(rows)
    # print(response)
    # return rows
    quantiles = df[dataPointName].quantile([.15, .25, .40, .55, .7, .9])
    quantiles.columns = ['Percentage', 'TopValue']

    jsonDataRows = json.dumps(rows,
                        sort_keys=True,
                        indent=4,
                        default=str)
    # jsonData = jsonData.replace("\"","'")
    # jsonData = jsonData.replace("\n", "\\\n")

    jsonDataQuantiles = json.dumps(quantiles.values.tolist(),
                        sort_keys=True,
                        indent=4,
                        default=str)
    return rows, jsonDataRows, jsonDataQuantiles

    
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()                        