# String constants representing the database view definitions

vcensusdata = """CREATE OR REPLACE VIEW covid19_vcensusdata
 AS
 SELECT t1.geocodeid,
    t1.population,
    t1.density,
    t2.name,
    t2.abbreviation
   FROM ( SELECT geocodeid,
            population,
            density
           FROM covid19_censusdata
        UNION
         SELECT 999 AS geocodeid,
            sum(population) AS sum,
            NULL::numeric AS density
           FROM covid19_censusdata) t1
     JOIN state t2 ON t1.geocodeid = t2.geocodeid;"""

vcompletecoviddata = """CREATE OR REPLACE VIEW covid19_vcompletecoviddata
 AS
 SELECT t1.geocodeid,
    t1.name AS state,
    t1.abbreviation AS stateabbr,
    t2.date,
    t2.positive,
    t2.negative,
    t2.hospitalizedcurrently,
    t2.hospitalizedcumulative,
    t2.inicucurrently,
    t2.inicucumulative,
    t2.onventilatorcurrently,
    t2.onventilatorcumulative,
    t2.recovered,
    t2.death,
    t2.deathconfirmed,
    t2.deathprobable,
    t2.positiveincrease,
    t2.negativeincrease,
    t2.totaltests,
    t2.newtests,
    t2.newdeaths,
    t2.newhospitalizations,
    t3.population,
    t3.density,
    t4.economystateid,
    t4.stayathomeexpiredate,
    t4.openbusinesses,
    t4.closedbusinesses,
    t4.hasstayathomeorder,
    t5.percentageoftestingtarget,
    t5.positivitytestrate,
    t5.hospitalizedper100k,
    t5.dailytestsper100k
   FROM covid19_state t1
     JOIN covid19_dailydata t2 ON t2.geocodeid = t1.geocodeid
     LEFT JOIN covid19_censusdata t3 ON t3.geocodeid = t1.geocodeid
     LEFT JOIN covid19_statereopening t4 ON t4.geocodeid = t1.geocodeid
     LEFT JOIN covid19_coronavirustesting t5 ON t5.geocodeid = t1.geocodeid;"""     

veventrelatedcoviddata = """CREATE OR REPLACE VIEW covid19_veventrelatedcoviddata
 AS
 SELECT t3.eventname,
    t4.name AS state,
    t1.geocodeid,
    t1.date,
    t1.positive,
    t1.negative,
    t1.hospitalizedcurrently,
    t1.hospitalizedcumulative,
    t1.inicucurrently,
    t1.inicucumulative,
    t1.onventilatorcurrently,
    t1.onventilatorcumulative,
    t1.recovered,
    t1.death,
    t1.deathconfirmed,
    t1.deathprobable,
    t1.positiveincrease,
    t1.negativeincrease,
    t1.totaltests,
    t1.newtests,
    t1.newdeaths,
    t1.newhospitalizations
   FROM covid19_dailydata t1
     JOIN covid19_eventdate t2 ON t2.eventdate = t1.date
     JOIN covid19_event t3 ON t2.eventid = t3.id
     JOIN covid19_state t4 ON t1.geocodeid = t4.geocodeid;"""

vlatestdatecoviddata="""CREATE OR REPLACE VIEW covid19_vlatestdatecoviddata
 AS
 SELECT t1.geocodeid,
    t1.name AS state,
    t1.abbreviation AS stateabbr,
    t2.date,
    t2.positive,
    t2.negative,
    t2.hospitalizedcurrently,
    t2.hospitalizedcumulative,
    t2.inicucurrently,
    t2.inicucumulative,
    t2.onventilatorcurrently,
    t2.onventilatorcumulative,
    t2.recovered,
    t2.death,
    t2.deathconfirmed,
    t2.deathprobable,
    t2.positiveincrease,
    t2.negativeincrease,
    t2.totaltests,
    t2.newtests,
    t2.newdeaths,
    t2.newhospitalizations,
    t3.population,
    t3.density,
    t4.economystateid,
    t4.stayathomeexpiredate,
    t4.openbusinesses,
    t4.closedbusinesses,
    t4.hasstayathomeorder,
    t5.percentageoftestingtarget,
    t5.positivitytestrate,
    t5.positivitytestrate::character varying(5)::text || '%'::text AS positivitytastratelabel,
    t5.hospitalizedper100k,
    t5.dailytestsper100k
   FROM covid19_state t1
     JOIN covid19_dailydata t2 ON t2.geocodeid = t1.geocodeid
     LEFT JOIN covid19_censusdata t3 ON t3.geocodeid = t1.geocodeid
     LEFT JOIN covid19_statereopening t4 ON t4.geocodeid = t1.geocodeid
     LEFT JOIN covid19_coronavirustesting t5 ON t5.geocodeid = t1.geocodeid
  WHERE (t2.date IN ( SELECT max(dd.date) AS max
           FROM covid19_dailydata dd));"""

vstatereopening = """CREATE OR REPLACE VIEW covid19_vstatereopening
 AS
 SELECT s.name,
    g.stayathomedeclaredate,
    g.stayathomestartdate,
    o.stayathomeexpiredate,
    g.grade,
    es.state,
        CASE
            WHEN o.closedbusinesses::text ~~ '%bars%'::text THEN 1
            WHEN o.closedbusinesses::text ~~ '%Bars%'::text THEN 1
            WHEN o.closedbusinesses::text ~~ '%Nightclubs%'::text THEN 1
            WHEN o.closedbusinesses::text ~~ '%Breweries%'::text THEN 1
            ELSE 0
        END AS barsclosed
   FROM covid19_statereopening o
     JOIN covid19_state s ON o.geocodeid = s.geocodeid
     JOIN covid19_GredeEffDt g ON g.state::text = s.name::text
     JOIN covid19_economystate es ON es.id = o.economystateid;"""
                        