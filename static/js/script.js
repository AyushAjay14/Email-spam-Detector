const label = document.getElementsByClassName("label")[0];
const alertText = document.getElementsByClassName("alertText")[0].innerText;
if (alertText === "") {
  label.style.display = "none";
} else {
  label.style.display = "block";
}
