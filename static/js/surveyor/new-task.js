$("#load").click(function () {
  $("#modal-load").modal("show");
});

$("#add_more").click(function () {
  var form_idx = $("#id_form-TOTAL_FORMS").val();
  $("#form_set").append(
    $("#empty_form")
      .html()
      .replace(/__prefix__/g, form_idx)
  );
  $("#id_form-TOTAL_FORMS").val(parseInt(form_idx) + 1);
});

function deleteRow(row) {
  var form_idx = $("#id_form-TOTAL_FORMS").val();
  var inputElem = row.getElementsByTagName("INPUT")[0].id;
  inputElem = inputElem.replace("description", "DELETE");
  $("#" + inputElem).prop("checked", true);
  row.remove();
}

function browserSupportsDateInput() {
  var i = document.createElement("input");
  i.setAttribute("type", "date");
  return i.type !== "text";
}

if (!browserSupportsDateInput()) {
  $(function () {
    $("#id_due_date").datepicker();
  });
  $(document).ready(function () {
    $("input.timepicker").timepicker({
      timeFormat: "HH:mm",
      dynamic: true,
    });
  });
}

const allFields = ["id_group", "id_due_date", "id_due_time"];
$("#save").click(function () {
  allFields.forEach(function (field) {
    $("#" + field).removeAttr("required");
  });
  $("#save").trigger("click");
});

$(".delete-template").click(function () {
  if (confirm("Are you sure you want to delete this template?")) {
    var btn = $(this);
    var template = btn.data("template");
    var form = $('<form method="post">');
    form.append(csrf);
    form.append('<input name="template" value="' + template + '" />');
    form.append('<input name="delete" value="delete_template" />');
    $("body").append(form);
    form.submit();
  } else {
    return false;
  }
  if (event.stopPropagation) event.stopPropagation();
  else event.cancelBubble = true;
});
