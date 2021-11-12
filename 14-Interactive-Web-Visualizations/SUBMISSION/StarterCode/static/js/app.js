$(document).ready(function() {
    //alert("Page Loaded");
    getData();
});

function getData() {
    let url = "samples.json";

    // AJAX
    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: "json",
        success: function(data) {

            // DO WORK HERE
            console.log(data);
            buildDropdown(data);
            buildBarPlot(data);
        },
        error: function(data) {
            console.log("YOU BROKE IT!!");
        },
        complete: function(data) {
            console.log("Request finished");
        }
    });

} ////// FUNCTIONS/////////
function buildDropdown(data) {
    let names = data.names;

    for (let i = 0; i < names.length; i++) {
        let name = names[i];
        let html = `<option value="${name}">${name}</option>`;
        $("#selDataset").append(html);
    }
}

function buildBarPlot(data) {
    let curr_id = $("#selDataset").val();
    let curr_data = data.samples.filter(x => x.id === curr_id)[0];

    var data = [{
        type: 'bar',
        x: [20, 14, 23],
        y: ['giraffes', 'orangutans', 'monkeys'],
        orientation: 'h'
    }];

    Plotly.newPlot('myDiv', data);
}