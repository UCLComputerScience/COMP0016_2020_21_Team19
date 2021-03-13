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

function render(leaderboardData, button) {
  clear_leaderboard();
  select_button(button);
  render_leaderboard(leaderboardData);
}

function remove_leaderboard() {
  var elem = document.getElementById("leaderboard");
  elem.remove();
}

function add_row(parent, rank, name, score) {
  var row_wrapper = document.createElement("tr");

  var name_wrapper = document.createElement("td");
  var score_wrapper = document.createElement("td");
  var rank_wrapper = document.createElement("td");

  rank_wrapper.textContent = rank;
  name_wrapper.textContent = name;
  score_wrapper.textContent = score;

  var new_elements = [];
  new_elements.push(rank_wrapper, name_wrapper, score_wrapper);

  for (var i = 0; i < new_elements.length; i++) {
    row_wrapper.appendChild(new_elements[i]);
  }
  parent.appendChild(row_wrapper);
}

function clear_leaderboard() {
  var parent = document.getElementById("table-body");
  while (parent.firstChild) parent.removeChild(parent.lastChild);
}

function render_leaderboard(leaderboard) {
  var parent = document.getElementById("table-body");

  for (var i = 0; i < leaderboard.length; i++) {
    var row = leaderboard[i];
    add_row(parent, i + 1, row["name"], row["score"]);
  }
}
