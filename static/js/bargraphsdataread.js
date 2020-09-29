

var dateselected = ""
var dateSel = new Litepicker({
    element: document.getElementById('datepicker'),
    startDate: "2020-07-21",
    maxDate: "2020-07-21",
    minDate: "2020-03-01",
    onSelect: function (date1) {
        dateselected = dateSel.getDate()
        return dateselected
    }

})

//filter the data
function sortdata(data, param) {
    data = data.sort(function (a, b) {
        return d3.ascending(a[param], b[param])
    })
}

//set up svg using margins
var margin = {
    top: 15,
    right: 60,
    bottom: 60,
    left: 60
};

//declare the width and height of svg element
var width = 960 - margin.left - margin.right;
var height = 700 - margin.top - margin.bottom;


//Initial Params
var chosenXAxis = "Pos_Tests"


//function to convert date object to appropriate string format
function convert(str) {
    var date = new Date(str),
        mnth = ("0" + (date.getMonth() + 1)).slice(-2),
        day = ("0" + date.getDate()).slice(-2);
    return [date.getFullYear(), mnth, day].join("-");
}

// function used for updating x-scale var upon click on axis label
function xScale(dailyData, chosenXAxis) {
    // create scales
    console.log("daily", dailyData)
    console.log(dailyData[0][chosenXAxis])
    var xLinearScale = d3.scaleLinear()
        .range([0, width])
        .domain([0,
            d3.max(dailyData, d => d[chosenXAxis])
        ])
    // .domain([0, d3.max(dailyData, function (d) {
    //     return d[chosenXAxis];
    // })]);
    // console.log("xlinear")
    // console.log(xLinearScale())
    return xLinearScale;
}

//function used for updating y-scale
function yScale(fdata) {
    console.log("height", height)
    var yordscale = d3.scale.ordinal()
        .rangeRoundBands([height, 0], .1)
        .domain(fdata.map(function (d) {
            return d.State;
        }));

    return yordscale
}

//function to create x and y axis
function createaxis(sourcedata, chosenXAxis) {
    // xLinearScale function above csv import
    var xLinearScale = xScale(sourcedata, chosenXAxis);

    var yOrdinalScale = yScale(sourcedata);


    // Create initial axis functions
    var bottomAxis = d3.axisBottom(xLinearScale);
    var yAxis = d3.axisLeft()
        .scale(yOrdinalScale)

    console.log(yOrdinalScale)
    var xaxisheight = height - 27
    console.log(xaxisheight)
    //append x axis
    var xAxis = chartGroup.append("g")
        .classed("x-axis", true)
        .attr("transform", `translate(-60, ${xaxisheight})`)
        .call(bottomAxis);

    chartGroup.append("g")
        .attr("transform", function () {
            return "translate(-60,-10)"
        })
        .call(yAxis);
}

// function used for updating xAxis var upon click on axis label
function renderAxes(newXScale, xAxis) {
    var bottomAxis = d3.axisBottom(newXScale);

    xAxis.transition()
        .duration(1000)
        .call(bottomAxis);

    return xAxis;
}
var svg = ""
var chartGroup = ""
var xLabelsGroup = ""
function removeSvg() {
    var svgArea = d3.select("#scatter").select("svg")

    if (!svgArea.empty()) {
        console.log("removing svg")
        svgArea.remove();
    }

    svg = d3.select("#scatter").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    console.log("svg", svg)

    chartGroup = svg.append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);
    console.log("chartgroup1", chartGroup)

}
//function to create listener to change data on axis click
function xaxislistener(filteredData) {
    xLabelsGroup.selectAll("text")
        .on("click", function () {
            console.log("active?")
            // console.log(xLabelsGroup.selectAll("text").value())
            // get value of selection
            var value = d3.select(this).attr("value");

            if (value !== chosenXAxis) {

                // replaces chosenXAxis with value
                chosenXAxis = value;
                console.log("filtered", filteredData)
                removeSvg();
                var filteredd = filtermydata()
                createbar(filteredd, "totalbar", chosenXAxis, "green");
                createbar(filteredd, "prevbars", chosenXAxis, "red");
                console.log("xlabels", xLabelsGroup)
                xaxislistener(filteredd)

            }
        });
}
var button = d3.select("#filter-btn");
console.log("button", button);
button.on("click", function () {
    removeSvg();
    var filteredd = filtermydata()
    createbar(filteredd, "totalbar", chosenXAxis, "green");
    createbar(filteredd, "prevbars", chosenXAxis, "red");
    console.log("xlabels", xLabelsGroup)
    xaxislistener(filteredd)
});


console.log("chartgroup2", chartGroup)
// function to make a bars of graph

function createbar(sourcedata, cclass, chosenXAxis, color) {

    console.log("cclass", cclass)
    console.log("sourcedata", sourcedata)
    console.log("chosenXaxis", chosenXAxis)
    //sort data
    sortdata(sourcedata, chosenXAxis)

    //select the appropriate daily associated with total
    if (chosenXAxis === "Pos_Tests") {
        var diff = "NewPosCases"
    }
    else {
        var diff = "NewDeaths"
    }

    createaxis(sourcedata, chosenXAxis)
    var xLinearScale = xScale(sourcedata, chosenXAxis);

    var yOrdinalScale = yScale(sourcedata);

    console.log("chartgroup", chartGroup)
    var obj = svg.selectAll("." + cclass)
        // obj = svg.selectAll
        .data(sourcedata)
        .enter()
        .append("g")
        .append("rect")
        .attr("class", "bar")
        .attr("y", function (d) {
            return yOrdinalScale(d.State)
        })
        .attr("fill", color)
        .attr("height", yOrdinalScale.rangeBand())
        .attr("width", function (d) {
            if (cclass == "prevbars") {
                return xLinearScale(d[chosenXAxis] - d[diff])
            }
            else {
                return xLinearScale(d[chosenXAxis])
            }

        });

    // Create group for two x-axis labels
    xLabelsGroup = chartGroup.append("g")
        .attr("transform", `translate(${width / 2}, ${height})`)
        .attr("id", "xlabelsGroup");

    var casesLabel = xLabelsGroup.append("text")
        .attr("x", 0)
        .attr("y", 20)
        .attr("value", "Pos_Tests") // value to grab for event listener
        .classed("active", true)
        .classed("inactive", false)
        .text("Total Cases");

    var deathsLabel = xLabelsGroup.append("text")
        .attr("x", 0)
        .attr("y", 40)
        .attr("value", "Deaths") // value to grab for event listener
        .classed("inactive", true)
        .classed("active", false)
        .text("Total Deaths");

    console.log("xlabel", xLabelsGroup)
    console.log("chosenXaxis", chosenXAxis)
    if (chosenXAxis === "Pos_Tests") {
        console.log("cases Bold")
        casesLabel
            .classed("active", true)
            .classed("inactive", false);
        deathsLabel
            .classed("active", false)
            .classed("inactive", true);
    }
    else {
        console.log("deaths bold")
        casesLabel
            .classed("active", false)
            .classed("inactive", true);
        deathsLabel
            .classed("active", true)
            .classed("inactive", false);
    }

}






//grab current info and return
function filtermydata() {

    var chosenDate = convert(dateSel.getDate().toString())
    console.log("chosendate", chosenDate)

    var filteredData = gdailyData.filter(days => days.Date === chosenDate);

    //function to return unique values of a list
    function uniqueValues(value, index, self) {
        return self.indexOf(value) === index
    }
    var sts = filteredData.map(d => d.State.toUpperCase()).filter(uniqueValues).sort();
    console.log(sts)
    //Create State selection drop down options
    sts.forEach(function (c) {
        var x = d3.select("#stateSelect");
        x.append("option").text(c).attr("value", c);
    })

    var statessel = document.getElementById("stateSelect")

    chosensts = []
    for (i = 0; i < statessel.length; i++) {
        currentoption = statessel[i]
        // console.log(currentoption)
        if (currentoption.selected == true) {
            if (currentoption.value != "all") {
                console.log(currentoption.value)
                chosensts.push(currentoption.value)
            }
        }
    }
    console.log("chosen", chosensts)
    if (chosensts.length != 0) {
        filteredData = filteredData.filter(data => {
            return chosensts.includes(data.State)
        })
    }

    console.log("filtered", filteredData);
    return filteredData;

}


var gdailyData = []
d3.csv("static/js/data/Covid19.csv").then(function (dailyData, err) {
    if (err) throw err;
    console.log(dailyData)
    //Convert necessary string fields to integers
    dailyData.forEach(function (data) {
        data.Pos_Tests = +data.Pos_Tests;
        data.Deaths = +data.Deaths;
        data.income = +data.income;
        data.healthcare = +data.healthcare
    });
    gdailyData = dailyData

    removeSvg();
    var filteredd = filtermydata()
    createbar(filteredd, "totalbar", chosenXAxis, "green");
    createbar(filteredd, "prevbars", chosenXAxis, "red");
    console.log("xlabels", xLabelsGroup)
    xaxislistener(filteredd)
});




