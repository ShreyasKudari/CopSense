google.charts.load('current', {
    'packages': ['geochart'],
    // Note: you will need to get a mapsApiKey for your project.
    // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
    'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
});
google.charts.setOnLoadCallback(drawRegionsMap);

function drawRegionsMap() {
    var data = google.visualization.arrayToDataTable([ // <IMPORTANT> need to change the dummy data to sentiment data later
        ['State', 'Sentiment'],
        ['Alabama', 57],
        ['Alaska', 67],
        ['Arizona', 53],
        ['Arkansas', 100],
        ['California', 23],
        ['Colorado', 31],
        ['Connecticut', 56],
        ['Delaware', 25],
        ['Florida', 39],
        ['Georgia', 89],
        ['Hawaii', 85],
        ['Idaho', 34],
        ['Illinois', 73],
        ['Indiana', 43],
        ['Iowa', 90],
        ['Kansas', 3],
        ['Kentucky', 32],
        ['Louisiana', 63],
        ['Maine', 72],
        ['Maryland', 34],
        ['Massachusetts', 39],
        ['Michigan', 82],
        ['Minnesota', 37],
        ['Mississippi', 67],
        ['Missouri', 49],
        ['Montana', 64],
        ['Nebraska', 83],
        ['Nevada', 34],
        ['New Hampshire', 46],
        ['New Jersey', 26],
        ['New Mexico', 43],
        ['New York', 51],
        ['North Carolina', 70],
        ['North Dakota', 38],
        ['Ohio', 28],
        ['Oklahoma', 85],
        ['Oregon', 61],
        ['Pennsylvania', 91],
        ['Rhode Island', 13],
        ['South Carolina', 85],
        ['South Dakota', 73],
        ['Tennessee', 49],
        ['Texas', 95],
        ['Utah', 56],
        ['Vermont', 40],
        ['Virginia', 23],
        ['Washington', 57],
        ['West Virginia', 45],
        ['Wisconsin', 80],
        ['Wyoming', 94]


    ]);

    var options = {
        region: 'US',
        displayMode: 'regions',
        resolution: 'provinces',
        colorAxis: {
            colors: ['#00853f', '#ffffff', '#e31b23']
        },
        backgroundColor: '#81d4fa',
        datalessRegionColor: '#f8bbd0',
        defaultColor: '#f5f5f5',
    };

    var chart = new google.visualization.GeoChart(document.getElementById('geochart-colors'));
    chart.draw(data, options);
};