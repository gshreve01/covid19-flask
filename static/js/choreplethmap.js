console.log('starting choreplethmap');

console.log("datapointName", datapointName);
console.log("datapointDescription", datapointDescription);

// // Setup Form submit
// var form = d3.select("#form");
// console.log("form", form);
// form.on("submit", runFormSearch);

// Setup the button
var button = d3.select("#filter-btn");
console.log("button", button);
button.on("click", runFormSearch);

function runFormSearch() {
  // build route
  selectedDataType = datatypeSelect.property("value");
  var route = "Maps/" + selectedDataType
  window.location.href = "http://127.0.0.1:5000/" + route;
}

// DataType Selection
console.log("datapointmap", dataPointMap);
var datatypeSelect = d3.select("#dataType");
datatypeSelect.on("change", function () {
  console.log("Entering datatypeSelect on change event");
  selectedDataType = Array.from(this.options) // create an array from the htmlCollection
    .filter(function (option) { return option.selected })  // filter for selected values
    .map(function (option) { return option.value; }); // return a new array with the selected values
  console.log("selectedDataType", selectedDataType);
});


console.log("datapointMap.keys", dataPointMap.keys);
var options = datatypeSelect.selectAll("option").data(dataPointMap).enter().append("option")
  .text(function (d) { return d.description; })
  .attr("value", function (d) { return d.name });

var datapointIndex = dataPointMap.map((x) => x.name).indexOf(datapointName);
console.log("datapointIndex", datapointIndex);

// datatypeSelect.selectedIndex = datapointIndex;
// I sort of hate going old school....but d3 select was not working...and no time.
document.getElementById("dataType").selectedIndex = datapointIndex;
console.log("datatypeSelect", datatypeSelect);

// Need to convert the data to javascript array
console.log('rows', rows)
// rows = rows.replace("\\\n", "\n").replace("\"", "'")
// console.log('JSON rows', JSON.parse(rows))
var repositoryDataArray = rows;
console.log(repositoryDataArray);

// sort the quantile values in descending order
quantiles = quantiles.map((x => Math.round(x)));
quantiles = quantiles.sort((a, b) => b - a);
console.log("quantiles", quantiles);


var mapData = {};
function loadStatesData() {
  Object.assign(mapData, statesData);

  // console.log(jsonArray);

  console.log(mapData.features);

  mapData.features.forEach((feature) => {
    // Get the state that the feature represents
    var stateName = feature.properties.name;
    var stateRow = repositoryDataArray.filter(x => x.state == stateName)[0];
    feature.properties["density"] = stateRow["density"];
    feature.properties[datapointName] = stateRow[datapointName];
    console.log("feature.properties", feature.properties);
    // console.log(stateName, stateRow);
  }
  );
}

// taken from: https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function getColor(d) {
  return d > quantiles[0] ? '#800026' :
    d > quantiles[1] ? '#BD0026' :
      d > quantiles[2] ? '#E31A1C' :
        d > quantiles[3] ? '#FC4E2A' :
          d > quantiles[4] ? '#FD8D3C' :
            d > quantiles[5] ? '#FEB24C' :
              //  d > quantiles[6]   ? '#FED976' :
              '#FFEDA0';
}

// mode function taken from https://stackoverflow.com/questions/52898456/simplest-way-of-finding-mode-in-javascript
var mode = a => {
  a.sort((x, y) => x - y);

  var bestStreak = 1;
  var bestElem = a[0];
  var currentStreak = 1;
  var currentElem = a[0];

  for (let i = 1; i < a.length; i++) {
    if (a[i - 1] !== a[i]) {
      if (currentStreak > bestStreak) {
        bestStreak = currentStreak;
        bestElem = currentElem;
      }

      currentStreak = 0;
      currentElem = a[i];
    }

    currentStreak++;
  }

  return currentStreak > bestStreak ? currentElem : bestElem;
};

function loadStatesMap() {
  var geojson;
  var myMap = L.map('map').setView([37.8, -96], 4);

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
    tileSize: 512,
    zoomOffset: -1,
    id: 'mapbox/streets-v11',
    accessToken: API_KEY
  }).addTo(myMap);

  function style(feature) {
    console.log("Setting style");
    return {
      fillColor: getColor(feature.properties[datapointName]),
      weight: 2,
      opacity: 1,
      color: 'white',
      dashArray: '3',
      fillOpacity: 0.7
    };
  }

  function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
      weight: 5,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
      layer.bringToFront();
    }
    info.update(layer.feature.properties);
  }

  function resetHighlight(e) {
    geojson.resetStyle(e.target);
  }

  function zoomToFeature(e) {
    myMap.fitBounds(e.target.getBounds());
    info.update();
  }


  // L.geoJson(mapData, { style: style }).addTo(myMap);

  function onEachFeature(feature, layer) {
    layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      click: zoomToFeature
    });
  }

  geojson = L.geoJson(mapData, {
    style: style,
    onEachFeature: onEachFeature
  }).addTo(myMap);

  var info = L.control();
  info.setPosition("bottomleft");

  info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
  };

  // method that we will use to update the control based on feature properties passed
  info.update = function (props) {

    // var displayValue = numberWithCommas( props[datapointName] );
    this._div.innerHTML = '<h4>US ' + datapointDescription + '</h4>' + (props ?
      '<b>' + props.name + '</b><br />' + numberWithCommas(props[datapointName])
      : 'Hover over a state');
  };

  info.addTo(myMap);

  var legend = L.control({ position: 'bottomright' });
  legend.setPosition("bottomright");
  legend.onAdd = function (map) {

    grades = quantiles.slice().reverse();
    grades.unshift(0);
    console.log("grades", grades);
    var div = L.DomUtil.create('div', 'info legend'),
      grades = grades,
      labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
      div.innerHTML +=
        '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
        grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
  };

  legend.addTo(myMap);

  // L.geoJson(mapData).addTo(myMap);
}



// L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
//   attribution: '© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>',
//   tileSize: 512,
//   maxZoom: 18,
//   zoomOffset: -1,
//   id: 'mapbox/streets-v11',
//   accessToken: API_KEY
// }).addTo(myMap);

loadStatesData();
loadStatesMap();

console.log('finished choreplethmap');

// L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
//     id: 'mapbox/light-v9',
//     attribution: '© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>',
//     tileSize: 512,
//     zoomOffset: -1,
//     accessToken: API_KEY
// }).addTo(myMap);

// Replace out density with latest density as well as
// the rest of the data


