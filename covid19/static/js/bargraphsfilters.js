// var stateselect = d3.select("#stateSelect")
// stateselect.on("click", limitAfterState)



function limitstates(){
    var statessel = document.getElementById("stateSelect")
    console.log(statessel[1])
    chosensts = []
    for(i = 0; i<statessel.length;i++){
        currentoption = statessel[i]
        console.log(currentoption)
        if(currentoption.selected == true){
            console.log(currentoption.value)
            chosensts.push(currentoption.value)
        }
    }
    console.log(chosensts)

    
    // for(i=0;i=length(chosensts); i++){

    // }
    d3.csv("static/js/data/Covid19.csv").then(function(dailyData,err) {
        if (err) throw err;
        console.log(dailyData)
        dailyData.forEach(function(data) {
            data.Pos_Tests = +data.Pos_Tests;
            data.Deaths = +data.Deaths;
            data.income = +data.income;
            data.healthcare = +data.healthcare
            });
        console.log(chosensts)
        var statefilter = dailyData.filter(data => {
            return chosensts.includes(data.State)

        })
        console.log(statefilter)
        });
    //     console.log(statefilter)
    
    // var cities = statefilter.map(function(siting) {
    //     a = toTitleCase(siting.city)
    //     return(a)
    // }).filter(uniqueValues).sort();

    //     d3.select("#citySelect").html("");

    // cities.forEach(function(c) {
    //     var x = d3.select("#citySelect");
    //     x.append("option").text(c).attr("value", c.toLowerCase());
    //     //console.log(x)
   
}