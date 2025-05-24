const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', ()=> {
    container.classList.add('active');
})

loginBtn.addEventListener('click',()=>{
    container.classList.remove('active');
})

const dateInput = document.getElementById('date_of_birth');

// Set initial placeholder
dateInput.setAttribute('placeholder', 'Date of birth');

// Function to switch to date input
function switchToDateInput() {
    if (dateInput.type === 'text') {
        dateInput.type = 'date';
        dateInput.setAttribute('placeholder', ''); // Remove placeholder when switching to date
    }
}

// Function to switch back to text input if no date is selected
function switchToTextInput() {
    if (dateInput.type === 'date' && dateInput.value === '') {
        dateInput.type = 'text';
        dateInput.setAttribute('placeholder', 'Date of birth'); // Set placeholder back when switching to text
    }
}

// Event listeners
dateInput.addEventListener('focus', switchToDateInput);
dateInput.addEventListener('blur', switchToTextInput);


//SignUp---------------------------------------------------------
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = new FormData(e.target);
    const email = formData.get('email_signup');
    const password = formData.get('password_signup');
    const first_name = formData.get('first_name');
    const last_name = formData.get('last_name');
    const phone_number = formData.get('phone_number');
    const date_of_birth = formData.get('date_of_birth');


    try {
        // Send signup request via AJAX
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password,
                first_name,
                last_name,
                phone_number,
                date_of_birth
            }),
        });

        const data = await response.json();

        if (response.ok) {
            createToast(data.message)
            console.log(data.message)
            setTimeout(() => window.location.reload() , 1000); // Removing the toast after 500ms
            // window.location.href = "/";
        } else {
            createToast(data.error)
            console.log(data.error)
        }
    } catch (error) {
        createToast(data.error)
        console.log(data.error)
    }
});

// <i class='bx bxs-check-circle'></i> 
// <i class='bx bxs-x-circle'></i>
// <i class='bx bx-x' ></i>

const notifications = document.querySelector(".notifications");
// Object containing details for different types of toasts
const toastDetails = {
    timer: 1000,
    success: {
        icon: 'bx bxs-check-circle',
        text: 'Success: Account created successfully. Please login.',
    },
    error: {
        icon: 'bx bxs-x-circle',
        text: 'Error: Email already exists.',
    },
    noUser :{
        icon: 'bx bxs-x-circle',
        text: 'Error: User not found.',
    },
    passProb     : {
        icon: 'bx bxs-x-circle',
        text: 'Error: Invalid password.',
    }

}
const removeToast = (toast) => {
    toast.classList.add("hide");
    if(toast.timeoutId) clearTimeout(toast.timeoutId); // Clearing the timeout for the toast
    setTimeout(() => toast.remove(), 500); // Removing the toast after 500ms
}
const createToast = (id) => {
    // Getting the icon and text for the toast based on the id passed
    const { icon, text } = toastDetails[id];
    const toast = document.createElement("li"); // Creating a new 'li' element for the toast
    toast.className = `toast ${id}`; // Setting the classes for the toast
    // Setting the inner HTML for the toast
    toast.innerHTML = `<div class="column">
                         <i class="${icon}"></i>
                         <span>${text}</span>
                      </div>
                      <i class="bx bx-x" onclick="removeToast(this.parentElement)"></i>`;
    notifications.appendChild(toast); // Append the toast to the notification ul
    // Setting a timeout to remove the toast after the specified duration
    toast.timeoutId = setTimeout(() => removeToast(toast), toastDetails.timer);
}


document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = new FormData(e.target);
    const email = formData.get('email_login');
    const password = formData.get('password_login');


    try {
        // Send signup request via AJAX
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password
            }),
        });

        const data = await response.json();

        if (response.ok) {
            // Redirect to index page on successful login
            window.location.href = "/dashboard";
        } else {
            createToast(data.error)
            console.log(data.error)
        }
    } catch (error) {
        createToast(data.error)
        console.log(data.error)
    }
});