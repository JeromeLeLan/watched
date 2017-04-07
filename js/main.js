function drawRegionsMap() {
  var jsonData = $.ajax({
    url: 'js/watched.json',
      dataType: 'json',
  }).done(function (results) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Country');
    data.addColumn('number', 'Movie count');

    $.each(results.countries, function(index, value) {
      data.addRow([value.name,value.count]);
    });

    var options = {
      colorAxis: {
      colors: ['#B6C9D9', '#97BDDB', '#86B5DB', '#2E8CD9'],
        values: [1, 10, 30, 150]
      },
      backgroundColor: '#DAE5ED',
    };
    var chart = new google.visualization.GeoChart(document.getElementById('countries'));
    chart.draw(data, options);
  });
}

function drawYearChart() {
  var jsonData = $.ajax({
    url: 'js/watched.json',
    dataType: 'json',
  }).done(function (results) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Decade');
    data.addColumn('number', 'Movie count');

    $.each(results.decades, function(index, value) {
      data.addRow([index,value]);
    });

    var options = {
      legend: { position: 'none' },
      colors:['#db7093'],
    };
    var chart = new google.visualization.BarChart(document.getElementById('decades'));
    chart.draw(data, options);
  });
}

function drawGenreChart() {
  var jsonData = $.ajax({
    url: 'js/watched.json',
    dataType: 'json',
  }).done(function (results) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Genre');
    data.addColumn('number', 'Movie count');

    $.each(results.genres, function(index, value) {
      data.addRow([index,value]);
    });

    var options = {
      pieHole: 0.3,
      sliceVisibilityThreshold: .03
    };
    var chart = new google.visualization.PieChart(document.getElementById('genres'));
    chart.draw(data, options);
  });
}

google.charts.load('current', {'packages':['geochart', 'corechart']});
google.charts.setOnLoadCallback(drawRegionsMap);
google.charts.setOnLoadCallback(drawYearChart);
google.charts.setOnLoadCallback(drawGenreChart);

$(document).ready(function() {
  var jsonData = $.ajax({
    url: 'js/watched.json',
    dataType: 'json',
  }).done(function (results) {
    var dataSet = [];
    $.each(results.movies, function(index, value) {
      dataSet.push([
        value.watchDate,
        value.original_title,
        value.director,
        value.release_date,
        value.runtime,
        value.personalRating,
        value.poster_path
      ]);
    });
    var table = $('#movieList').DataTable({
      autoWidth: true,
      data: dataSet,
      pageLength: 8,
      lengthChange: false,
      order: [[ 0, "desc" ]],
      columns: [
        { width: "15%", title: "Vu le" },
        { width: "30%", title: "Titre" },
        { width: "30%", title: "Réalisateur" },
        { width: "8%", title: "Année" },
        { width: "7%", title: "Durée" },
        { width: "10%", title: "Note" }
      ]
    });
    document.getElementById("poster").src = 'https://image.tmdb.org/t/p/w300'+table.row(this).data()[6];
    $('#movieList tbody').on('mouseenter', 'td', function () {
      document.getElementById("poster").src = 'https://image.tmdb.org/t/p/w300'+table.row(this).data()[6];
    });
  });
});
