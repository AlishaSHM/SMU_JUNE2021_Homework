// Store the API query variables.
var baseURL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/";
// Add the dates in the ISO formats
var timeframe = "all_week.geojson";

// build URL
var url = baseURL + timeframe;

// geojson
var tect_plates_url = "static/data/PB2002_boundaries.json";

$(document).ready(function() {
    // AJAX
    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: "json",
        success: function(data) {
            // NESTED AJAX
            $.ajax({
                type: "GET",
                url: tect_plates_url,
                contentType: "application/json",
                dataType: "json",
                success: function(tect_data) {
                    console.log(data);
                    console.log(tect_data)
                    makeMap(data, tect_data);

                },
                error: function(data) {
                    console.log("YOU BROKE IT!!");
                },
                complete: function(data) {
                    console.log("Request finished");
                }
            });

        },
        error: function(data) {
            console.log("YOU BROKE IT!!");
        },
        complete: function(data) {
            console.log("Request finished");
        }
    });
});

function makeMap(data, tect_data) {
    // Create the base layers.
    var dark_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/dark-v10',
        accessToken: API_KEY
    });

    var light_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/light-v10',
        accessToken: API_KEY
    });

    // Create a baseMaps object to contain the streetmap and the darkmap.
    var baseMaps = {
        "Dark": dark_layer,
        "Light": light_layer
    };

    // CREATE THE OVERLAY LAYERS
    // GEO JSON MARKER LAYER
    let features = data.features;
    let geoLayer = L.geoJSON(features, {
        onEachFeature: onEachFeature
    });

    let plateLayer = L.geoJson(tect_data, {
        // Passing in our style object
        style: function(feature) {
            return {
                color: "#f5c542",
                weight: 5
            };
        }
    });


    let tectplateLayer = L.geoJson(tect_data);

    var earthquakeMarkers = L.markerClusterGroup();
    var heatArray = [];
    var circleArray = [];
    for (var i = 0; i < features.length; i++) {
        var location = features[i].geometry;

        if (location) {
            // add heat map data
            heatArray.push([location.coordinates[1], location.coordinates[0]]);

            let marker = L.marker([location.coordinates[1], location.coordinates[0]]);
            marker.bindPopup(`<h1>${features[i].properties.mag}<b> MAG</b></h1><hr><p>${features[i].properties.place}</h1>`);
            earthquakeMarkers.addLayer(marker);

            // create the circle marker
            let circle = L.circle([location.coordinates[1], location.coordinates[0]], {
                fillOpacity: 0.75,
                color: makeColor(location.coordinates[2]),
                fillColor: makeColor(location.coordinates[2]),
                // Setting our circle's radius to equal the output of our markerSize() function:
                // This will make our marker's size proportionate to its population.
                radius: makeRadius(features[i].properties.mag)
            }).bindPopup(`<h1>${features[i].properties.mag}<b> MAG</b></h1><hr><p>${features[i].properties.place}</h1>`);
            circleArray.push(circle);
        }
    }

    // Create  layer groups for circles
    var circleLayer = L.layerGroup(circleArray);

    var heatLayer = L.heatLayer(heatArray, {
        radius: 110,
        blur: 20
    });

    // Create an overlayMaps object to contain the "State Population" and "City Population" layers
    var overlayMaps = {
        "Earthquake Clusters": earthquakeMarkers,
        "Earthquakes": geoLayer,
        "Heatmap": heatLayer,
        "Circles": circleLayer,
        "Tect Plates": tectplateLayer
    };

    // Modify the map so that it has the streetmap, states, and cities layers
    var myMap = L.map("map", {
        center: [37.09, -95.71],
        zoom: 5,
        layers: [dark_layer, circleLayer]
    });

    // Create a layer control that contains our baseMaps and overlayMaps, and add them to the map.
    L.control.layers(baseMaps, overlayMaps).addTo(myMap);

    var legend = L.control({ position: 'bottomleft' });
    legend.onAdd = function(map) {
        var div = L.DomUtil.create('div', 'info legend');

        let legend_html = `<i class="circle" style='background: #90f542'></i><span>-10-10</span><br>
    <i class="circle" style='background: #bff542'></i><span>10-30</span><br>
    <i class="circle" style='background: #eff542'></i><span>30-50</span><br>
    <i class="circle" style='background: #f5ce42'></i><span>50-70</span><br>
    <i class="circle" style='background: #f5a442'></i><span>70-90</span><br>
    <i class="circle" style='background: #f56042'></i><span>90+</span>`;

        div.innerHTML = legend_html;
        return div;
    }
    legend.addTo(myMap);

}

// Helper Function
function onEachFeature(feature, layer) {
    layer.bindPopup(`<h1>${feature.properties.mag}<b> MAG</b></h1><hr><p>${feature.properties.place}</p>`);
}

// HELPER FUNCTION FOR RADIUS
function makeRadius(magnitude) {
    // Adjust the radius
    return magnitude * 20000;
}

// HELPER FUNCTION FOR COLOR
function makeColor(depth) {
    let rtnColor = "90f542";

    // Conditionals for earthquake magnitude
    if (depth > 90) {
        rtnColor = "#f56042";
    } else if (depth > 70) {
        rtnColor = "#f5a442";
    } else if (depth > 50) {
        rtnColor = "#f5ce42";
    } else if (depth > 30) {
        rtnColor = "#eff542";
    } else if (depth > 10) {
        rtnColor = "#bff542";
    } else {
        rtnColor = "#90f542";
    }

    return rtnColor;
}