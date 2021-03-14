var dates;
var data;
var chart;
var start;
var end;

function word_cloud(ctx, src) {
  img = document.createElement("img");
  img.src = src;
  img.style.width = isMobileDevice() ? "100%" : "75%";
  img.style.height = "auto";
  ctx.prepend(img);
}

function line_graph(ctx, data, labels, color, title) {
  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          lineTension: 0,
          backgroundColor: "transparent",
          borderColor: color,
          borderWidth: 4,
          pointBackgroundColor: color,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: title,
      },
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Score",
            },
            ticks: {
              min: 0,
              max: 5,
            },
          },
        ],
        xAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Time",
            },
            type: "time",
            time: {
              displayFormats: {
                day: "DD MMM",
                week: "DD MMM",
                month: "MMM YY",
                quarter: "MMM YY",
                year: "YYYY",
              },
              tooltipFormat: "DD MMM YYYY",
              minUnit: "day",
            },
          },
        ],
      },
      legend: {
        display: false,
      },
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

function render(graph, button) {
  clear_graph();
  select_button(button);
  render_graph(graph);
}

function select_button(target_button) {
  // Deactivate all other buttons
  var parent = document.getElementById("button-container");
  var buttons = parent.children;
  for (var i = 0; i < buttons.length; i++) {
    var button = buttons[i];
    if (button.classList.contains("btn-primary")) {
      button.classList.remove("btn-primary");
      button.classList.add("btn-light");
    }
  }
  // Activate new button
  target_button.classList.remove("btn-light");
  target_button.classList.add("btn-primary");
}

function clear_graph() {
  var parent = document.getElementById("graph-container");
  while (parent.firstChild) parent.removeChild(parent.lastChild);
}

function updateChart(start, end) {
  var startDays = getDiffInDays(dates[0], start);
  var endDays = getDiffInDays(dates[0], end);
  if (start > dates[0]) {
    // if start is later than oldest response
    chart.data.labels = dates.slice(startDays, endDays + 1);
    chart.data.datasets[0].data = data.slice(startDays, endDays + 1);
  } else {
    chart.data.labels = dates;
    chart.data.datasets[0].data = data;
  }
  chart.update();
}

function getDiffInDays(date1, date2) {
  return Math.ceil(Math.abs(date2 - date1) / (1000 * 60 * 60 * 24));
}

function random_hex_color() {
  return "#" + Math.floor(Math.random() * 16777215).toString(16);
}

function render_graph(graph) {
    dates = graph.labels;
    for (var i = 0; i < dates.length; i++) { 
      dates[i] = new Date(dates[i]);
    }
    data = graph.scores;
  
    var ctx = document.getElementById("graph-container").getContext('2d');
    var color = random_hex_color();
    line_graph(ctx, dates, data, color, graph.title);
  
    start = moment().subtract(6, 'days');
    end = moment();
    
    $('input[id="datepicker"]').daterangepicker({
      "locale": {
        "format": "DD/MM/YYYY",
      },
      "showDropdowns": true,
      startDate: new Date(Math.max(start, dates[0])),
      endDate: end,
      "minDate": dates[0],
      "maxDate": end,
      ranges: {
          'Last 7 Days': [moment().subtract(6, 'days'), moment()],
          'Last 30 Days': [moment().subtract(29, 'days'), moment()],
          'This Month': [moment().startOf('month'), moment().endOf('month')],
          'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      }
    }, updateChart);
    updateChart(start, end);
}
