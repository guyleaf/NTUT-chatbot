$(function () {
  let table = document.getElementById("order_table")
  for (var r = 1, n = table.rows.length; r < n; r++) {
    table.rows[r].cells[4].innerHTML = table.rows[r].cells[2].innerHTML * table.rows[r].cells[3].innerHTML //calculate total price
    table.rows[r].cells[0].innerHTML = new Date(table.rows[r].cells[0].innerHTML * 1000).getDate() //transfer timestamp to Date
  }
});