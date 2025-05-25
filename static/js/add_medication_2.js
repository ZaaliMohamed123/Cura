// Navigation hover effects
document.addEventListener('DOMContentLoaded', function() {
  const navItems = document.querySelectorAll(".med-navigation li");
  const logo = document.querySelector(".logo");
  let initiallyHovered = document.querySelector(".med-navigation li.hovered");

  navItems.forEach(item => {
      item.addEventListener("mouseover", function() {
          navItems.forEach(listItem => listItem.classList.remove("hovered"));
          this.classList.add("hovered");
      });

      item.addEventListener("mouseleave", function() {
          navItems.forEach(listItem => listItem.classList.remove("hovered"));
          if (initiallyHovered) initiallyHovered.classList.add("hovered");
      });
  });

  // Menu Toggle
  const toggle = document.querySelector(".toggle");
  const navigation = document.querySelector(".med-navigation");
  const main = document.querySelector(".core");

  toggle.addEventListener('click', function() {
      navigation.classList.toggle("active");
      main.classList.toggle("active");
      logo.style.display = navigation.classList.contains("active") ? "none" : "block";
  });
});

// Autocomplete functionality
document.addEventListener('DOMContentLoaded', function() {
  const medicineInput = document.getElementById('medicineName');
  const selectedMedicine = document.getElementById('selectedMedicine');
  const suggestionsDiv = document.getElementById('suggestions');
  
  medicineInput.addEventListener('input', function() {
      const query = this.value.trim();
      
      fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
          .then(response => response.json())
          .then(data => {
              suggestionsDiv.innerHTML = '';
              
              if (data.length === 0) {
                  suggestionsDiv.innerHTML = '<div class="p-2 text-muted">No results found</div>';
              } else {
                  data.forEach(medicine => {
                      const div = document.createElement('div');
                      div.className = 'p-2 cursor-pointer';
                      
                      // Highlight the matched text
                      const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                      const regex = new RegExp(escapedQuery, 'gi');
                      div.innerHTML = medicine.replace(regex, match => `<span style="background-color: yellow;">${match}</span>`);
                      
                      div.addEventListener('click', function() {
                          medicineInput.value = medicine;
                          selectedMedicine.value = medicine;
                          suggestionsDiv.classList.add('d-none');
                      });
                      suggestionsDiv.appendChild(div);
                  });
              }
              
              suggestionsDiv.classList.remove('d-none');
          });
  });
  
  medicineInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
          e.preventDefault();
          if (!selectedMedicine.value) {
              this.value = '';
              alert('Please select a medicine from the suggestions.');
          }
      }
  });
  
  document.addEventListener('click', function(e) {
      if (!medicineInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
          suggestionsDiv.classList.add('d-none');
      }
  });
});

// Dynamic reminder time fields
document.addEventListener('DOMContentLoaded', function() {
  const frequencyInput = document.getElementById('frequency');
  const reminderTimesContainer = document.getElementById('reminderTimesFields');

  function updateReminderTimeFields() {
      const numReminders = parseInt(frequencyInput.value, 10);
      reminderTimesContainer.innerHTML = '';

      for (let i = 0; i < numReminders; i++) {
          const div = document.createElement('div');
          div.className = 'col-12 d-flex align-items-center mb-3';

          const label = document.createElement('label');
          label.innerText = `Reminder Time ${i + 1}`;
          label.className = 'form-label fw-semibold me-3 mb-0';
          label.style.minWidth = '150px';

          const input = document.createElement('input');
          input.type = 'time';
          input.className = 'form-control flex-grow-1';
          input.id = `reminderTime_${i + 1}`;
          input.name = `reminderTime_${i + 1}`;
          input.required = true;

          div.appendChild(label);
          div.appendChild(input);
          reminderTimesContainer.appendChild(div);
      }
  }

  frequencyInput.addEventListener('input', updateReminderTimeFields);
  updateReminderTimeFields();
});

