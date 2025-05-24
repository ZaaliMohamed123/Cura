// add hovered class to selected list item
let list = document.querySelectorAll(".med-navigation li");
const logo = document.querySelector(".logo");

// function activeLink() {
//   list.forEach((item) => {
//     item.classList.remove("hovered");
//   });
//   this.classList.add("hovered");
// }

// list.forEach((item) => item.addEventListener("click", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".med-navigation");
let main = document.querySelector(".core");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
  if (navigation.classList.contains("active")) {
    logo.style.display = "none";
  } else {
    logo.style.display = "block";
  }
};
