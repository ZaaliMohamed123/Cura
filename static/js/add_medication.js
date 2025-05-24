// add hovered class to selected list item
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





// //Medication form 

// document.getElementById('addMedicineForm').addEventListener('submit', async function(event) {
//     event.preventDefault(); // Prevent the default form submission

//     // Extract form data
//     const formData = {
//         medicineName: document.getElementById('medicineName').value,
//         dosage: document.getElementById('dosage').value,
//         frequency: document.getElementById('frequency').value,
//         startDate: document.getElementById('startDate').value,
//         endDate: document.getElementById('endDate').value
//     };

//     try {
//         // Send POST request to the Flask backend
//         const response = await fetch('/add_medication', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(formData)
//         });

//         const data = await response.json();

//         if (response.ok) {
//             createToast(data.message);
//             console.log(data.message);
//             setTimeout(() => window.location.href = "/medications", 5000);
//         } else {
//             createToast(data.message);
//             console.log(data.error);
//         }
//     } catch (error) {
//         createToast('error');
//         console.log(error);
//     }
// });


// //notification 
// const notifications = document.querySelector(".notifications");
// // Object containing details for different types of toasts
// const toastDetails = {
//     timer: 2000,
//     success: {
//         icon: 'bx bxs-check-circle',
//         text: 'Medication added successfully!',
//     },
//     error: {
//         icon: 'bx bxs-x-circle',
//         text: 'An error occurred while adding the medication.',
//     },
// }

// const removeToast = (toast) => {
//     toast.classList.add("hide");
//     if(toast.timeoutId) clearTimeout(toast.timeoutId); // Clearing the timeout for the toast
//     setTimeout(() => toast.remove(), 2000); // Removing the toast after 500ms
// }
// const createToast = (id) => {
//     // Getting the icon and text for the toast based on the id passed
//     const { icon, text } = toastDetails[id];
//     const toast = document.createElement("li"); // Creating a new 'li' element for the toast
//     toast.className = `toast ${id}`; // Setting the classes for the toast
//     // Setting the inner HTML for the toast
//     toast.innerHTML = `<div class="column">
//                          <i class="${icon}"></i>
//                          <span>${text}</span>
//                       </div>
//                       <i class="bx bx-x" onclick="removeToast(this.parentElement)"></i>`;
//     notifications.appendChild(toast); // Append the toast to the notification ul
//     // Setting a timeout to remove the toast after the specified duration
//     toast.timeoutId = setTimeout(() => removeToast(toast), toastDetails.timer);
// }

