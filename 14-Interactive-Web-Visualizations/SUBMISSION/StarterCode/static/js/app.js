$(document).ready(function() {
    //alert("Page Loaded");
    getData();

    $("#selDataset").on("change", function() {
        getData();
    });
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
            buildTable(data);
            buildBubblePlot(data);
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

function buildTable(data) {
    let curr_id = parseInt($("#selDataset").val());
    let curr_data = data.metadata.filter(x => x.id === curr_id)[0];

    $("#sample-metadata").empty();
    let items = Object.entries(curr_data).map(([key, value]) => `${key}: ${value}`);
    for (let i = 0; i < items.length; i++) {
        let item = items[i];
        let html_text = `<p>${item}<p>`;
        $("#sample-metadata").append(html_text);
    }
}

function buildBarPlot(data) {
    let curr_id = $("#selDataset").val();
    let curr_data = data.samples.filter(x => x.id === curr_id)[0];

    // Trace1 
    let trace1 = {
        x: curr_data.sample_values.slice(0, 10).reverse(),
        y: curr_data.otu_ids.map(x => `OTU ID: ${x}`).slice(0, 10).reverse(),
        text: curr_data.otu_labels.slice(0, 10).reverse(),
        name: "Bacteria Count",
        type: "bar",
        marker: {
            color: "#fc5a03"
        },
        orientation: 'h'
    };

    // Create data array
    let traces = [trace1];

    // Apply a title to the layout
    let layout = {
        title: "Belly Button Bacteria Count",
        xaxis: {
            title: "Bacteria Number"
        }
    };

    Plotly.newPlot('bar', traces, layout);
}

function buildBubblePlot(data) {
    let curr_id = $("#selDataset").val();
    let curr_data = data.samples.filter(x => x.id === curr_id)[0];

    // Trace1 
    let trace1 = {
        x: curr_data.otu_ids,
        y: curr_data.sample_values,
        text: curr_data.otu_labels,
        mode: 'markers',
        marker: {
            color: curr_data.otu_ids,
            size: curr_data.sample_values,
            colorscale: 'Hot',
        }
    };

    let traces = [trace1];

    let layout = {
        title: 'Bacteria Count in Belly Button Bubble Chart',
        showlegend: false,
        xaxis: {
            title: "Bacteria OTU ID"
        },
        yaxis: {
            title: "Bacteria Number"
        },
    };

    Plotly.newPlot('bubble', traces, layout);

};