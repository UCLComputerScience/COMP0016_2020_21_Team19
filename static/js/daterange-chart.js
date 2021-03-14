function updateChart(i, start, end) {
  var startDays = getDiffInDays(groupData[i].dates[0], start);
  var endDays = getDiffInDays(groupData[i].dates[0], end);
  if (start > groupData[i].dates[0]) {
    // if start is later than oldest response
    groupData[i].chart.data.labels = groupData[i].dates.slice(
      startDays,
      endDays + 1
    );
    groupData[i].chart.data.datasets[0].data = groupData[i].scores.slice(
      startDays,
      endDays + 1
    );
  } else {
    groupData[i].chart.data.labels = groupData[i].dates;
    groupData[i].chart.data.datasets[0].data = groupData[i].scores;
  }
  groupData[i].chart.update();
}

function getDiffInDays(date1, date2) {
  return Math.ceil(Math.abs(date2 - date1) / (1000 * 60 * 60 * 24));
}

for (var i in groupData) {
  var dates = groupData[i].dates;
  for (var j = 0; j < dates.length; j++) {
    dates[j] = new Date(dates[j]);
  }
  var data = groupData[i].scores;
  var ctx = document.getElementById(groupData[i].id).getContext("2d");

  var chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          data: data,
          lineTension: 0,
          backgroundColor: "transparent",
          borderColor: "#007bff",
          borderWidth: 4,
          pointBackgroundColor: "#007bff",
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: groupData[i].title,
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

  groupData[i].chart = chart;

  var start = moment().subtract(6, "days");
  var end = moment();

  $('input[id="datepicker' + i + '"]').daterangepicker(
    {
      locale: {
        format: "DD/MM/YYYY",
      },
      showDropdowns: true,
      startDate: new Date(Math.max(start, groupData[i].dates[0])),
      endDate: end,
      minDate: groupData[i].dates[0],
      maxDate: end,
      ranges: {
        "Last 7 Days": [moment().subtract(6, "days"), moment()],
        "Last 30 Days": [moment().subtract(29, "days"), moment()],
        "This Month": [moment().startOf("month"), moment().endOf("month")],
        "Last Month": [
          moment().subtract(1, "month").startOf("month"),
          moment().subtract(1, "month").endOf("month"),
        ],
      },
    },
    function (start, end) {
      updateChart($(this)[0].element[0].dataset.index, start, end);
    }
  );
  updateChart(i, start, end);
}
  