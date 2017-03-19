function drawRegionsMap() {
    var jsonData = $.ajax({
        url: 'js/countryStats.json',
        dataType: 'json',
    }).done(function (results) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Country');
        data.addColumn('number', 'Movie count');

        $.each(results, function(index, value) {
            data.addRow([index,value]);
        });

        var options = {
            colorAxis: {colors: ['#fdfd96', '#fadadd', '#db7093'], values: [1, 30, 150]},
            backgroundColor: '#b0e0e6',
        };
        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
        chart.draw(data, options);
    });
}

function drawYearChart() {
    var jsonData = $.ajax({
        url: 'js/yearStats.json',
        dataType: 'json',
    }).done(function (results) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Decade');
        data.addColumn('number', 'Movie count');

        $.each(results, function(index, value) {
            data.addRow([index,value]);
        });

        var options = {
            legend: { position: 'none' },
            colors:['#db7093'],
        };
        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    });
}

function drawGenreChart() {
    var jsonData = $.ajax({
        url: 'js/genreStats.json',
        dataType: 'json',
    }).done(function (results) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Genre');
        data.addColumn('number', 'Movie count');

        $.each(results, function(index, value) {
            data.addRow([index,value]);
        });

        var options = {
            pieHole: 0.4,
            sliceVisibilityThreshold: .02
        };
        var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
        chart.draw(data, options);
    });
}

google.charts.load('current', {'packages':['geochart', 'corechart']});
google.charts.setOnLoadCallback(drawRegionsMap);
google.charts.setOnLoadCallback(drawYearChart);
google.charts.setOnLoadCallback(drawGenreChart);
