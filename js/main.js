function orderFulfilled(taskId) {
  var row = document.getElementById(taskId);
  row.style.backgroundColor = "#C8E6C9";
  row.querySelector("button").style.display = "none";
  alert("Order fulfilled successfully!");
}
