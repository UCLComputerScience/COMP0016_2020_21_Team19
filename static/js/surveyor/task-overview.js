$(function() {
    $('#toggleAccordions-show').on('click', function(e) {
        $('#accordion .collapse').collapse('show');
    })
    $('#toggleAccordions-hide').on('click', function(e) {
        $('#accordion .collapse').collapse('hide');
    })
});
$("#complete").click(function () {
    var btn = $(this);
    var task = btn.data('task');
    var form = $('<form method="post">');
    form.append(csrf_complete);
    form.append('<input name="task" value="' + task + '" />');
    form.append('<input name="request" value="complete" />');
    $('body').append(form);
    form.submit();
    if (event.stopPropagation) event.stopPropagation(); else event.cancelBubble = true;
    return false;
});

$("#incomplete").click(function () {
    var btn = $(this);
    var task = btn.data('task');
    var form = $('<form method="post">');
    form.append(csrf_incomplete);
    form.append('<input name="task" value="' + task + '" />');
    form.append('<input name="request" value="incomplete" />');
    $('body').append(form);
    form.submit();
    if (event.stopPropagation) event.stopPropagation(); else event.cancelBubble = true;
    return false;
});

$("#delete").click(function () {
    var btn = $(this);
    var task = btn.data('task');
    var form = $('<form method="post">');
    form.append(csrf_delete);
    form.append('<input name="task" value="' + task + '" />');
    form.append('<input name="request" value="delete" />');
    $('body').append(form);
    var message = 'Deleting this task will also delete all responses associated with it. Are you sure you want to delete this task?';
    if (confirm(message)) {
      form.submit();
    }
    if (event.stopPropagation) event.stopPropagation(); else event.cancelBubble = true;
    return false;
});

function updateChart(type, canvas_id) {
    if (type === 'pie') {
        var canvas=document.getElementById(canvas_id + '_bar');
        canvas.style.display="none";
        var canvas=document.getElementById(canvas_id + '_pie');
        canvas.style.display="block";
    } 
    else if (type === 'bar') {
        var canvas=document.getElementById(canvas_id + '_pie');
        canvas.style.display="none";
        var canvas=document.getElementById(canvas_id + '_bar');
        canvas.style.display="block";
    }
}

function isMobileDevice(){
    return ( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));
}

function word_cloud(ctx, src) {
    img = document.createElement('img');
    img.src = src;
    img.style.width = isMobileDevice() ? "100%" : "25%";
    img.style.height = "auto";
    img.alt = "Word cloud"
    ctx.appendChild(img);
}

function bar_chart(ctx, data, labels) {
  var myChart = new Chart (ctx, {
    type: 'bar',
    data: {
      datasets: [{
        data: data,
        backgroundColor: labels.length == 5 ? ['tomato', 'orange', 'Gold', 'LightGreen', 'SeaGreen'] : ['tomato', 'Gold', 'SeaGreen'],
      }],
      labels: labels,
    },
    options: {
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
            ticks: {
                stepSize: 1
            }
        }],
        xAxes: [{
            ticks: {
              display: !isMobileDevice(),
              autoSkip: false
            }
        }]
     }
    },
    responsive: true,
    maintainAspectRatio: false
  });
}

function pie_chart(ctx , data, labels) {
  var myChart = new Chart (ctx, {
    type: 'pie',
    data: {
      datasets: [{
        data: data,
        backgroundColor: labels.length == 5 ? ['tomato', 'orange', 'Gold', 'LightGreen', 'SeaGreen'] : ['tomato', 'Gold', 'SeaGreen'],
      }],
      labels: labels,
    },
    options: {
      legend: {
        display: !isMobileDevice(),
        position: 'bottom',
        align: 'center'
      }
    },
    responsive: true,
    maintainAspectRatio: false
  });
}