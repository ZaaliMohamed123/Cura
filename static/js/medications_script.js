// add hovered class to selected list item
let list = document.querySelectorAll(".med-navigation li");
const logo = document.querySelector(".logo");
// On mémorise l'élément hovered au départ
let initiallyHovered = document.querySelector(".med-navigation li.hovered");
console.log(initiallyHovered);

list.forEach((item) => {
  item.addEventListener("mouseover", function() {
    list.forEach((listItem) => {
      listItem.classList.remove("hovered");
    });
    this.classList.add("hovered");
  });

  item.addEventListener("mouseleave", function() {
    // Retirer la classe hovered de tous
    list.forEach((listItem) => {
      listItem.classList.remove("hovered");
    });
    // Restaurer l'élément hovered initial
    
    initiallyHovered.classList.add("hovered");
    
  });
});



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
